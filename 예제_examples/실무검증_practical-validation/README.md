# 실무 검증의 오류 재현 코드 | Reproducible engineering fault examples

정상 경로와 의도적으로 잘못 만든 경로를 같은 입력에서 비교합니다. 실행이 끝났는지, 오류가 기대대로 검출됐는지, 해결 경로가 계약을 만족하는지를 따로 확인합니다. 각 코드의 실측·호스트 실행·소프트웨어 모형 범위는 해당 안내에 적었습니다.

| 분야 | 코드와 실행 방법 | 관측과 해설 |
| --- | --- | --- |
| C·C++·펌웨어 | [native_firmware](native_firmware/README.md): C11·C++17 세 프로그램과 빌드 러너 | 프레임 길이 16,496조합, 뷰·소유 복사, 여섯 공개 순서, SPSC 순차 wrap 검사 |
| 칩·시험 데이터 | [chip](chip/README.md): 표준 라이브러리 Python 실행기 | 레이아웃·누산 폭·명시적 wrap, 제품 ID 연결과 오판율, 분리된 통과 구간 |
| AI 학습·배포·평가 | [ai](ai/README.md): 작은 합성 모델 두 실행기 | 특성 순서·저장 scaler·입력 거부, 행/group 분할과 평가 정보 유입 |
| RTOS 동시성 | [rtos](rtos/README.md): 결정적 태스크·알림 모델 | 우선순위 상속·마감시간, 검사/대기 사이의 resume 유실과 누적 알림 |
| CAN 장애·수신 계약 | [can](can/README.md): 합성 컨트롤러·프레임 trace 실행기 | 복구 요청/확인/횟수 제한, ID·길이·순번·나이와 상태 갱신 |
| 칩 시험 자동화 | [chip_automation](chip_automation/README.md): 실제 자식프로그램과 판정 러너 | 종료0·PASS 문자열의 거짓 승인, timeout·오래된 결과·해시·누락·수치 오류 |
| 인터럽트·DMA·캐시 | [interrupt_dma](interrupt_dma/README.md): W1C·완료 인계와 write-back 캐시 모델 | 잘못 지워진 상태, 소유권 위반, 오래된 TX/RX와 공유 line 손실 |
| SPI·I2C | [serial_buses](serial_buses/README.md): 플래시·EEPROM 전송 모델 | CS·dummy·샘플링과 묶음 읽기·NACK 주체·중간 실패 |
| RTL·기준 모델 | [rtl_reference](rtl_reference/README.md): SystemVerilog 내적기·테스트벤치·Python 비교 | 부호·비트 폭·전송 수락·지연·리셋과 결과 대응 |
| UART·Ethernet·UDP | [uart_ethernet](uart_ethernet/README.md): 스트림 파서·원시 캡처 해석·로컬 socket | 분할·병합 수신, 길이·padding·checksum, 데이터그램 경계 |
| 워치독·리셋 | [watchdog_reset](watchdog_reset/README.md): 작업 진행·감시 구간·원인 플래그 모델 | 멈춘 task 은폐·오래된 완료 표시·tick 순환·capture-before-clear |
| CDC·비동기 FIFO | [cdc_async_fifo](cdc_async_fifo/README.md): dual-clock SystemVerilog·Python 기준 큐 | Gray 포인터 동기화·full/empty·순서·reset flush와 기능 오류 주입 |
| USB·PCIe 전송 | [usb_pcie](usb_pcie/README.md): 부분 전송·재시도·분할 completion 모델 | 실제 길이·명령 ID·연결 세대와 tag·주소·응답 완성 |
| 부트로더·펌웨어 업데이트 | [firmware_update](firmware_update/README.md): 파일 기반 A/B 슬롯·재시작 검사 | 기록 중단·이미지 검사·시험 부팅·확정과 롤백 |
| DDR 명령·메모리 패턴 | [ddr_validation](ddr_validation/README.md): SV 명령 fixture·Python 감시기 | 시간 간격·refresh·주소와 데이터 결함·응답 누락·패턴 한계 |

[설계와 검증 사례](../../설계와검증사례_engineering-cases/README.md)에서 원인과 해결을 읽고, [현장 계측과 검증](../../현장계측과검증_measurement-validation/README.md)에서 장비·펌웨어·칩 시험 조건으로 연결합니다.

## 기록 보존

실행기는 매번 새로운 결과 폴더를 요구합니다. 입력·소스 해시, 환경, 명령과 종료 상태를 남기며, 제품 FAIL을 재현했다고 실행기 자체가 실패한 것으로 합치지 않습니다. C/C++ 검사는 NDEBUG가 켜진 채라면 빌드를 거부합니다. 장비에 접속하지 않는 Python 모형, 실제 로컬 UDP socket, HDL 실행을 각 안내에서 구분합니다.

## English

Fifteen sets of runnable examples compare faulty controls and intended fixes: native contracts, chip analysis, AI evaluation, RTOS concurrency, CAN, subprocess reports, interrupt/DMA/cache ownership, SPI/I2C, UART/Ethernet/UDP, watchdog/reset, RTL/reference and CDC/asynchronous FIFO comparison, USB/PCIe, file-backed firmware updates and DDR command/pattern checks. New output directories preserve earlier failures. HDL simulation, actual host child processes, deterministic software models and physical measurements have distinct scopes.
