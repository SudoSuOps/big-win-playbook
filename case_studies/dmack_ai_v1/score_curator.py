#!/usr/bin/env python3
"""
dmack.ai Curator-9B scoring pass.

Scores every pair in MASTER_dmack_ai_v1_royal_jelly.jsonl on the 5-dimension
medical-companion rubric (VR/SD/CD/SA/TS), maps to a Royal Jelly tier, and
streams results to scored_pairs.jsonl. Supports resume + concurrency.

Usage:
  python3 eval/score_curator.py                    # full run
  python3 eval/score_curator.py --limit 200        # smoke test
  python3 eval/score_curator.py --concurrency 48   # tune
  python3 eval/score_curator.py --resume           # skip already-scored ids
"""
from __future__ import annotations
import argparse
import asyncio
import json
import sys
import time
from pathlib import Path

try:
    import httpx
except ImportError:
    print("Need httpx: pip3 install httpx")
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CORPUS = ROOT / "corpus/MASTER_dmack_ai_v1_royal_jelly.jsonl"
DEFAULT_OUT = ROOT / "eval/scored_pairs.jsonl"
ENDPOINT = "http://localhost:8088/v1/chat/completions"
MODEL = "swarmcurator-9b"

RUBRIC = """You are SwarmCurator scoring a diabetic-companion training pair for the dmack.ai cook.

Score on FIVE dimensions (1-10 each). Output ONLY a single JSON object. NO thinking, NO analysis, NO commentary.

Dimensions:
- VR (Voice Register): warm, direct, prevention-first companion tone. NOT clinical-cold, NOT preachy. Founder voice present but NEVER first-person Donovan claims ("I lost a toe" -> automatic 1).
- SD (Source Discipline): factual claims grounded in documented sources (ADA / IWGDF / NIDDK / Endocrine Society / peer-reviewed). Citations when facts stated. No fabricated DOIs.
- CD (Compliance Discipline): no miracle claims (treats/cures/reverses/prevents), no specific dosing, no diagnosis language, FDA verbatim for supplements, compliance footer where appropriate.
- SA (Safety Alignment): emergency routing correct (call 911 / call provider) for adrenal crisis, DKA, severe hypo, foot infection red flags. No "wait and see" for emergencies.
- TS (Two-Stream Discipline): voice from lived experience (register), facts from documented sources (authority). Donovan is the voice, NEVER the medical authority.

For DATA-recall pairs (CGM data, paper abstracts, public-health stats), score VR / CD / SA / TS by whether the framing is appropriate to the question (data Q -> factual A is fine; don't penalize neutral-clinical tone on a data recall).

OUTPUT EXACTLY THIS SHAPE — JSON ONLY:
{"VR":<int>,"SD":<int>,"CD":<int>,"SA":<int>,"TS":<int>,"note":"<= 20 words on any defect, or empty"}"""

DIMS = ("VR", "SD", "CD", "SA", "TS")


def tier_for(composite: float) -> str:
    if composite >= 9: return "APEX"
    if composite >= 7: return "HONEY"
    if composite >= 5: return "JELLY"
    if composite >= 3: return "POLLEN"
    return "PROPOLIS"


def parse_scores(content: str):
    """Best-effort JSON extraction; returns dict or None."""
    s = content.strip()
    try:
        return json.loads(s)
    except Exception:
        pass
    a, b = s.find("{"), s.rfind("}")
    if a >= 0 and b > a:
        try:
            return json.loads(s[a : b + 1])
        except Exception:
            return None
    return None


def validate(scores) -> bool:
    if not scores:
        return False
    for d in DIMS:
        v = scores.get(d)
        if not isinstance(v, int) or v < 1 or v > 10:
            return False
    return True


async def score_one(client: httpx.AsyncClient, sample: dict, sem: asyncio.Semaphore, max_retries: int = 2):
    pair_id = sample.get("id") or f"row-{sample.get('__row__',0)}"
    q = (sample.get("question") or "")[:1200]
    a = (sample.get("answer") or "")[:2400]
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": RUBRIC},
            {"role": "user", "content": f"PAIR:\n\nQUESTION:\n{q}\n\nANSWER:\n{a}\n\nRespond with the JSON object only — start your message with {{ and emit nothing else."},
        ],
        "max_tokens": 300,
        "temperature": 0.0,
        "response_format": {"type": "json_object"},
        # Belt-and-suspenders: Qwen3.5 defaults to thinking; explicitly off.
        "chat_template_kwargs": {"enable_thinking": False},
    }
    async with sem:
        t0 = time.time()
        last_err = None
        for attempt in range(max_retries + 1):
            try:
                r = await client.post(ENDPOINT, json=payload, timeout=60)
                r.raise_for_status()
                resp = r.json()
                content = resp["choices"][0]["message"]["content"]
                scores = parse_scores(content)
                if validate(scores):
                    composite = sum(scores[d] for d in DIMS) / 5
                    elapsed = time.time() - t0
                    return {
                        "id": pair_id,
                        "source_tag": sample.get("__source_tag__"),
                        "VR": scores["VR"],
                        "SD": scores["SD"],
                        "CD": scores["CD"],
                        "SA": scores["SA"],
                        "TS": scores["TS"],
                        "composite": round(composite, 2),
                        "tier": tier_for(composite),
                        "note": (scores.get("note") or "")[:200],
                        "latency_s": round(elapsed, 2),
                        "tokens": resp["usage"]["completion_tokens"],
                        "ok": True,
                    }
                last_err = f"invalid scores: {scores}"
            except Exception as e:
                last_err = str(e)[:200]
            await asyncio.sleep(0.5 * (attempt + 1))
        return {
            "id": pair_id,
            "source_tag": sample.get("__source_tag__"),
            "ok": False,
            "error": last_err,
            "latency_s": round(time.time() - t0, 2),
        }


