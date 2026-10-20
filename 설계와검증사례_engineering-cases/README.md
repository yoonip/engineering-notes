# 설계와 검증 사례 | Engineering decisions and checks

요구사항과 실제 코드를 연결하고, 같은 입력에서 잘못된 조건과 해결한 조건을 비교합니다. 15개 사례의 본문에서 원인·대안·수정 방법을 읽고, 날짜별 기록에서 환경·명령·관측값을 확인하실 수 있습니다.

## C·C++·펌웨어

| 사례 | 오류와 해결 | 실행 기록 |
| --- | --- | --- |
| [C 프레임 길이·바이트 순서](이진프레임의길이와바이트순서_c-frame-bounds.md) | 길이 축약의 거짓 승인, 공간 상한 검사, 알려진 endian 패턴을 비교합니다. | [2026-10-21](검증기록_evidence/C펌웨어경계검사_20261021.md) |
| [C++ 수신 버퍼·뷰 소유권](수신버퍼의소유권과뷰수명_cpp-view-ownership.md) | 버퍼 재사용·길이 손실·재할당 핸들을 복사와 명시적 계약으로 구분합니다. | [2026-10-21](검증기록_evidence/C펌웨어경계검사_20261021.md) |
| [링버퍼의 공개 순서](링버퍼의공개순서와공유카운터_ring-publication.md) | 조기 공개·공유 카운터 유실을 사건 모델로 재현하고 C11 SPSC 규칙을 실행합니다. | [2026-10-21](검증기록_evidence/C펌웨어경계검사_20261021.md) |
| [뮤텍스 대기·우선순위 역전](뮤텍스대기와마감시간_rtos-priority-inversion.md) | 낮은 우선순위 소유자의 실행을 추적하고 상속 유무에 따른 응답·마감시간을 비교합니다. | [2026-10-21](검증기록_evidence/RTOS스케줄과알림검사_20261021.md) |
| [검사와 대기 사이의 알림 유실](검사와대기사이의알림유실_rtos-lost-wakeup.md) | resume 유실과 보존되는 알림, 알림을 지운 뒤 남은 큐 데이터를 구분합니다. | [2026-10-21](검증기록_evidence/RTOS스케줄과알림검사_20261021.md) |
| [FPGA 프레임 오류](프레임오류와FPGA검증_fpga-frame-validation.md) | 바이트·채널·순번 오류를 구별하고 가상 ADC·mock UART와 별도 RTL을 나누어 확인합니다. | [2026-10-21](검증기록_evidence/FPGA검증_20261021.md) |

## CAN 복구·수신 데이터

| 사례 | 오류와 해결 | 실행 기록 |
| --- | --- | --- |
| [CAN의 ACK·복구 정책](CAN의ACK와복구정책_can-recovery-policy.md) | 합성 상태 관측에서 재시작 요청·상태 확인·횟수 제한을 분리합니다. | [2026-10-21](검증기록_evidence/CAN정책과수신계약검증_20261021.md) |
| [CAN 수신값의 형식·신선도](CAN수신값의형식과신선도_can-payload-contract.md) | 프레임 형식·바이트 순서·순번·수신 시각을 검사하고 무효 프레임의 상태 갱신을 막습니다. | [2026-10-21](검증기록_evidence/CAN정책과수신계약검증_20261021.md) |

## 칩 산술·시험 데이터

| 사례 | 오류와 해결 | 실행 기록 |
| --- | --- | --- |
| [칩 산술의 레이아웃·누산 폭](칩산술의레이아웃과누산폭_chip-arithmetic-contract.md) | 주소식·장치 입력 복사본·좁히기를 독립 기대값과 비교합니다. | [2026-10-21](검증기록_evidence/칩모델과시험자료검증_20261021.md) |
| [시험 ID·수율·오판율](시험데이터의식별자와오판율_test-data-identity-metrics.md) | 행 비교가 만든 거짓 일치율을 ID 연결로 드러내고 서로 다른 분모를 구분합니다. | [2026-10-21](검증기록_evidence/칩모델과시험자료검증_20261021.md) |
| [시험 러너의 결과 계약](시험러너의종료상태와결과계약_chip-runner-result-contract.md) | 실제 자식프로그램의 종료·시간초과와 결과의 실행 ID·입력 해시·case·수치를 함께 판정합니다. | [2026-10-21](검증기록_evidence/칩시험러너오류재현_20261021.md) |

## AI·데이터 시스템

| 사례 | 오류와 해결 | 실행 기록 |
| --- | --- | --- |
| [AI 배포의 전처리·특성 순서](AI배포의전처리와특성순서_ai-preprocessing-contract.md) | 잘못된 열 순서·scaler 누락·요청별 재학습을 저장한 입력 계약과 대조합니다. | [2026-10-21](검증기록_evidence/AI배포와그룹평가검증_20261021.md) |
| [생산 묶음 단위 평가](생산묶음단위분할과평가누출_ai-group-evaluation.md) | 행 분할의 공유 group을 거절하고 학습 통계로만 평가합니다. | [2026-10-21](검증기록_evidence/AI배포와그룹평가검증_20261021.md) |
| [제조 시계열의 인과 경계](제조시계열의인과경계_causal-trace-validation.md) | attention·합성곱의 미래 참조, 저장 추론·입력 거부를 확인합니다. | [2026-10-21](검증기록_evidence/인과마스크검증_20261021.md) |
| [SQLite 갱신 충돌](동시갱신과SQLite검증_sqlite-concurrency.md) | 덮어쓰기·원자적 증가·업무 버전 검사와 WAL 스냅샷을 비교합니다. | [2026-10-21](검증기록_evidence/SQLite갱신검증_20261021.md) |

## 코드와 계측으로 연결하기

- [새 오류 재현 코드](../예제_examples/실무검증_practical-validation/README.md): C/C++ 빌드, 칩 모형, AI 합성 학습의 실행 방법입니다.
- [현장 계측과 검증](../현장계측과검증_measurement-validation/README.md): 장비 9개 모델의 특성과 사용 절차, DMA·캐시, 예외 추적, PVT, 통신, 계측 자동화입니다.
- [계측 자동화의 offline 기록](검증기록_evidence/계측자동화모의검사_20261021.md): 기존 19개 mock·모형 검사의 범위입니다.
- [구현 프로젝트](../프로젝트_projects/README.md): 기존 소스와 이전 실험·실행 결과입니다.

새 사례의 실행은 PC 호스트·소프트웨어 모형입니다. FPGA의 RTL 성공 1회와 반복 컴파일 실패, 기존 제조 GPU 요약과 새 합성 CPU 검사는 각 기록에서 구별합니다. 실제 장비·산업 데이터·동시 스트레스 검증 여부는 해당 관측 옆에 표시합니다.

## English

Fifteen cases connect requirements, executable code, deliberately faulty controls, intended fixes and dated observations. They cover C/C++ ownership, firmware publication, RTOS scheduling/notifications, CAN recovery/payload contracts, chip arithmetic, test identity, subprocess result validation, AI serving/evaluation, FPGA frames and SQLite updates. Host execution, deterministic models and physical measurements have distinct scopes.
