"""새 자료 폴더와 수집 상태만 주제별 커밋으로 게시합니다."""
from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path
import subprocess

from update_pipeline import GROUPS, KST, OUTPUT_DIRS, ROOT

TITLES = {
    'models': ('모델 발표', 'Model announcements'),
    'reports': ('보고서 소식', 'Report updates'),
    'technology': ('기술 동향 자료', 'Technology sources'),
    'tools': ('도구·보안 자료', 'Tool and security sources'),
    'industry': ('산업 기술 자료', 'Industry sources'),
    'products': ('제품·기술 자료', 'Product technology sources'),
    'papers': ('새 논문·연구 소개', 'Paper and research notices'),
    'learning': ('새 강의·학습 자료', 'Course and learning notices'),
}


def git(repo: Path, *args: str) -> bytes:
    return subprocess.run(['git', '-C', str(repo), *args], check=True, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE).stdout


def commit_changes(repo: Path, stamp: str) -> list[dict]:
    if git(repo, 'diff', '--cached', '--name-only', '-z'):
        raise ValueError('Existing staged work must not be published.')
    folders = {group: folder + '/' + OUTPUT_DIRS[group] for group, (folder, _) in GROUPS.items()}
    state_path = '.github/updates/state.json'
    status = [row for row in git(repo, 'status', '--porcelain=v1', '-z', '--untracked-files=all').decode('utf-8').split('\0') if row]
    dirty = []
    for row in status:
        path = row[3:]
        if row[:2].strip() not in ('M', '??'):
            raise ValueError('Unexpected file operation: ' + path)
        if path != state_path and not any(path.startswith(folder + '/') for folder in folders.values()):
            raise ValueError('Refusing to publish a file outside the source folders: ' + path)
        dirty.append(path)
    commits = []
    for group, folder in list(folders.items()) + [('state', state_path)]:
        paths = [path for path in dirty if path == folder or path.startswith(folder + '/')]
        if not paths:
            continue
        git(repo, 'add', '--', *paths)
        staged = [path for path in git(repo, 'diff', '--cached', '--name-only', '-z').decode('utf-8').split('\0') if path]
        if set(staged) != set(paths):
            raise ValueError('Staged files differ from the selected source folder.')
        git(repo, 'diff', '--cached', '--check')
        korean, english = TITLES.get(group, ('공식 자료 확인 상태', 'Publication check state'))
        title = f'{korean} {stamp} / {english} {stamp}'
        git(repo, 'commit', '-m', title)
        commits.append({'group': group, 'sha': git(repo, 'rev-parse', 'HEAD').decode().strip(), 'title': title})
    return commits


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=ROOT)
    parser.add_argument('--push', action='store_true')
    args = parser.parse_args()
    git(args.repo, 'config', 'user.name', 'github-actions[bot]')
    git(args.repo, 'config', 'user.email', '41898282+github-actions[bot]@users.noreply.github.com')
    result = commit_changes(args.repo, datetime.now(KST).strftime('%Y-%m-%d %H:%M'))
    if args.push and result:
        for attempt in range(3):
            git(args.repo, 'fetch', 'origin', 'main')
            git(args.repo, 'rebase', 'origin/main')
            try:
                git(args.repo, 'push', 'origin', 'HEAD:main')
                break
            except subprocess.CalledProcessError:
                if attempt == 2:
                    raise
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
