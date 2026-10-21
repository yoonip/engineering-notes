# 설계와 검증 사례 | Engineering decisions and checks

요구사항과 실제 코드를 연결하고, 같은 입력에서 잘못된 조건과 해결한 조건을 비교합니다. 38개 사례의 본문에서 원인·대안·수정 방법을 읽고, 날짜별 기록에서 환경·명령·관측값을 확인하실 수 있습니다.

## C·C++·펌웨어

| 사례 | 오류와 해결 | 실행 기록 |
| --- | --- | --- |
| [C 프레임 길이·바이트 순서](이진프레임의길이와바이트순서_c-frame-bounds.md) | 길이 축약의 거짓 승인, 공간 상한 검사, 알려진 endian 패턴을 비교합니다. | [2026-10-21](검증기록_evidence/C펌웨어경계검사_20261021.md) |
| [C++ 수신 버퍼·뷰 소유권](수신버퍼의소유권과뷰수명_cpp-view-ownership.md) | 버퍼 재사용·길이 손실·재할당 핸들을 복사와 명시적 계약으로 구분합니다. | [2026-10-21](검증기록_evidence/C펌웨어경계검사_20261021.md) |
| [링버퍼의 공개 순서](링버퍼의공개순서와공유카운터_ring-publication.md) | 조기 공개·공유 카운터 유실을 사건 모델로 재현하고 C11 SPSC 규칙을 실행합니다. | [2026-10-21](검증기록_evidence/C펌웨어경계검사_20261021.md) |
| [뮤텍스 대기·우선순위 역전](뮤텍스대기와마감시간_rtos-priority-inversion.md) | 낮은 우선순위 소유자의 실행을 추적하고 상속 유무에 따른 응답·마감시간을 비교합니다. | [2026-10-21](검증기록_evidence/RTOS스케줄과알림검사_20261021.md) |
| [검사와 대기 사이의 알림 유실](검사와대기사이의알림유실_rtos-lost-wakeup.md) | resume 유실과 보존되는 알림, 알림을 지운 뒤 남은 큐 데이터를 구분합니다. | [2026-10-21](검증기록_evidence/RTOS스케줄과알림검사_20261021.md) |
| [FPGA 프레임 오류](프레임오류와FPGA검증_fpga-frame-validation.md) | 바이트·채널·순번 오류를 구별하고 가상 ADC·mock UART와 별도 RTL을 나누어 확인합니다. | [2026-10-21](검증기록_evidence/FPGA검증_20261021.md) |
| [W1C 상태 소거·완료 버퍼 소유권](상태비트소거와완료버퍼소유권_irq-w1c-ownership.md) | 읽기-수정-쓰기로 다른 상태를 지우는 오류와 완료 버퍼 인계를 분리합니다. | [2026-10-21](검증기록_evidence/인터럽트DMA캐시모델검증_20261021.md) |
| [캐시와 DMA의 복사본·공유 line](캐시와RAM의데이터불일치_dma-cache-lines.md) | TX·RX의 오래된 값과 공유 line 이웃 손실을 유지 연산·소유권으로 비교합니다. | [2026-10-21](검증기록_evidence/인터럽트DMA캐시모델검증_20261021.md) |
| [작업 진행·워치독·리셋 기록](작업진행을확인하는워치독과리셋기록_watchdog-health-reset.md) | 갱신 task만 살아 있는 오류, 이전 완료 표시 재사용, 시간 순환과 리셋 원인 소거를 비교합니다. | [2026-10-21](검증기록_evidence/워치독진행상태와리셋검사_20261021.md) |
| [중단된 업데이트·슬롯 선택·롤백](중단된업데이트의슬롯선택과롤백_firmware-ab-update.md) | 파일 기록 중단과 재시작에서 이미지·선택 기록·시험 부팅·성공 확정을 구분합니다. | [2026-10-21](검증기록_evidence/펌웨어업데이트중단과복구검사_20261021.md) |

## 통신과 수신 데이터

