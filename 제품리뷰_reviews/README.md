# 제품과 모델 리뷰 | Software and model reviews

실제 프로그램이나 배포된 모델을 대상으로 기능, 동작 조건, 사용상의 제약을 살펴봅니다. 직접 실행한 결과와 공식 문서로 확인한 사양을 구분합니다. 여러 기술의 흐름을 비교하는 글은 [기술 동향](../기술동향_technology/README.md), 방법을 수식으로 읽는 글은 [논문 해설](../논문해설_papers/README.md)에서 다룹니다.

| 대상 | 리뷰에서 확인할 내용 | 확인 방식 |
| --- | --- | --- |
| [SQLite WAL](SQLite의동시접근_SQLITE.md) | 읽기와 쓰기가 겹칠 때 관찰되는 값과 잠금 | 두 연결의 실제 트랜잭션 실행 |
| [AI 모델과 서비스](../AI모델실험_model-lab/README.md) | 배포물, 구조, 실행 자원, 공개 범위 | 공급사별 공식 자료와 CPU 계산 실험 |
| [개발 도구와 실행 환경](../도구와환경_tools/README.md) | 언어·컴파일러·시뮬레이터·계측 도구의 역할 | 공식 문서와 저장소의 실행 예제 연결 |

## 리뷰에서 숫자를 읽는 방법

지연시간은 하드웨어·입력 크기·배치에 따라 달라지고, 메모리는 가중치 외에 캐시와 실행 버퍼를 포함합니다. 같은 이름의 모델도 버전과 양자화 방식이 다르면 다른 대상으로 취급합니다. 구매나 도입 판단에는 기능뿐 아니라 배포 조건, 유지보수, 외부로 보내는 데이터, 장애 시 복구 방법도 함께 봅니다.

SQLite 글은 두 연결을 로컬에서 실행한 리뷰입니다. 공급사별 모델 글에는 해당 모델의 가중치 추론 여부를 표시했습니다.

## English

Reviews examine deployable software and models: behavior, operating conditions and practical limits. SQLite is reviewed through an executable concurrency observation. Model studies distinguish official specifications from locally executed calculations. Paper analysis and technology-wide comparisons have separate indexes. Version, input, hardware and deployment terms belong with any comparison.
