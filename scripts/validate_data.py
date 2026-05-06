import json
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "official_600_questions_2025_extracted.json"
EXPECTED = {1: 180, 2: 25, 3: 58, 4: 37, 5: 185, 6: 115}

def main():
    data = json.loads(DATA.read_text(encoding="utf-8"))
    print("Total:", len(data))
    ids = [q.get("id") for q in data]
    missing = [i for i in range(1, 601) if i not in set(ids)]
    dup = sorted({x for x in ids if ids.count(x) > 1})
    print("Missing IDs:", missing[:20], "count=", len(missing))
    print("Duplicate IDs:", dup[:20], "count=", len(dup))
    print("Answered:", sum(1 for q in data if q.get("answer_index") and q.get("answer")))
    print("Critical marked:", sum(1 for q in data if q.get("is_critical")))
    counts = Counter(int(q.get("chapter") or 0) for q in data)
    print("Chapter counts:", dict(counts))
    ok = len(data) == 600 and not missing and not dup and all(counts.get(k, 0) == v for k, v in EXPECTED.items())
    print("OK" if ok else "NEEDS_REVIEW")
    return 0 if ok else 1

if __name__ == "__main__":
    raise SystemExit(main())
