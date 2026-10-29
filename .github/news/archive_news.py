"""최신 뉴스와 한국 표준시 기준 날짜별 보관본을 함께 작성합니다."""
from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
from pathlib import Path
import re
import tempfile

KST = timezone(timedelta(hours=9), name='KST')
LOCAL_DOCUMENTS = {
    'README.md', '매체와수집기준_sources.md', '운영안내_operations.md',
    '최신뉴스_latest.md', '날짜별/README.md',
}
LINK_TARGET = re.compile(r'(?P<open>\]\(<?)(?P<target>[^\s>)]+)(?P<close>>?\))')
ARCHIVE_NAME = re.compile(r'\d{4}-\d{2}-\d{2}\.md')


def _check_target(root: Path, target: Path) -> None:
    """보관 경로가 다른 디렉터리나 심볼릭 링크로 이어지지 않는지 확인합니다."""
    if target.is_symlink():
        raise ValueError('뉴스 게시 경로에는 심볼릭 링크를 사용할 수 없습니다.')
    try:
        target.resolve().relative_to(root)
    except ValueError:
        raise ValueError('뉴스 게시 경로가 뉴스 디렉터리를 벗어납니다.') from None
    cursor = target.parent
    while cursor != root:
        if cursor.is_symlink():
            raise ValueError('뉴스 게시 디렉터리에 심볼릭 링크가 있습니다.')
        if cursor.parent == cursor:
            raise ValueError('뉴스 게시 경로가 뉴스 디렉터리를 벗어납니다.')
        cursor = cursor.parent


def archive_text(text: str) -> str:
    """알려진 뉴스 내부 링크만 연도별 보관 디렉터리에 맞게 바꿉니다."""
    def rewrite(match: re.Match) -> str:
        target = match['target']
        base = target.split('#', 1)[0].split('?', 1)[0]
        if base in LOCAL_DOCUMENTS:
            target = '../../' + target
        return match['open'] + target + match['close']
    return LINK_TARGET.sub(rewrite, text)


def _archive_entries(root: Path, incoming: Path) -> list[Path]:
    base = root / '날짜별'
    entries = {incoming.relative_to(base)}
    if base.exists():
        for path in base.glob('*/*.md'):
            if not path.is_file() or not ARCHIVE_NAME.fullmatch(path.name):
                continue
            _check_target(root, path)
            try:
                day = date.fromisoformat(path.stem)
            except ValueError:
                continue
            if path.parent.name == f'{day.year:04d}':
                entries.add(path.relative_to(base))
    return sorted(entries, key=lambda path: path.name, reverse=True)


def _index_text(entries: list[Path], latest_name: str) -> str:
    navigation = f'[최신 뉴스](../{latest_name})'
    if latest_name != 'README.md':
        navigation += ' · [뉴스 안내](../README.md)'
    lines = ['# 날짜별 뉴스 | News archive', '',
        navigation, '',
        '한국 표준시를 기준으로 날짜를 구분합니다. 날짜를 선택하면 그날의 기사를 읽으실 수 있습니다.', '']
    year = None
    for path in entries:
        if path.parent.name != year:
            if year is not None:
                lines.append('')
            year = path.parent.name
            lines += ['## ' + year, '']
        lines.append(f'- [{path.stem}]({path.as_posix()})')
    return '\n'.join(lines) + '\n'


def _stage(target: Path, text: str) -> Path:
    staged = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', newline='\n',
                                        dir=target.parent, prefix='.' + target.name + '.',
                                        suffix='.tmp', delete=False) as stream:
            staged = Path(stream.name)
            stream.write(text)
    except BaseException:
        if staged is not None:
            staged.unlink(missing_ok=True)
        raise
    return staged


def publish_bundle(output: Path, text: str, now: datetime) -> dict[str, str]:
    """최신 목록·당일 보관본·날짜별 목차를 작성하고 상대 경로를 반환합니다.

수집 실패 시에는 호출하지 않습니다. 각 파일은 임시 파일을 완성한 뒤 교체합니다.
전체 파일 묶음에 대한 파일시스템 트랜잭션은 아니므로 게시 단계는 모든 파일 작성이
성공했을 때에만 Git 커밋을 수행해야 합니다.
"""
    output = Path(output)
    if now.tzinfo is None:
        raise ValueError('보관 날짜를 정하려면 시간대가 필요합니다.')
    if '..' in output.parts or output.parent.is_symlink() or output.is_symlink():
        raise ValueError('뉴스 게시 경로에 상위 이동이나 심볼릭 링크를 사용할 수 없습니다.')
    if output.suffix != '.md':
        raise ValueError('최신 뉴스 파일은 Markdown 파일이어야 합니다.')
    root = output.parent.resolve()
    output = root / output.name
    day = now.astimezone(KST).date()
    daily = root / '날짜별' / f'{day.year:04d}' / (day.isoformat() + '.md')
    index = root / '날짜별' / 'README.md'
    for target in (output, daily, index):
        _check_target(root, target)
    entries = _archive_entries(root, daily)
    documents = [(daily, archive_text(text)), (index, _index_text(entries, output.name)), (output, text)]
    staged: list[tuple[Path, Path]] = []
    try:
        for target, content in documents:
            target.parent.mkdir(parents=True, exist_ok=True)
            _check_target(root, target)
            staged.append((_stage(target, content), target))
        for temporary, target in staged:
            _check_target(root, target)
            temporary.replace(target)
    finally:
        for temporary, _ in staged:
            temporary.unlink(missing_ok=True)
    return {'latest': output.name, 'daily': daily.relative_to(root).as_posix(),
            'index': index.relative_to(root).as_posix()}
