"""수동 실행 시 실제 공개 번역 모델의 다운로드와 CPU 추론을 확인합니다."""
import json
import os
from pathlib import Path
import tempfile

from collect import HERE, Introductions, KST, clean, collect, datetime, get, repository
import guides
import comparisons
import source_checks

cache = {}
introductions = Introductions({}, cache)
source = 'A Python tool for converting documents to Markdown.'
translated = introductions.translate(source)
assert translated['text'] != source
assert introductions.translate(source) == translated
print(translated['method'] + ': ' + translated['text'])

# 초기 기록이 이미 있어도 hosted runner에서 새 원본 수집 경로를 시험합니다.
with tempfile.TemporaryDirectory(prefix='github-weekly-live-') as directory:
    root = Path(directory)
    reviewed = json.loads((HERE / 'reviewed.json').read_text(encoding='utf-8'))
    details = json.loads((HERE / 'details.json').read_text(encoding='utf-8'))
    assessments = json.loads((HERE / 'comparisons.json').read_text(encoding='utf-8'))
    result = collect(root / 'archive', datetime.now(KST), os.environ.get('GITHUB_TOKEN', ''),
                     reviewed, root / 'translations.json', details, assessments)
    assert result['status'] == 'published' and result['count'] == 10
    record = next((root / 'archive').glob('주간기록/*/*/*.json'))
    items = json.loads(record.read_text(encoding='utf-8'))['items']
    assert all(item.get('guide') and item.get('readme') for item in items)
    assert all(item['guide'].get('assessment') for item in items)
    assert all(item['guide'].get('source_checks') for item in items)
    print(json.dumps(result, ensure_ascii=False))
    # 처음 등장한 저장소와 같은 경로로 원문 추출·CPU 번역도 실제 확인합니다.
    repo = items[0]['repository']
    readme = guides.fetch_readme(repo, os.environ.get('GITHUB_TOKEN', ''), get)
    extracted = guides.make_guide(repo, readme, {}, introductions)
    markdown = '\n'.join(guides.render_guide(extracted, clean))
    assert all('### ' + heading in markdown for heading in ('어떤 일을 하나요', '누구에게 유용한가요', '설치 방법', '사용 예시'))
    assert extracted['method'] == '공식 README 구간 추출·한국어 번역'
    extracted['assessment'] = comparisons.build(repo, readme, {}, introductions, get,
                                               repository, os.environ.get('GITHUB_TOKEN', ''))
    checked = source_checks.verify(extracted, readme, get, os.environ.get('GITHUB_TOKEN', ''))
    comparison_markdown = '\n'.join(guides.render_guide(extracted, clean))
    assert all('### ' + heading in comparison_markdown for heading in ('장점', '제약과 확인할 점', '비슷한 도구와의 차이', '선택하기 좋은 상황'))
    print('README extraction and CPU translation: ' + repo['full_name'] + ' @ ' + readme['commit'][:12])
    print(json.dumps(checked, ensure_ascii=False))
