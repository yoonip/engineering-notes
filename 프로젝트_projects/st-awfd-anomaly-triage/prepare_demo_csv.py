"""공개 D2에서 정답 열을 제외한 Step 1 예제 CSV를 만든다."""
from pathlib import Path
import csv
import io
import zipfile

ROOT = Path(__file__).resolve().parent


def prepare_demo(archive_path: Path, output_path: Path, group_count: int = 20) -> int:
    features = [f"feature_{index}" for index in range(1, 21)]
    fields = ["MaterialID", "StepID", "duration_ms", *features]
    identifiers = set()
    rows = []
    with zipfile.ZipFile(archive_path) as archive:
        members = [name for name in archive.namelist() if Path(name).name.lower() == "d2.csv"]
        if len(members) != 1:
            raise ValueError("D2.zip 안에 D2.csv 하나가 필요합니다.")
        with archive.open(members[0]) as raw:
            source = csv.DictReader(io.TextIOWrapper(raw, encoding="utf-8-sig"))
            if not set(fields + ["is_test"]).issubset(source.fieldnames or []):
                raise ValueError("공식 D2 입력 열이 일치하지 않습니다.")
            for row in source:
                if float(row["is_test"]) != 1 or float(row["StepID"]) != 1:
                    continue
                identifier = row["MaterialID"]
                if identifier not in identifiers and len(identifiers) < group_count:
                    identifiers.add(identifier)
                if identifier in identifiers:
                    rows.append({field: row[field] for field in fields})
    if len(identifiers) != group_count:
        raise ValueError(f"Step 1 예제 lot {group_count}개가 필요합니다: {len(identifiers)}개 발견")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    return len(rows)


if __name__ == "__main__":
    destination = ROOT / "results/st_awfd/st_awfd_label_free_demo_input.csv"
    count = prepare_demo(ROOT / "data/st_awfd/D2.zip", destination)
    print(f"{count} rows -> {destination}")