| 사례 | 오류와 해결 | 실행 기록 |
| --- | --- | --- |
| [CAN의 ACK·복구 정책](CAN의ACK와복구정책_can-recovery-policy.md) | 합성 상태 관측에서 재시작 요청·상태 확인·횟수 제한을 분리합니다. | [2026-10-21](검증기록_evidence/CAN정책과수신계약검증_20261021.md) |
| [CAN 수신값의 형식·신선도](CAN수신값의형식과신선도_can-payload-contract.md) | 프레임 형식·바이트 순서·순번·수신 시각을 검사하고 무효 프레임의 상태 갱신을 막습니다. | [2026-10-21](검증기록_evidence/CAN정책과수신계약검증_20261021.md) |
| [SPI 선택선·더미 클록](SPI의선택선과더미클록_spi-cs-dummy-edges.md) | 플래시 읽기의 명령·주소·dummy·유효 데이터와 CS 경계를 비교합니다. | [2026-10-21](검증기록_evidence/SPI와I2C전송경계검증_20261021.md) |
| [I2C 묶음 읽기·NACK](I2C의묶음읽기와NACK_i2c-combined-read.md) | EEPROM 주소 지정·repeated START·읽기 종료 NACK의 주체와 실패 단계를 구분합니다. | [2026-10-21](검증기록_evidence/SPI와I2C전송경계검증_20261021.md) |
| [UART 분할 수신·재동기화](UART의분할수신과재동기화_uart-stream-resync.md) | 수신 호출과 프레임 경계를 구분하고 길이·checksum·손상 뒤 재시작을 검사합니다. | [2026-10-21](검증기록_evidence/UART와UDP수신경계검증_20261021.md) |
| [Ethernet·IPv4·UDP 길이](이더넷프레임의길이와UDP경계_ethernet-ipv4-udp.md) | 계층별 길이·padding·checksum·지원 범위와 로컬 UDP 데이터그램 경계를 구분합니다. | [2026-10-21](검증기록_evidence/UART와UDP수신경계검증_20261021.md) |
| [USB 부분 전송·재시도](USB의부분전송과중복없는복구_usb-bulk-recovery.md) | status와 실제 길이, STALL 뒤 중복 적용, 연결 세대와 버퍼 소유권을 비교합니다. | [2026-10-21](검증기록_evidence/USB와PCIe전송계약검증_20261021.md) |
| [PCIe 태그·분할 응답](PCIe의태그와분할응답_pcie-split-completions.md) | 제한된 read 요청의 tag·byte count·lower address와 응답 완성을 대조합니다. | [2026-10-21](검증기록_evidence/USB와PCIe전송계약검증_20261021.md) |

## 저장장치와 데이터 복구

