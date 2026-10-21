# 기술 동향 | Technology landscape

발표 날짜와 확인 날짜를 구분하고, 실제 배포물·표준·벤치마크에서 무엇이 달라졌는지 살펴봅니다. 개별 제품의 작동 원리와 비교 근거는 [제품 리뷰](../제품리뷰_reviews/README.md), 방법과 수식은 [논문 해설](../논문해설_papers/README.md)에서 다룹니다.

| 주제 | 읽을 글 | 관찰할 변화 |
| --- | --- | --- |
| AI 추론 시스템 | [MLPerf Inference v6.1과 비교 조건](AI추론평가_2026-10.md) | 단일 모델 처리에서 RAG·도구 사용·전체 시스템 평가로 넓어지는 범위 |
| 모델 배포 | [공급사와 실제 모델](../AI모델실험_model-lab/PROVIDERS.md) | API, 공개 가중치, 연구 코드가 제공하는 접근 범위 |
| 메모리와 연산 | [차세대 소자·컴퓨팅](../분야_topics/54-차세대소자컴퓨팅_research-frontiers/README.md) | PIM의 데이터 이동 이점과 변환·교정 비용 |
| 공개 하드웨어 | [EDA와 공개 하드웨어](../분야_topics/35-EDA오픈하드웨어_eda-open-hardware/README.md) | ISA·CPU 구현·PDK·설계 도구의 서로 다른 역할 |

## 발표를 해석하는 기준

발표의 대상이 논문, 공개 코드, 가중치, 판매 제품 중 무엇인지 먼저 확인합니다. 논문에 수치가 있다는 사실과 제품이 동일한 조건에서 동작한다는 사실은 다릅니다. 비교에서는 하드웨어 수, 정밀도, 입력 길이, 품질 조건과 측정 범위를 맞춥니다. 장기적인 추세를 판단할 때는 같은 조건의 결과를 시간 순서로 비교합니다.

## English

This section separates publication dates from verification dates and follows concrete changes in deployable artifacts, standards and benchmarks. The first dated analysis examines MLPerf Inference v6.1 and the move toward end-to-end workloads. Related technical guides cover model access, processing-in-memory and open hardware. Product-specific observations and paper derivations have separate sections.
