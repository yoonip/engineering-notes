"""주간 프로젝트 기록과 번역 캐시만 커밋하고 정상 push합니다."""
from datetime import datetime
import subprocess

from collect import KST, ROOT

ALLOWED = ('인기GitHub프로젝트_github-weekly/주간기록/', '.github/github-weekly/translations.json')


def git(*args: str) -> bytes:
    return subprocess.run(['git', '-C', str(ROOT), *args], check=True,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout


def publish() -> None:
    if git('diff', '--cached', '--name-only', '-z'):
        raise ValueError('Existing staged changes must not be published')
    paths = []
    for row in git('status', '--porcelain=v1', '-z', '--untracked-files=all').decode('utf-8').split('\0'):
        if not row:
            continue
        status, path = row[:2], row[3:]
        if status not in (' M', '??') or not (path.startswith(ALLOWED[0]) or path == ALLOWED[1]):
            raise ValueError('Unexpected change; refusing to publish: ' + path)
        paths.append(path)
    if not paths:
        print('No new weekly record')
        return
    git('config', 'user.name', 'github-actions[bot]')
    git('config', 'user.email', '41898282+github-actions[bot]@users.noreply.github.com')
    git('add', '--', *paths)
    staged = git('diff', '--cached', '--name-only', '-z').decode('utf-8').split('\0')
    if set(filter(None, staged)) != set(paths):
        raise ValueError('Staged paths differ from selected output')
    git('diff', '--cached', '--check')
    stamp = datetime.now(KST).date().isoformat()
    git('commit', '-m', f'주간 GitHub 프로젝트 {stamp} / Weekly GitHub projects {stamp}')
    for attempt in range(3):
        git('fetch', 'origin', 'main')
        git('rebase', 'origin/main')
        try:
            git('push', 'origin', 'HEAD:main')
            return
        except subprocess.CalledProcessError:
            if attempt == 2:
                raise


if __name__ == '__main__':
    publish()