| 사례 | 오류와 해결 | 실행 기록 |
| --- | --- | --- |
| [NVMe 쓰기 완료·영속성](NVMe의쓰기완료와영속성_nvme-write-persistence.md) | 완료 상태와 휘발성 캐시, flush·FUA의 적용 범위를 비교합니다. | [2026-10-21](검증기록_evidence/저장장치완료와영속성검사_20261021.md) |
| [eMMC·SD busy와 쓰기 실패](eMMC와SD의busy와쓰기실패_emmc-sd-write-status.md) | 자료 수신·busy 해제·상태 오류와 캐시 조건을 구분합니다. | [2026-10-21](검증기록_evidence/저장장치완료와영속성검사_20261021.md) |
| [중단된 저널·트랜잭션 복구](중단된저널의트랜잭션복구_storage-journal-recovery.md) | 파일 기록 중단 뒤 유효한 commit과 손상·미완성 자료를 구분합니다. | [2026-10-21](검증기록_evidence/저장저널중단과복구검사_20261021.md) |
| [NAND 불량 블록·마모 분산](NAND의불량블록과마모분산_nand-bad-block-wear.md) | 불량 블록 제외, 쓰기 실패와 동적·정적 마모 분산의 비용을 비교합니다. | [2026-10-21](검증기록_evidence/NAND블록과교란모델검사_20261021.md) |
| [읽기 교란·데이터 이동](읽기교란의징후와데이터이동_nand-read-disturb-scrub.md) | 주입한 정정·복구 불가 상태에서 이동·검증·매핑 게시 순서를 확인합니다. | [2026-10-21](검증기록_evidence/NAND블록과교란모델검사_20261021.md) |
| [FTL 매핑 게시·기록 중단](FTL의매핑게시와전원중단_ftl-map-publication.md) | 파일 기록의 각 중단 지점에서 데이터와 논리·물리 주소의 대응을 확인합니다. | [2026-10-21](검증기록_evidence/FTL매핑과GC중단검사_20261021.md) |
| [FTL GC·TRIM·주소 재사용](FTL의GC와폐기된주소재사용_ftl-gc-trim-reuse.md) | 오래된 이동 계획, 삭제 상태와 재사용된 물리 주소의 세대를 구분합니다. | [2026-10-21](검증기록_evidence/FTL매핑과GC중단검사_20261021.md) |
| [파일시스템 검사·사본 복구](파일시스템의손상검사와복구계획_filesystem-check-repair.md) | 학습 이미지의 구조·내용을 검사하고 원본 해시에 묶인 복구 계획을 실행합니다. | [2026-10-21](검증기록_evidence/파일시스템이미지검사와복구_20261021.md) |
| [파일 이름·블록 소유권](파일이름과블록소유권의복구_filesystem-orphans-block-ownership.md) | 고아 파일·정상 하드 링크·블록 충돌과 복구를 거부해야 할 조건을 비교합니다. | [2026-10-21](검증기록_evidence/파일시스템이미지검사와복구_20261021.md) |

## RTL·칩 산술·시험 데이터

| 사례 | 오류와 해결 | 실행 기록 |
| --- | --- | --- |
| [칩 산술의 레이아웃·누산 폭](칩산술의레이아웃과누산폭_chip-arithmetic-contract.md) | 주소식·장치 입력 복사본·좁히기를 독립 기대값과 비교합니다. | [2026-10-21](검증기록_evidence/칩모델과시험자료검증_20261021.md) |
| [시험 ID·수율·오판율](시험데이터의식별자와오판율_test-data-identity-metrics.md) | 행 비교가 만든 거짓 일치율을 ID 연결로 드러내고 서로 다른 분모를 구분합니다. | [2026-10-21](검증기록_evidence/칩모델과시험자료검증_20261021.md) |
| [시험 러너의 결과 계약](시험러너의종료상태와결과계약_chip-runner-result-contract.md) | 실제 자식프로그램의 종료·시간초과와 결과의 실행 ID·입력 해시·case·수치를 함께 판정합니다. | [2026-10-21](검증기록_evidence/칩시험러너오류재현_20261021.md) |
| [RTL 내적기의 폭·전송 계약](RTL내적기의비트폭과전송계약_rtl-dot-handshake.md) | SystemVerilog 실행 결과를 Python 기대값과 대응시켜 부호·폭·지연·리셋·수락 오류를 검출합니다. | [2026-10-21](검증기록_evidence/RTL내적기비교검증_20261021.md) |
| [CDC·비동기 FIFO](비동기FIFO의Gray포인터와reset_cdc-async-fifo.md) | 두 클록의 포인터 동기화·full/empty·순서·리셋 계약을 RTL과 기준 큐로 비교합니다. | [2026-10-21](검증기록_evidence/비동기FIFO비교검증_20261021.md) |
| [DDR 명령 간격·메모리 패턴](DDR명령간격과메모리패턴_ddr-command-pattern-checks.md) | 명령표의 시간 위반, stuck bit·주소 alias·응답 누락과 패턴의 검출 한계를 구분합니다. | [2026-10-21](검증기록_evidence/DDR명령과패턴검증_20261021.md) |
| [ECC 단일 정정·이중 검출](ECC의단일비트정정과이중비트검출_ecc-secded.md) | 고정 학습 부호의 오류 위치·검출·정정과 보장 밖 반례를 비교합니다. | [2026-10-21](검증기록_evidence/ECC오류주입과검출범위_20261021.md) |

