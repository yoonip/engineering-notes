"""국립국어원 2025 묵자-점자 자료를 읽기 전용으로 읽어 학습 JSONL을 만듭니다.

실행 예:
  python -X utf8 prepare_data.py --raw-dir data/raw/nikl

원시 JSON source는 묵자, target은 점자입니다. revision.revision1 검수본을
우선 사용하며 결과에는 명확한 braille/korean 키를 씁니다. 원문은 NFC 외
수정하지 않습니다. 중복 탐지에만 별도 정규화 키를 사용합니다.
GPU 학습이나 길이 제한에 따른 제외는 이 스크립트에서 수행하지 않습니다.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys
import unicodedata


ROOT = Path(__file__).resolve().parent
CATEGORIES = {"I": "인터넷 기반 신문", "L": "지역 종합지", "P": "전문지", "W": "전국 종합지"}
SPLIT_NAMES = ("train", "validation", "test")
SCHEMA_VERSION = 1


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".partial")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def normalized_korean_key(text: str) -> str:
    """누수 방지용 보수적 키. 저장하거나 모델에 입력할 텍스트가 아닙니다."""
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def normalized_braille_key(text: str) -> str:
    """빈 점자 셀과 공백 변형도 같은 중복 그룹에 묶습니다."""
    return " ".join(unicodedata.normalize("NFC", text).replace("\u2800", " ").split())


def document_id_from_original(original_id: str) -> str:
    # 설명서는 original_id를 원자료 문장 ID라고만 정의합니다.
    # 세 부분 ID의 마지막 문장 번호를 제거한 상위 단위를 문서 그룹으로 사용합니다.
    # 이 해석은 공개 파일 구조에 대한 운영상 추정이며 공식 내부 계층 정의가 아닙니다.
    if not re.fullmatch(r"[A-Z]+\d+\.\d+\.\d+", original_id):
        raise ValueError("original_id must have corpus.article.sentence form")
    return original_id.rsplit(".", 1)[0]


class DisjointSet:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, value: int) -> int:
        while self.parent[value] != value:
            self.parent[value] = self.parent[self.parent[value]]
            value = self.parent[value]
        return value

    def union(self, left: int, right: int) -> bool:
        left, right = self.find(left), self.find(right)
        if left == right:
            return False
        if self.size[left] < self.size[right]:
            left, right = right, left
        self.parent[right] = left
        self.size[left] += self.size[right]
        return True


def length_stats(values: list[int]) -> dict:
    if not values:
        return {"count": 0}
    values = sorted(values)
    stats = {"count": len(values), "mean": round(sum(values) / len(values), 3)}
    for q in (0, 25, 50, 75, 90, 95, 99, 100):
        stats[f"p{q}"] = values[round((len(values) - 1) * q / 100)]
    return stats


def text_stats(rows: list[dict]) -> dict:
    source_chars = Counter()
    target_chars = Counter()
    korean_nfd = Counter()
    for row in rows:
        source_chars.update(row["braille"])
        target_chars.update(row["korean"])
        korean_nfd.update(unicodedata.normalize("NFD", row["korean"]))
    return {
        "rows": len(rows),
        "categories": dict(sorted(Counter(r["category_code"] for r in rows).items())),
        "documents": len({r["document_id"] for r in rows}),
        "korean_eojeol": sum(len(r["korean"].split()) for r in rows),
        "lengths_without_special_tokens": {
            "braille": length_stats([len(r["braille"]) for r in rows]),
            "korean_nfc": length_stats([len(r["korean"]) for r in rows]),
            "korean_nfd": length_stats([len(unicodedata.normalize("NFD", r["korean"])) for r in rows]),
        },
        "unique_characters": {"braille": len(source_chars), "korean_nfc": len(target_chars), "korean_nfd": len(korean_nfd)},
        "braille_codepoints": [f"U+{ord(c):04X}" for c in sorted(source_chars)],
        "whitespace": {
            "braille": {f"U+{ord(c):04X}": n for c, n in sorted(source_chars.items()) if c.isspace()},
            "korean": {f"U+{ord(c):04X}": n for c, n in sorted(target_chars.items()) if c.isspace()},
        },
        "leading_or_trailing_whitespace_rows": {
            field: sum(r[field] != r[field].strip() for r in rows) for field in ("braille", "korean")
        },
        "consecutive_ascii_space_rows": {
            field: sum("  " in r[field] for r in rows) for field in ("braille", "korean")
        },
    }


def read_corpus(raw_dir: Path):
    paths = sorted(raw_dir.glob("N?PAKOKB25*.json"))
    if not paths:
        raise FileNotFoundError(f"2025 JSON 파일을 찾지 못했습니다: {raw_dir}")
    rows, excluded, files = [], [], []
    ids = {}
    for path in paths:
        category_code = path.name[1]
        if category_code not in CATEGORIES:
            raise ValueError(f"알 수 없는 파일 범주: {path.name}")
        raw_hash = sha256(path)
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
        if payload.get("language_info") != {"source_language": "ko", "target_language": "kb"}:
            raise ValueError(f"언어 정보가 예상 ko/kb와 다릅니다: {path.name}")
        if not isinstance(payload.get("parallel"), list):
            raise ValueError(f"parallel 배열이 없습니다: {path.name}")
        counters = Counter()
        differences = []
        file_rows = []
        for index, raw in enumerate(payload["parallel"]):
            counters["raw_rows"] += 1
            reason = None
            if not isinstance(raw, dict):
                raw = {}
                reason = "row_not_object"
            sentence_id = raw.get("id")
            original_id = raw.get("original_id")
            korean = raw.get("source")
            revision = raw.get("revision")
            revised = revision.get("revision1") if isinstance(revision, dict) else None
            if isinstance(revised, str) and revised.strip():
                braille = revised
                braille_field = "revision.revision1"
                counters["revision1_selected"] += 1
                if revised != raw.get("target"):
                    counters["revision1_differs_from_target"] += 1
                    differences.append({"id": sentence_id, "target_sha256": hashlib.sha256(str(raw.get("target")).encode()).hexdigest(),
                                        "revision1_sha256": hashlib.sha256(revised.encode()).hexdigest()})
            else:
                braille = raw.get("target")
                braille_field = "target"
                counters["revision1_missing_or_empty_fallback_target"] += 1
            if not reason and (not isinstance(sentence_id, str) or not sentence_id or not isinstance(original_id, str)):
                reason = "missing_id"
            if not reason and (not isinstance(korean, str) or not isinstance(braille, str)):
                reason = "text_not_string"
            if not reason and (not korean.strip() or not braille.strip()):
                reason = "empty_text"
            if not reason:
                try:
                    document_id = document_id_from_original(original_id)
                except ValueError:
                    reason = "unrecognized_original_id_structure"
            if not reason and any(not ("\u2800" <= char <= "\u283f" or char == " ") for char in braille):
                reason = "braille_not_six_dot_or_ascii_space"
            if not reason and any(unicodedata.category(char) in {"Cc", "Cs", "Cf"} for char in korean):
                reason = "korean_control_or_format_character"
            if reason:
                excluded.append({"raw_file": path.name, "raw_index": index, "id": sentence_id, "reason": reason})
                counters["excluded_" + reason] += 1
                continue
            normalized_korean = unicodedata.normalize("NFC", korean)
            normalized_braille = unicodedata.normalize("NFC", braille)
            counters["korean_nfc_changed"] += normalized_korean != korean
            counters["braille_nfc_changed"] += normalized_braille != braille
            if sentence_id in ids:
                # 동일 ID의 서로 다른 내용을 조용히 선택하지 않습니다.
                raise ValueError(f"중복 id가 있습니다: {sentence_id}, {ids[sentence_id]}, {path.name}")
            ids[sentence_id] = path.name
            row = {"id": sentence_id, "original_id": original_id, "document_id": document_id,
                   "category": CATEGORIES[category_code], "category_code": category_code,
                   "braille": normalized_braille, "korean": normalized_korean,
                   "braille_field": braille_field, "raw_file": path.name}
            rows.append(row)
            file_rows.append(row)
            counters["valid_rows_before_dedup"] += 1
        files.append({"file": path.name, "path": str(path), "bytes": path.stat().st_size, "sha256": raw_hash,
                      "category_code": category_code, "category": CATEGORIES[category_code],
                      "language_info": payload["language_info"], "counters": dict(counters),
                      "revision_difference_records": differences, "statistics": text_stats(file_rows)})
        print(f"읽음: {path.name}: {counters['raw_rows']:,}행 / 유효 {len(file_rows):,}", flush=True)
    return rows, excluded, files


def connect_groups(rows: list[dict]):
    dsu = DisjointSet(len(rows))
    seen = {key: {} for key in ("document", "original_id", "korean", "braille")}
    union_counts = Counter()
    ambiguous_braille = defaultdict(set)
    ambiguous_korean = defaultdict(set)
    for index, row in enumerate(rows):
        korean_key = normalized_korean_key(row["korean"])
        braille_key = normalized_braille_key(row["braille"])
        keys = {"document": row["document_id"], "original_id": row["original_id"], "korean": korean_key, "braille": braille_key}
        ambiguous_braille[braille_key].add(korean_key)
        ambiguous_korean[korean_key].add(braille_key)
        for kind, key in keys.items():
            if key in seen[kind]:
                if dsu.union(index, seen[kind][key]):
                    union_counts[kind] += 1
            else:
                seen[kind][key] = index
    members = defaultdict(list)
    for index in range(len(rows)):
        members[dsu.find(index)].append(index)
    groups, duplicate_records = [], []
    for indices in members.values():
        # 그룹 이름은 입력 행 순서/DSU 루트에 의존하지 않습니다.
        member_ids = sorted(rows[index]["id"] for index in indices)
        group_id = "g_" + hashlib.sha256("\n".join(member_ids).encode("utf-8")).hexdigest()[:24]
        kept, exact_pairs = [], {}
        for index in sorted(indices, key=lambda i: rows[i]["id"]):
            row = rows[index]
            pair = (row["braille"], row["korean"])
            if pair in exact_pairs:
                duplicate_records.append({"id": row["id"], "raw_file": row["raw_file"], "reason": "exact_pair_duplicate",
                                          "duplicate_of": exact_pairs[pair], "group": group_id})
                continue
            exact_pairs[pair] = row["id"]
            row["group"] = group_id
            kept.append(row)
        groups.append({"id": group_id, "rows": kept, "raw_member_count": len(indices),
                       "categories": Counter(row["category_code"] for row in kept),
                       "all_document_ids": sorted({rows[i]["document_id"] for i in indices})})
    ambiguity = {
        "normalized_braille_with_multiple_normalized_korean": sum(len(values) > 1 for values in ambiguous_braille.values()),
        "normalized_korean_with_multiple_normalized_braille": sum(len(values) > 1 for values in ambiguous_korean.values()),
        "action": "Conflicting variants are kept in one group; no arbitrary target is selected.",
    }
    return groups, duplicate_records, dict(union_counts), ambiguity


def assign_splits(groups: list[dict], ratios: dict[str, float], seed: int):
    total = sum(len(group["rows"]) for group in groups)
    category_totals = sum((group["categories"] for group in groups), Counter())
    counts = Counter()
    by_category = {split: Counter() for split in SPLIT_NAMES}
    result = {split: [] for split in SPLIT_NAMES}
    group_assignments, forced_train = {}, []
    targets = {split: total * ratios[split] for split in SPLIT_NAMES}
    category_targets = {split: {c: n * ratios[split] for c, n in category_totals.items()} for split in SPLIT_NAMES}
    ordered = sorted(groups, key=lambda g: (-len(g["rows"]), hashlib.sha256(f"{seed}:{g['id']}".encode()).hexdigest()))
    for group in ordered:
        size = len(group["rows"])
        if size > min(targets["validation"], targets["test"]):
            chosen = "train"
            forced_train.append({"group": group["id"], "rows": size})
        else:
            def cost(split):
                # 행 수와 범주 구성에 대한 정규화 제곱 오차 증가량을 최소화합니다.
                score = (size * size + 2 * size * (counts[split] - targets[split])) / max(targets[split], 1)
                for category, number in group["categories"].items():
                    target = category_targets[split][category]
                    score += (number * number + 2 * number * (by_category[split][category] - target)) / max(target, 1)
                return score, SPLIT_NAMES.index(split)
            chosen = min(SPLIT_NAMES, key=cost)
        counts[chosen] += size
        by_category[chosen].update(group["categories"])
        result[chosen].extend(group["rows"])
        group_assignments[group["id"]] = chosen
    for split, values in result.items():
        values.sort(key=lambda row: hashlib.sha256(f"{seed}:{split}:{row['id']}".encode()).hexdigest())
    if any(not result[split] for split in SPLIT_NAMES):
        raise RuntimeError("그룹을 유지한 채 세 분할을 만들 수 없습니다. 그룹 크기를 확인하세요.")
    return result, group_assignments, forced_train


def audit_overlap(splits: dict[str, list[dict]]) -> dict:
    getters = {"id": lambda r: r["id"], "original_id": lambda r: r["original_id"],
               "document_id": lambda r: r["document_id"], "group": lambda r: r["group"],
               "normalized_braille": lambda r: normalized_braille_key(r["braille"]),
               "normalized_korean": lambda r: normalized_korean_key(r["korean"])}
    audit = {}
    for label, getter in getters.items():
        sets = {split: {getter(row) for row in values} for split, values in splits.items()}
        audit[label] = {f"{a}__{b}": len(sets[a] & sets[b]) for a, b in (("train", "validation"), ("train", "test"), ("validation", "test"))}
        if any(audit[label].values()):
            raise RuntimeError(f"분할 사이 중복이 발견되었습니다: {label}, {audit[label]}")
    return audit


def make_vocab(splits: dict[str, list[dict]]) -> dict:
    transforms = {"braille_chars": lambda r: r["braille"], "korean_chars": lambda r: r["korean"],
                  "korean_nfd_chars": lambda r: unicodedata.normalize("NFD", r["korean"])}
    vocab = {"schema_version": SCHEMA_VERSION, "built_from": "train only", "special_tokens": ["<pad>", "<bos>", "<eos>", "<unk>"],
             "token_id_assignment": "모델 코드가 특수 토큰 뒤에 아래 정렬된 문자 목록을 붙여 ID를 정합니다.",
             "korean_nfd_policy": "unicodedata.normalize('NFD', korean); 출력 복원은 NFC; 원 JSONL은 NFC 보존"}
    oov = {}
    for name, transform in transforms.items():
        counts = Counter()
        for row in splits["train"]:
            counts.update(transform(row))
        vocab[name] = sorted(counts)
        vocab[name + "_counts"] = dict(sorted(counts.items()))
        oov[name] = {}
        for split in ("validation", "test"):
            unknown = Counter()
            affected = 0
            total_tokens = 0
            for row in splits[split]:
                text = transform(row)
                missing = [char for char in text if char not in counts]
                affected += bool(missing)
                unknown.update(missing)
                total_tokens += len(text)
            oov[name][split] = {"affected_rows": affected, "unknown_tokens": sum(unknown.values()),
                                "total_tokens": total_tokens, "characters": dict(sorted(unknown.items()))}
    vocab["heldout_oov_audit"] = oov
    return vocab


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "data/processed")
    parser.add_argument("--manifest", type=Path, default=ROOT / "data_manifest.json")
    parser.add_argument("--seed", type=int, default=20261006)
    parser.add_argument("--validation-ratio", type=float, default=0.1)
    parser.add_argument("--test-ratio", type=float, default=0.1)
    parser.add_argument("--force", action="store_true", help="기존 생성물만 다시 씁니다. 원본은 수정하지 않습니다.")
    args = parser.parse_args()
    raw_dir, output_dir, manifest_path = args.raw_dir.resolve(), args.output_dir.resolve(), args.manifest.resolve()
    if not raw_dir.is_dir():
        parser.error(f"원본 폴더가 없습니다: {raw_dir}")
    if output_dir == raw_dir or raw_dir in output_dir.parents or manifest_path == raw_dir or raw_dir in manifest_path.parents:
        parser.error("원본 자료 폴더 안에는 생성물을 쓰지 않습니다.")
    if not (0 < args.validation_ratio < 1 and 0 < args.test_ratio < 1 and args.validation_ratio + args.test_ratio < 1):
        parser.error("validation/test 비율은 각각 양수이며 합이 1보다 작아야 합니다.")
    generated_names = [*(f"{split}.jsonl" for split in SPLIT_NAMES), "vocab_train.json", "excluded.jsonl", "groups.jsonl"]
    existing = [output_dir / name for name in generated_names if (output_dir / name).exists()]
    if (existing or manifest_path.exists()) and not args.force:
        parser.error("기존 생성물이 있습니다. 재현 실행은 --force 또는 다른 --output-dir/--manifest를 사용하세요.")
    ratios = {"train": 1 - args.validation_ratio - args.test_ratio, "validation": args.validation_ratio, "test": args.test_ratio}
    rows, exclusions, raw_files = read_corpus(raw_dir)
    if not rows:
        raise RuntimeError("유효한 문장쌍이 없습니다.")
    raw_valid_stats = text_stats(rows)
    groups, duplicates, unions, ambiguity = connect_groups(rows)
    exclusions.extend(duplicates)
    splits, assignments, forced_train = assign_splits(groups, ratios, args.seed)
    overlap = audit_overlap(splits)
    vocab = make_vocab(splits)
    output_dir.mkdir(parents=True, exist_ok=True)
    outputs = {}
    for split, values in splits.items():
        path = output_dir / f"{split}.jsonl"
        temporary = path.with_suffix(".jsonl.partial")
        with temporary.open("w", encoding="utf-8", newline="\n") as handle:
            for row in values:
                handle.write(json.dumps(row, ensure_ascii=False) + "\n")
        temporary.replace(path)
        outputs[split] = {"path": str(path), "sha256": sha256(path), "bytes": path.stat().st_size,
                          "groups": len({r["group"] for r in values}), "statistics": text_stats(values)}
        print(f"저장: {split} {len(values):,}행 / {outputs[split]['groups']:,}그룹", flush=True)
    write_json(output_dir / "vocab_train.json", vocab)
    with (output_dir / "excluded.jsonl").open("w", encoding="utf-8", newline="\n") as handle:
        for row in exclusions:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    with (output_dir / "groups.jsonl").open("w", encoding="utf-8", newline="\n") as handle:
        for group in sorted(groups, key=lambda g: g["id"]):
            record = {"group": group["id"], "split": assignments[group["id"]], "rows": len(group["rows"]),
                      "raw_member_count": group["raw_member_count"], "categories": dict(group["categories"]),
                      "document_ids": group["all_document_ids"]}
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    # 읽기 전후 원본 해시를 비교해 실행 중 원본이 바뀌지 않았는지 확인합니다.
    unchanged = all(sha256(Path(record["path"])) == record["sha256"] for record in raw_files)
    if not unchanged:
        raise RuntimeError("실행 중 원본 파일이 바뀌었습니다. 이 생성물을 학습에 사용하지 마세요.")
    manuals = [{"file": p.name, "path": str(p), "bytes": p.stat().st_size, "sha256": sha256(p)} for p in sorted(raw_dir.glob("*.pdf"))]
    counts = {split: len(values) for split, values in splits.items()}
    manifest = {
        "schema_version": SCHEMA_VERSION, "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "preprocessor": {"path": str(Path(__file__).resolve()), "sha256": sha256(Path(__file__)), "python": sys.version},
        "raw_source_dir": str(raw_dir), "raw_files_unchanged": unchanged, "raw_files": raw_files, "manuals": manuals,
        "corpus": {"title": "국립국어원 묵자-점자 병렬 말뭉치 2025", "version": "1.0", "release_date": "2026-06-30",
                   "manual_reported_sentences": 83528, "manual_reported_eojeol": 1675580,
                   "braille_rules": "한국 점자 규정(2024)", "domain": "신문 기사에서 선정한 한글·로마자·숫자·기호 혼합 문장",
                   "citation": "국립국어원(2025). 국립국어원 묵자-점자 병렬 말뭉치 2025(버전 1.0). https://kli.korean.go.kr/corpus",
                   "use_conditions": "원자료와 학습 가중치는 이 소스 패키지에 포함되지 않습니다."},
        "rights": {"raw_redistribution": "전처리 출력은 로컬 자료이며 공개 패키지에서 제외됩니다.",
                   "model_distribution": "자료 제공기관의 이용 약정에 따라 별도로 확인합니다."},
        "schema": {"id": "원본 병렬 문장 ID", "original_id": "원자료 문장 ID", "document_id": "original_id의 마지막 .번호를 제거한 상위 단위(운영상 추정)",
                   "group": "문서와 동일 입력/정답을 연결한 분할 단위", "category": "국문 매체 범주", "category_code": "I/L/P/W",
                   "braille": "검수본 revision.revision1 우선, 없으면 target", "korean": "원본 source의 NFC", "braille_field": "선택한 원본 필드", "raw_file": "원본 JSON 이름"},
        "normalization": {"saved_text": "NFC only; whitespace, punctuation, case preserved; no strip, truncation or sentence segmentation",
                          "korean_group_key": "NFKC + casefold + whitespace collapse", "braille_group_key": "NFC + U+2800→space + whitespace collapse",
                          "length_policy": "길이 제한 없음. 모델 학습 시 별도 필터 개수·ID를 기록해야 합니다."},
        "raw_valid_statistics": raw_valid_stats,
        "filtering": {"raw_rows": sum(f["counters"]["raw_rows"] for f in raw_files), "valid_before_dedup": len(rows),
                      "retained": sum(counts.values()), "excluded": len(exclusions), "reasons": dict(Counter(e["reason"] for e in exclusions)),
                      "records_path": str(output_dir / "excluded.jsonl"), "long_sentence_filtering": False},
        "split": {"seed": args.seed, "ratios_requested": ratios, "counts": counts, "ratios_actual": {s: n / sum(counts.values()) for s, n in counts.items()},
                  "method": "문서/원자료ID/정규화묵자/정규화점자 연결요소를 분리하지 않고 행수와 범주 분포를 탐욕적 최소오차 배정",
                  "document_id_caveat": "설명서는 문장 ID 내부 계층을 정의하지 않습니다. corpus.article.sentence로 읽어 마지막 단위를 제거한 보수적 운영 그룹입니다.",
                  "groups": len(groups), "group_size_statistics": length_stats([len(g["rows"]) for g in groups]),
                  "largest_groups": [{"group": g["id"], "rows": len(g["rows"]), "documents": len(g["all_document_ids"])} for g in sorted(groups, key=lambda g: -len(g["rows"]))[:10]],
                  "union_operations": unions, "forced_large_groups_to_train": forced_train, "overlap_audit": overlap,
                  "limitations": "정의한 ID/문자정규화 중복만 방지합니다. 근접 문장·동일 사건·출처 매체·시간 분포의 완전 독립성을 보장하지 않습니다."},
        "ambiguity_audit": ambiguity, "outputs": outputs,
        "vocabulary": {"path": str(output_dir / "vocab_train.json"), "sha256": sha256(output_dir / "vocab_train.json"), "built_from": "train only",
                       "sizes_without_special_tokens": {name: len(vocab[name]) for name in ("braille_chars", "korean_chars", "korean_nfd_chars")},
                       "heldout_oov_audit": vocab["heldout_oov_audit"]},
    }
    write_json(manifest_path, manifest)
    print(json.dumps({"counts": counts, "excluded": len(exclusions), "groups": len(groups),
                      "largest_group": max(len(g["rows"]) for g in groups), "overlaps": overlap,
                      "vocabulary": manifest["vocabulary"]["sizes_without_special_tokens"], "manifest": str(manifest_path)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