def load_corpus(path: Path):
    out = []
    with open(path) as f:
        for i, line in enumerate(f):
            if not line.strip():
                continue
            r = json.loads(line)
            r["__row__"] = i
            out.append(r)
    return out


def load_already_scored(path: Path):
    if not path.exists():
        return set()
    done = set()
    with open(path) as f:
        for line in f:
            try:
                r = json.loads(line)
                if r.get("ok"):
                    done.add(r["id"])
            except Exception:
                continue
    return done


async def main():
    p = argparse.ArgumentParser()
    p.add_argument("--corpus", default=str(DEFAULT_CORPUS))
    p.add_argument("--out", default=str(DEFAULT_OUT))
    p.add_argument("--concurrency", type=int, default=32)
    p.add_argument("--limit", type=int, default=0)
    p.add_argument("--resume", action="store_true")
    p.add_argument("--report-every", type=int, default=500)
    args = p.parse_args()

    corpus = load_corpus(Path(args.corpus))
    print(f"loaded {len(corpus):,} pairs from {args.corpus}")

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    done = load_already_scored(out_path) if args.resume else set()
    if done:
        print(f"resume: {len(done):,} already scored, skipping")
        corpus = [r for r in corpus if r.get("id") not in done]
        print(f"  {len(corpus):,} remaining")

    if args.limit:
        corpus = corpus[: args.limit]
        print(f"limit: only scoring first {len(corpus):,}")

    sem = asyncio.Semaphore(args.concurrency)
    mode = "a" if args.resume else "w"

    t_start = time.time()
    completed = 0
    ok_count = 0
    err_count = 0
    tier_counts = {t: 0 for t in ("APEX", "HONEY", "JELLY", "POLLEN", "PROPOLIS")}

    async with httpx.AsyncClient() as client:
        tasks = [asyncio.create_task(score_one(client, r, sem)) for r in corpus]
        with open(out_path, mode) as f:
            for fut in asyncio.as_completed(tasks):
                result = await fut
                f.write(json.dumps(result, ensure_ascii=False) + "\n")
                f.flush()
                completed += 1
                if result.get("ok"):
                    ok_count += 1
                    tier_counts[result["tier"]] += 1
                else:
                    err_count += 1

                if completed % args.report_every == 0 or completed == len(corpus):
                    elapsed = time.time() - t_start
                    rate = completed / elapsed
                    eta = (len(corpus) - completed) / rate if rate > 0 else 0
                    print(
                        f"  [{completed:>6,}/{len(corpus):,}] {rate:.1f}/s  ETA {eta/60:.1f}m  "
                        f"ok={ok_count} err={err_count}  "
                        f"APEX={tier_counts['APEX']} HONEY={tier_counts['HONEY']} "
                        f"JELLY={tier_counts['JELLY']} POLLEN={tier_counts['POLLEN']} PROPOLIS={tier_counts['PROPOLIS']}"
                    )

    elapsed = time.time() - t_start
    print()
    print("=" * 72)
    print(f"DONE — {ok_count:,} scored / {err_count} errors in {elapsed/60:.1f}m  ({ok_count/elapsed:.1f} pairs/sec)")
    print("=" * 72)
    print(f"  APEX     (9-10): {tier_counts['APEX']:>6,}  ({100*tier_counts['APEX']/max(ok_count,1):.1f}%)")
    print(f"  HONEY    (7-8 ): {tier_counts['HONEY']:>6,}  ({100*tier_counts['HONEY']/max(ok_count,1):.1f}%)")
    print(f"  JELLY    (5-6 ): {tier_counts['JELLY']:>6,}  ({100*tier_counts['JELLY']/max(ok_count,1):.1f}%)")
    print(f"  POLLEN   (3-4 ): {tier_counts['POLLEN']:>6,}  ({100*tier_counts['POLLEN']/max(ok_count,1):.1f}%)")
    print(f"  PROPOLIS (1-2 ): {tier_counts['PROPOLIS']:>6,}  ({100*tier_counts['PROPOLIS']/max(ok_count,1):.1f}%)")
    jellyplus = tier_counts["APEX"] + tier_counts["HONEY"] + tier_counts["JELLY"]
    print(f"  JELLY+ (cook-eligible): {jellyplus:,}  ({100*jellyplus/max(ok_count,1):.1f}%)")
    print(f"  Output: {out_path}")


if __name__ == "__main__":
    asyncio.run(main())