## AI·데이터 시스템

| 사례 | 오류와 해결 | 실행 기록 |
| --- | --- | --- |
| [AI 배포의 전처리·특성 순서](AI배포의전처리와특성순서_ai-preprocessing-contract.md) | 잘못된 열 순서·scaler 누락·요청별 재학습을 저장한 입력 계약과 대조합니다. | [2026-10-21](검증기록_evidence/AI배포와그룹평가검증_20261021.md) |
| [생산 묶음 단위 평가](생산묶음단위분할과평가누출_ai-group-evaluation.md) | 행 분할의 공유 group을 거절하고 학습 통계로만 평가합니다. | [2026-10-21](검증기록_evidence/AI배포와그룹평가검증_20261021.md) |
| [제조 시계열의 인과 경계](제조시계열의인과경계_causal-trace-validation.md) | attention·합성곱의 미래 참조, 저장 추론·입력 거부를 확인합니다. | [2026-10-21](검증기록_evidence/인과마스크검증_20261021.md) |
| [SQLite 갱신 충돌](동시갱신과SQLite검증_sqlite-concurrency.md) | 덮어쓰기·원자적 증가·업무 버전 검사와 WAL 스냅샷을 비교합니다. | [2026-10-21](검증기록_evidence/SQLite갱신검증_20261021.md) |

## 코드와 계측으로 연결하기

- [오류 재현 코드](../예제_examples/실무검증_practical-validation/README.md): C/C++·RTOS·인터럽트·DMA·통신·RTL·칩·AI 예제의 실행 방법입니다.
- [현장 계측과 검증](../현장계측과검증_measurement-validation/README.md): 장비 9개 모델의 특성과 사용 절차, DMA·캐시, 예외 추적, PVT, 통신, 계측 자동화입니다.
- [계측 자동화의 offline 기록](검증기록_evidence/계측자동화모의검사_20261021.md): 기존 19개 mock·모형 검사의 범위입니다.
- [구현 프로젝트](../프로젝트_projects/README.md): 기존 소스와 이전 실험·실행 결과입니다.

인터럽트·캐시·워치독 정책과 원시 통신 해석은 호스트 모델이며, UDP loopback은 실제 로컬 socket을 사용합니다. RTL 내적기·비동기 FIFO와 DDR 명령 fixture는 HDL 컴파일·시뮬레이션과 Python 비교를 연결합니다. USB·PCIe는 호스트 전송 모델이며, 펌웨어 업데이트와 데이터 저널 복구는 실제 파일 기록과 별도 프로세스의 재시작을 사용합니다. NVMe·eMMC·SD는 제한된 전송·보존 모델이며 ECC는 고정 부호의 오류 주입을 실행합니다. NAND는 작은 블록·마모·읽기 상태 모델이며, FTL은 호스트 파일의 매핑 기록과 별도 프로세스 종료를 사용합니다. 파일시스템 복구는 자체 학습 이미지의 사본에만 적용합니다. 이전 FPGA의 성공 1회와 반복 컴파일 실패 기록, 기존 GPU 결과도 해당 시점의 근거로 보존합니다. 실물 측정·산업 데이터·동시 스트레스 검증의 범위는 각 관측에서 구분합니다.

## English

Thirty-eight cases connect requirements, executable code, deliberately faulty controls, intended fixes and dated observations. They cover C/C++ ownership, firmware publication, RTOS scheduling/notifications, interrupt/DMA/cache contracts, CAN/SPI/I2C/UART/Ethernet, watchdog/reset, USB/PCIe, file-backed firmware updates, NVMe/eMMC/SD, file-journal recovery, NAND wear/read-disturb models, file-backed FTL mapping, educational filesystem repair, ECC fault injection, DDR command/pattern checks, RTL/reference and CDC/FIFO comparison, chip arithmetic, test identity, subprocess reports, AI serving/evaluation, FPGA frames and SQLite updates. HDL simulation, deterministic host models and physical measurements have distinct scopes.
