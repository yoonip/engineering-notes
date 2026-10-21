"""Render readable references without discarding their machine-readable records."""
from pathlib import Path
from urllib.parse import urlparse
import argparse
import json
import os

ROOT = Path(__file__).resolve().parents[2]
FOLDER = ROOT / '참고자료_references'
NAMES = {
    '기초출처_FOUNDATIONS_SOURCES': ('공학 기초의 출처', 'Foundations sources'),
    '확장출처_EXTENDED_SOURCES': ('분야별 학습의 출처', 'Technical topic sources'),
    '심화출처_ADVANCED_SOURCES': ('심화 학습의 출처', 'Advanced sources'),
    '추론출처_REASONING_SOURCES': ('추론과 인문사회의 출처', 'Reasoning and humanities sources'),
}


def render(path):
    data = json.loads(path.read_text(encoding='utf-8'))
    title, english = NAMES[path.stem]
    rows = data['articles']
    output = [f'# {title} | {english}', '',
              f'해설에서 사용한 자료를 글별로 모았습니다. 자료 목록의 확인 기준일은 {data["review_date"]}입니다. '
              '각 글의 정의·수식·가정 가까이에 있는 인용과 함께 읽으시면 근거의 범위를 확인하기 쉽습니다.', '',
              '[전체 참고 자료](README.md)', '',
              '## 글별 참고 자료', '']
    for number, row in enumerate(rows, 1):
        article = ROOT / row['path']
        if not article.is_file():
            raise ValueError(f'Missing article: {row["path"]}')
        relative = Path(os.path.relpath(article, FOLDER)).as_posix()
        output.extend([f'### {number}. {row["title"]}', '', f'[해설 읽기]({relative})', ''])
        for url in row['reference_urls']:
            parsed = urlparse(url)
            label = parsed.netloc.removeprefix('www.')
            tail = parsed.path.rstrip('/').rsplit('/', 1)[-1]
            if tail:
                label += ' · ' + tail
            output.append(f'- [{label}]({url})')
        output.append('')
    output.extend(['## 데이터와 문서', '',
                   f'[JSON 원본]({path.name})은 문서 경로와 출처 URL을 연결하는 데이터입니다. '
                   '출처 문서 생성과 경로 검사에서 사용합니다. 읽기용 목록은 이 Markdown 문서입니다.', '',
                   '기준일은 자료 목록의 기록 날짜이며 모든 외부 페이지를 매번 재검증했다는 뜻은 아닙니다. '
                   '구체적인 인용 범위와 실행 여부는 각 해설과 검증 기록에 있습니다.', '',
                   '## English', '',
                   'This readable index groups the references by article. '
                   'The JSON record retains article paths and source URLs for generation and path checks. '
                   'Read the citations beside each claim for the scope of support; the inventory date is not a claim of continuous link verification.', ''])
    return '\n'.join(output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    for name in NAMES:
        path = FOLDER / (name + '.json')
        expected = render(path)
        target = path.with_suffix('.md')
        if args.check:
            assert target.read_text(encoding='utf-8') == expected, f'Stale reference view: {target.name}'
        else:
            target.write_text(expected, encoding='utf-8', newline='\n')
        print(target.name)
