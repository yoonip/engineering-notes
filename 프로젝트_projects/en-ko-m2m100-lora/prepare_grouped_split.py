"""문장 ID 또는 정규화한 문장이 같으면 한 묶음으로 분할합니다.

기존 파일을 덮어쓰지 않습니다. 번역쌍을 단순 무작위로 나누면 같은 원문이
학습과 시험에 동시에 들어갈 수 있습니다. 이 스크립트는 연결된 모든 쌍을
하나의 그룹으로 묶고 그룹 전체를 한 split에만 넣습니다.
"""
from pathlib import Path
import argparse
import csv
import hashlib
import json
import random
import unicodedata

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "data/processed/tatoeba_en_ko"
DEST = ROOT / "data/processed/tatoeba_en_ko_grouped_v1"
SEED = 20261004


def normalize(text):
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    global SOURCE, DEST
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=SOURCE)
    parser.add_argument("--dest", type=Path, default=DEST)
    args = parser.parse_args()
    SOURCE, DEST = args.source.resolve(), args.dest.resolve()
    if DEST.exists():
        raise RuntimeError(f"분할을 고정하기 위해 기존 폴더를 덮어쓰지 않습니다: {DEST}")
    rows = []
    for name in ("train", "validation", "test"):
        with (SOURCE / f"{name}.tsv").open(encoding="utf-8", newline="") as handle:
            rows.extend(csv.DictReader(handle, delimiter="\t"))
    if not rows:
        raise ValueError("No rows to split")
    for row in rows:
        if any(not row.get(k, "").strip() for k in ("source_id", "target_id", "source", "target")):
            raise ValueError("Non-empty source_id, target_id, source and target columns are required")
    parent = list(range(len(rows)))

    def find(index):
        while parent[index] != index:
            parent[index] = parent[parent[index]]
            index = parent[index]
        return index

    seen = {}
    for index, row in enumerate(rows):
        keys = [
            ("source_text", normalize(row["source"])),
            ("target_text", normalize(row["target"])),
            ("source_id", row["source_id"]),
            ("target_id", row["target_id"]),
        ]
        for key in keys:
            if key in seen:
                parent[find(index)] = find(seen[key])
            else:
                seen[key] = index
    groups = {}
    for index, row in enumerate(rows):
        groups.setdefault(find(index), []).append(row)
    ordered = list(groups.values())
    random.Random(SEED).shuffle(ordered)
    splits = {"train": [], "validation": [], "test": []}
    for group in ordered:
        if len(splits["train"]) < round(len(rows) * .8):
            split = "train"
        elif len(splits["validation"]) < round(len(rows) * .1):
            split = "validation"
        else:
            split = "test"
        splits[split].extend(group)
    overlap = {}
    names = list(splits)
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            for side in ("source", "target"):
                sa = {normalize(row[side]) for row in splits[a]}
                sb = {normalize(row[side]) for row in splits[b]}
                overlap[f"{a}_{b}_{side}"] = len(sa & sb)
    assert not any(overlap.values()), overlap
    DEST.mkdir(parents=True)
    for name, values in splits.items():
        with (DEST / f"{name}.tsv").open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=["source_id", "target_id", "source", "target"], delimiter="\t")
            writer.writeheader()
            writer.writerows(values)
    manifest = {
        "seed": SEED,
        "method": "Connected components over source/target sentence IDs and NFKC-casefold-whitespace-normalized text, whole-component 80/10/10 split",
        "examples": {key: len(value) for key, value in splits.items()},
        "total": len(rows), "groups": len(groups),
        "largest_group": max(map(len, groups.values())),
        "normalized_overlap": overlap,
        "sha256": {name: digest(DEST / f"{name}.tsv") for name in splits},
        "source_files": {name: digest(SOURCE / f"{name}.tsv") for name in splits},
        "limits": "Exact ID/text overlap is blocked. Paraphrases, related topics, and unknown original M2M100 pretraining overlap are not removed.",
    }
    (DEST / "split_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
