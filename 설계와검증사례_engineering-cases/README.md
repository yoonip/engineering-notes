# 설계와 검증 사례 | Engineering decisions and checks

같은 출력이 나왔다는 사실과 설계 요구를 지켰다는 사실은 다릅니다. 이곳에서는 저장소의 실제 코드를 대상으로 요구사항을 정하고, 대안을 비교하고, 일부 조건을 의도적으로 깨뜨려 관측한 결과를 연결합니다. 실행 환경과 아직 확인하지 않은 범위도 함께 적습니다.

| 사례 | 설계 질문과 확인한 내용 | 실행 기록 |
| --- | --- | --- |
| [FPGA 프레임 오류](프레임오류와FPGA검증_fpga-frame-validation.md) | 길이가 같은 데이터의 바이트·채널·순번 오류를 어떻게 구별합니까? Python 프레임·가상 ADC·mock UART와 별도 RTL을 나누어 확인합니다. | [2026-10-21](검증기록_evidence/FPGA검증_20261021.md) |
| [제조 시계열의 인과 경계](제조시계열의인과경계_causal-trace-validation.md) | attention 마스크가 있어도 임베딩에서 미래가 섞일 수 있습니까? 원본과 의도적 오류를 비교하고 저장 추론·입력 거부 조건을 확인합니다. | [2026-10-21](검증기록_evidence/인과마스크검증_20261021.md) |
| [SQLite 갱신 충돌](동시갱신과SQLite검증_sqlite-concurrency.md) | 두 쓰기가 성공해도 값이 사라질 수 있습니까? 덮어쓰기·원자적 증가·업무 버전 검사와 WAL 스냅샷을 비교합니다. | [2026-10-21](검증기록_evidence/SQLite갱신검증_20261021.md) |

이 사례의 새 실행은 PC 소프트웨어 검사입니다. FPGA 사례의 RTL 성공 1회와 반복 컴파일 실패도 함께 기록했습니다. AI 사례의 과거 GPU 요약과 이번 무학습 합성 CPU fixture를 구별합니다. SQLite는 실제 로컬 DB를 사용했지만 병렬 부하·전원 손실 시험은 하지 않았습니다.

## 계측·펌웨어·시스템으로 연결하기

- [현장 계측과 검증](../현장계측과검증_measurement-validation/README.md): 장비 4종의 특성과 사용 절차, DMA·캐시, 예외 추적, PVT, 차량·설비 통신, 계측 자동화입니다.
- [계측 자동화의 offline 검사 기록](검증기록_evidence/계측자동화모의검사_20261021.md): 기존 19개 검사, mock 통신의 범위, 파일 보존을 확인합니다.
- [구현 프로젝트](../프로젝트_projects/README.md): 전체 소스와 각 프로젝트의 이전 실행·실험 결과입니다.

## English

These three cases connect repository code with requirements, alternatives, deliberate faults, observations, reproducible commands and limits. Fresh CPU/software checks are separated from historical GPU results and physical hardware claims. The FPGA simulator's intermittent compiler failures remain visible beside its successful run.
