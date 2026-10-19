"""Create or verify a relative-path SHA256 inventory of the source export."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRECTORIES = {'.git', '.venv', '__pycache__', '.pytest_cache', 'data',
                    'results', 'generated', 'user_runs', 'private-audit', 'vendor'}


def digest(path: Path) -> str:
    result = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            result.update(block)
    return result.hexdigest()


def inventory(root: Path):
    for path in sorted(root.rglob('*')):
        relative = path.relative_to(root)
        if path.is_file() and not SKIP_DIRECTORIES.intersection(relative.parts):
            if relative.as_posix() != 'MANIFEST_SHA256.json':
                yield path, relative.as_posix()


def create(root: Path) -> dict:
    rows = [{'path': relative, 'bytes': path.stat().st_size, 'sha256': digest(path)}
            for path, relative in inventory(root)]
    result = {'algorithm': 'SHA256', 'scope': 'supplied source files; manifest itself excluded',
              'file_count': len(rows), 'total_bytes': sum(row['bytes'] for row in rows),
              'files': rows}
    (root / 'MANIFEST_SHA256.json').write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    return {'passed': True, 'recorded_files': len(rows)}


def verify(root: Path) -> dict:
    manifest = json.loads((root / 'MANIFEST_SHA256.json').read_text(encoding='utf-8'))
    failures, names = [], set()
    for row in manifest['files']:
        relative = row['path']
        unresolved = root / relative
        path = unresolved.resolve()
        if (relative in names or Path(relative).is_absolute() or '\\' in relative
                or ':' in relative or '..' in Path(relative).parts
                or not path.is_relative_to(root) or unresolved.is_symlink()):
            failures.append({'path': relative, 'reason': 'invalid or duplicate path'})
            continue
        names.add(relative)
        if not path.is_file():
            failures.append({'path': relative, 'reason': 'missing'})
        elif path.stat().st_size != row['bytes'] or digest(path) != row['sha256']:
            failures.append({'path': relative, 'reason': 'size or hash mismatch'})
    actual = {relative for _, relative in inventory(root)}
    for relative in sorted(actual - names):
        failures.append({'path': relative, 'reason': 'unrecorded source file'})
    return {'passed': not failures, 'checked_files': len(manifest['files']), 'failures': failures}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--verify', action='store_true')
    args = parser.parse_args()
    root = args.root.resolve()
    result = verify(root) if args.verify else create(root)
    print(json.dumps(result, ensure_ascii=False))
    if not result['passed']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
