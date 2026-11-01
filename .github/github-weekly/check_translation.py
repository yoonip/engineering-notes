"""수동 실행 시 실제 공개 번역 모델의 다운로드와 CPU 추론을 확인합니다."""
import json
import os
from pathlib import Path
import tempfile

from collect import HERE, Introductions, KST, collect, datetime

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
    result = collect(root / 'archive', datetime.now(KST), os.environ.get('GITHUB_TOKEN', ''),
                     reviewed, root / 'translations.json')
    assert result['status'] == 'published' and result['count'] == 10
    print(json.dumps(result, ensure_ascii=False))
