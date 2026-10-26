# 기여 안내 | Contributing

오류를 발견하셨다면 관련 문서와 재현 조건, 근거가 되는 자료를 함께 알려 주시면 확인하기 쉽습니다. 설명의 가정과 실행 결과가 서로 맞는지 먼저 살펴보고, 내용을 고칠 때에는 연결된 예제와 출처도 함께 확인합니다.

| 안내 | 다루는 내용 |
| --- | --- |
| [문서와 코드 구성](저장소구성_STRUCTURE.md) | 학습 분야와 분석 글, 실행 자료의 위치 |
| [문장과 제목](../AGENTS.md) | 존댓말, 구체적인 제목, 측정 사실과 출처 보존 |
| [그림과 표](그림과표_FIGURES.md) | 단위·축·범례와 편집 원본 |
| [프로젝트 문서](프로젝트문서_PROJECT_DOCUMENTS.md) | 요구사항, 설계, 구현, 테스트의 연결 |
| [내용 점검 기록](콘텐츠점검_CONTENT_REVIEW.md) | 문서 분류와 본문, 확인 범위 |

그림과 표 안내는 자료를 재사용하거나 기여하실 때 원본과 표기를 이해하기 위한 공개 문서입니다. 일반 학습 목차와 구분하여 이곳에 모았습니다. 저장소에서 사용하는 도구의 뜻은 [도구와 환경](../도구와환경_tools/README.md)에서 확인하실 수 있습니다.

서로 다른 분야의 수정은 커밋을 나누고, 제목에는 해당 문서에서 바뀐 대상을 적습니다. 파일을 옮기거나 목차를 고칠 때에는 연결된 링크도 함께 확인합니다. 게시 전에는 수정한 파일과 상위 폴더의 최근 커밋 제목이 실제 변경 내용과 맞는지 살펴봅니다.

## 문서 링크 검사

저장소 루트에서 실행합니다. 문서 검사는 내부 경로·제목 앵커·출처 목록의 연결을 확인합니다. 코드 안의 배열식이나 링크 예시는 본문의 실제 링크와 구분합니다.

```bash
python 기여안내_contributing/tools/check_documents.py
python -m unittest discover -s 기여안내_contributing/tools -p test_check_documents.py
```

이 검사는 연결 상태를 확인하는 도구입니다. 기술 주장의 정확성과 원문이 뒷받침하는 범위는 해당 자료를 읽고 대조합니다.

## English

Please include the affected document, reproduction conditions and supporting sources when reporting an error. Contributor documentation covers repository structure, writing, editable figures and project evidence. It is separate from the learning index so readers can go directly to the subject they need.

Keep changes in different subjects in separate commits and name the actual changed material. Check links when moving files or editing indexes, and review the latest commit titles shown for changed files and their parent folders before publication.
