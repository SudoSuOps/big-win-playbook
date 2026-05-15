#!/usr/bin/env python3
"""
dmack.ai cook — Qwen3.5-9B-Instruct bf16 LoRA SFT on the JELLY+ corpus.

Implements the recipe in training/cook_recipe.md AFTER the SR Hack repair list
(2026-05-14, sr_hack_signoff_v1.md). Notable:
  - bf16 LoRA, NOT QLoRA (Qwen3.5 has high quantization error per
    gold_standard_70b_meta_cookbook.md lines 120-127)
  - packing=False (per sr_hack_final_look_rule.md + Atlas-Qwen-27B v4 lesson;
    SDPA + packing has cross-pair attention bleed on Blackwell sm_120)
  - max_seq_length=1024 (covers p99=214 tokens with margin; recovers the
    throughput packing would have given without the contamination risk)
  - Renamed from sft_qwen35_9b_qlora.py per Repair 2

Uses smash's full stack:
  - 5090 32 GB GPU bf16 (forward/backward · ~24-28 GB usage expected)
  - 9950X3D 32 threads (16 dataloader workers + persistent + tokenize num_proc=16)
  - 64 GB DDR5 (holds the entire tokenized corpus in memory)
  - 1.8 TB NVMe (checkpoints every 500 steps)

Usage:
  # Stage 2 canary (validate stack works · 50 steps · 1K subset)
  python3 training/sft_qwen35_9b_lora.py --canary

  # Stage 3 full cook
  python3 training/sft_qwen35_9b_lora.py
"""
from __future__ import annotations
import argparse
import os
from pathlib import Path

import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
)
from peft import LoraConfig, get_peft_model
from trl import SFTTrainer, SFTConfig
from datasets import load_dataset

ROOT = Path("/home/smash")
BASE_MODEL = ROOT / "models/qwen3.5-9b-base"
COOK_CORPUS = ROOT / "dmack-ai/training/cook_corpus_jellyplus.jsonl"
OUTPUT_DIR = ROOT / "cooks/dmack-ai-9b-v1"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--canary", action="store_true",
                   help="Stage 2 canary: 1000 pairs, 50 steps, save to cooks/dmack-ai-9b-canary")
    p.add_argument("--base", default=str(BASE_MODEL))
    p.add_argument("--corpus", default=str(COOK_CORPUS))
    p.add_argument("--output", default=str(OUTPUT_DIR))
    p.add_argument("--epochs", type=float, default=3.0)
    p.add_argument("--lr", type=float, default=1e-5)
    p.add_argument("--batch-size", type=int, default=2)   # MD recovery: dropped 4→2 after first canary OOM
    p.add_argument("--grad-accum", type=int, default=16)  # bumped 8→16 to keep effective batch 32
    p.add_argument("--max-seq", type=int, default=2048,
                   help="Per Corpus SR Repair 1: actual sample p90=860 / p99=2,594 "
                        "tokens (recipe SR's 214-token estimate was wrong by ~12×). "
                        "max_seq=2048 covers p90 cleanly + p99 with truncation only "
                        "at the long tail. VRAM ~28-30GB / 32GB at batch=4; if OOM "
                        "drop to batch=2 + grad_accum=16 (effective batch unchanged)")
    args = p.parse_args()

    if args.canary:
        args.output = str(ROOT / "cooks/dmack-ai-9b-canary")
        args.epochs = 1.0

    # ─── Tokenizer
    print(f"[1/6] loading tokenizer from {args.base}")
    tokenizer = AutoTokenizer.from_pretrained(args.base, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    # ─── Base model in bf16 (NOT QLoRA — Qwen3.5 has high quantization error)
    print(f"[2/6] loading base in bf16 (no QLoRA · per gold_standard Qwen rule)")
    model = AutoModelForCausalLM.from_pretrained(
        args.base,
        torch_dtype=torch.bfloat16,
        device_map={"": 0},
        trust_remote_code=True,
        attn_implementation="sdpa",
    )
    model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={"use_reentrant": False})
    model.config.use_cache = False

    # ─── LoRA adapters
    print(f"[3/6] attaching LoRA r=64 alpha=32 on attn+mlp")
    lora_config = LoraConfig(
        r=64,
        lora_alpha=32,
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                        "gate_proj", "up_proj", "down_proj"],
    )
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()

    # ─── Data
    print(f"[4/6] loading corpus from {args.corpus}")
    ds = load_dataset("json", data_files=args.corpus, split="train")
    print(f"  loaded {len(ds):,} pairs")

    if args.canary:
        ds = ds.shuffle(seed=42).select(range(min(1000, len(ds))))
        print(f"  canary subset: {len(ds):,}")

    # Held-out eval (5%)
    splits = ds.train_test_split(test_size=0.05, seed=42)
    train_ds = splits["train"]
    eval_ds = splits["test"]
    print(f"  train: {len(train_ds):,}  eval: {len(eval_ds):,}")

    # Format into chat for SFT (Qwen3.5 chat template)
    def to_chat(example):
        msgs = [
            {"role": "user", "content": example["question"]},
            {"role": "assistant", "content": example["answer"]},
        ]
        return {"text": tokenizer.apply_chat_template(msgs, tokenize=False)}

    train_ds = train_ds.map(to_chat, num_proc=16, remove_columns=train_ds.column_names)
    eval_ds = eval_ds.map(to_chat, num_proc=16, remove_columns=eval_ds.column_names)

    # ─── Trainer config
    print(f"[5/6] configuring SFTTrainer")
    out_path = Path(args.output)
    out_path.mkdir(parents=True, exist_ok=True)

    sft_config = SFTConfig(
        output_dir=str(out_path),
        # Training
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.batch_size,
        gradient_accumulation_steps=args.grad_accum,
        gradient_checkpointing=True,
        learning_rate=args.lr,
        lr_scheduler_type="cosine",
        warmup_ratio=0.03,
        max_grad_norm=1.0,
        # Sequence — packing OFF per SR rule (TRL 1.4: max_seq_length → max_length)
        max_length=args.max_seq,
        packing=False,                       # Per sr_hack_final_look_rule + Atlas v4 lesson
                                              # SDPA+packing has cross-pair contamination on Blackwell sm_120
        dataset_text_field="text",
        # Precision
        bf16=True,
        tf32=True,
        # Eval / save
        eval_strategy="steps",
        eval_steps=50 if args.canary else 200,
        save_strategy="steps",
        save_steps=50 if args.canary else 500,
        save_total_limit=4,
        logging_steps=10 if args.canary else 20,
        # Data pipeline (9950X3D · use it)
        dataloader_num_workers=16,
        dataloader_pin_memory=True,
        dataloader_persistent_workers=True,
        # Reporting — none for canary (skip tensorboard dep); install for full cook if desired
        report_to="none",
        run_name="dmack-ai-9b-canary" if args.canary else "dmack-ai-9b-v1",
        # Canary caps total steps
        max_steps=50 if args.canary else -1,
    )

    trainer = SFTTrainer(
        model=model,
        train_dataset=train_ds,
        eval_dataset=eval_ds,
        args=sft_config,
        processing_class=tokenizer,
    )

    # ─── Train
    print(f"[6/6] starting training")
    trainer.train()
    trainer.save_model(str(out_path / "final"))
    tokenizer.save_pretrained(str(out_path / "final"))
    print(f"\nDONE. Adapter saved to {out_path}/final")


if __name__ == "__main__":
    main()
