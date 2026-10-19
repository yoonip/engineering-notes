"""Download Tatoeba's public EN-KO sentence links and make fixed splits.

No sentence data is included in this source package. The local split files
preserve IDs; dataset terms and attribution remain separate from code.
"""

from __future__ import annotations

import argparse
import bz2
import csv
import random
import tarfile
from pathlib import Path

import requests


ROOT = Path(__file__).resolve().parent
RAW = ROOT / "data" / "raw" / "tatoeba"
PROCESSED = ROOT / "data" / "processed" / "tatoeba_en_ko"
BASE = "https://downloads.tatoeba.org/exports"
FILES = {
    "eng": f"{BASE}/per_language/eng/eng_sentences.tsv.bz2",
    "kor": f"{BASE}/per_language/kor/kor_sentences.tsv.bz2",
    "links": f"{BASE}/links.tar.bz2",
}


def download(url: str, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists() and destination.stat().st_size:
        print(f"Using cached {destination.name} ({destination.stat().st_size:,} bytes)")
        return
    temporary = destination.with_suffix(destination.suffix + ".part")
    print(f"Downloading {url}")
    with requests.get(url, stream=True, timeout=(30, 180)) as response:
        response.raise_for_status()
        total = int(response.headers.get("content-length", "0"))
        received = 0
        with temporary.open("wb") as output:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    output.write(chunk)
                    received += len(chunk)
                    if total:
                        print(f"\r  {received / total:6.1%}", end="", flush=True)
    if total and received != total:
        temporary.unlink(missing_ok=True)
        raise IOError(f"Incomplete download: expected {total}, received {received}")
    temporary.replace(destination)
    print(f"\nSaved {destination.name} ({received:,} bytes)")


def read_sentences(path: Path, expected_language: str) -> dict[int, str]:
    result: dict[int, str] = {}
    with bz2.open(path, "rt", encoding="utf-8", errors="replace") as source:
        for line in source:
            fields = line.rstrip("\n").split("\t", 2)
            if len(fields) != 3:
                continue
            try:
                sentence_id = int(fields[0])
            except ValueError:
                continue
            if fields[1] == expected_language and fields[2].strip():
                result[sentence_id] = fields[2].strip()
    return result


def iter_link_rows(path: Path):
    """Read the single TSV member from Tatoeba's compressed link archive."""
    found_file = False
    with tarfile.open(path, mode="r|bz2") as archive:
        for member in archive:
            if not member.isfile():
                continue
            found_file = True
            handle = archive.extractfile(member)
            if handle is None:
                continue
            while True:
                line = handle.readline()
                if not line:
                    break
                columns = line.rstrip(b"\r\n").split(b"\t")
                if len(columns) < 2:
                    continue
                try:
                    yield int(columns[0]), int(columns[1])
                except ValueError:
                    continue
    if not found_file:
        raise ValueError("Tatoeba links archive contained no regular files")


def build_pairs(english: dict[int, str], korean: dict[int, str], links: Path):
    pairs: dict[tuple[int, int], tuple[str, str]] = {}
    for left, right in iter_link_rows(links):
        if left in english and right in korean:
            pairs[(left, right)] = (english[left], korean[right])
        elif right in english and left in korean:
            pairs[(right, left)] = (english[right], korean[left])
    return pairs


def write_splits(pairs, seed: int = 20261003) -> None:
    rows = []
    seen_text_pairs = set()
    for (en_id, ko_id), (source, target) in pairs.items():
        # Remove empty/noisy and duplicate text pairs while retaining first IDs.
        if not source or not target or source.casefold() == target.casefold():
            continue
        if len(source) > 500 or len(target) > 500:
            continue
        normalized_pair = (source.casefold(), target.casefold())
        if normalized_pair in seen_text_pairs:
            continue
        seen_text_pairs.add(normalized_pair)
        rows.append((en_id, ko_id, source, target))
    rows.sort(key=lambda row: (row[0], row[1]))
    random.Random(seed).shuffle(rows)
    if len(rows) < 20:
        raise RuntimeError(f"Only {len(rows)} usable pairs found; inspect source exports")

    n = len(rows)
    train_end = max(1, int(n * 0.8))
    validation_end = max(train_end + 1, int(n * 0.9))
    splits = {
        "train": rows[:train_end],
        "validation": rows[train_end:validation_end],
        "test": rows[validation_end:],
    }
    PROCESSED.mkdir(parents=True, exist_ok=True)
    for name, subset in splits.items():
        with (PROCESSED / f"{name}.tsv").open("w", encoding="utf-8", newline="") as output:
            writer = csv.writer(output, delimiter="\t", lineterminator="\n")
            writer.writerow(("source_id", "target_id", "source", "target"))
            writer.writerows(subset)
    print(f"Usable unique EN-KO pairs: {n:,}")
    print("Split sizes: " + ", ".join(f"{name}={len(part):,}" for name, part in splits.items()))
    print(f"Wrote splits to {PROCESSED}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--download", action="store_true", help="Explicitly allow the large official export downloads")
    args = parser.parse_args()
    if PROCESSED.exists():
        raise FileExistsError("Processed splits already exist; refusing to overwrite")
    RAW.mkdir(parents=True, exist_ok=True)
    paths = {key: RAW / Path(url).name for key, url in FILES.items()}
    for key, url in FILES.items():
        if args.download:
            download(url, paths[key])
        elif not paths[key].is_file():
            raise FileNotFoundError(f"Local export missing: {paths[key].name}; downloads require --download")
    print("Reading English/Korean sentence exports...")
    english = read_sentences(paths["eng"], "eng")
    korean = read_sentences(paths["kor"], "kor")
    print(f"Loaded {len(english):,} English and {len(korean):,} Korean sentences")
    pairs = build_pairs(english, korean, paths["links"])
    write_splits(pairs)


if __name__ == "__main__":
    main()
