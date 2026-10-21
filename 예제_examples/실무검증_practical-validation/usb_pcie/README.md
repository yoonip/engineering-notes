# USB 부분 전송과 PCIe 분할 응답 / USB partial transfers and PCIe completions

Python 표준 라이브러리로 실행하는 합성 호스트 계약입니다. 실제 USB 장치·libusb·PCIe root port·FPGA IP·DMA·물리 링크를 실행하지 않습니다. 다른 소켓 전송으로 이를 대신하지도 않습니다.

| 파일 | 내용 |
| --- | --- |
| [models.py](models.py) | Bulk 결과·자체 레코드·응용 명령 ID·callback 소유권·PCIe 요청별 조립입니다. |
| [fixtures.json](fixtures.json) | 직접 만든 API 결과·해독된 Completion 필드·리터럴 기대 데이터/상태입니다. |
| [run_cases.py](run_cases.py) | 정상·경계·입력 거부·의도적 변이 검사와 JSON/환경/해시 기록입니다. |

[USB 사례](../../../설계와검증사례_engineering-cases/USB의부분전송과중복없는복구_usb-bulk-recovery.md) · [PCIe 사례](../../../설계와검증사례_engineering-cases/PCIe의태그와분할응답_pcie-split-completions.md) · [검증 기록](../../../설계와검증사례_engineering-cases/검증기록_evidence/USB와PCIe전송계약검증_20261021.md)

## 실행

Python 3.10 이상에서 이 폴더를 작업 경로로 실행합니다. 외부 패키지가 필요하지 않습니다. 아래는 매번 다른 새 출력 폴더를 쓰는 명령의 예입니다.

```powershell
python -X utf8 -B run_cases.py --output C:/temp/usb-pcie-normal-new
python -X utf8 -B -O run_cases.py --output C:/temp/usb-pcie-optimized-new
python -X utf8 -B -O run_cases.py --mutation usb-drop-timeout --output C:/temp/usb-prefix-fault-new
python -X utf8 -B -O run_cases.py --mutation usb-new-command-id --output C:/temp/usb-retry-fault-new
python -X utf8 -B -O run_cases.py --mutation pcie-ignore-byte-count --output C:/temp/pcie-count-fault-new
python -X utf8 -B -O run_cases.py --mutation pcie-finish-first --output C:/temp/pcie-early-fault-new
```

정상은 PASS·종료 0, 의도한 변이는 ERROR·종료 1입니다. 기존 결과 폴더는 종료 2로 거부합니다. 결과 JSON에는 소스·입력 SHA-256, 실제 Python·OS·명령 인수·시각과 관측값이 있습니다. `require()`는 명시적 예외를 사용하므로 -O에서도 검사가 남습니다.

## USB 계약

BulkRecords는 한 연결 세대의 순서가 유지된 IN 결과를 받아 자체 6바이트 레코드를 조립합니다. status와 actual_length를 함께 확인하고 COMPLETED/TIMED_OUT의 prefix만 보존합니다. 취소·STALL 등 prefix의 응용 폐기는 자체 정책입니다. NO_DEVICE/CANCELLED 결과를 받더라도 이미 보존한 partial buffer를 자동 소거하지 않습니다. UsbEndpoint와 자동 연결된 파이프라인이 아니므로 재연결 때 호출자가 새 collector를 만들고 옛 부분 레코드를 폐기해야 합니다. short packet을 모든 응용 메시지의 끝으로 가정하지 않으며 실제 packet은 생성하지 않습니다. 입력 상한 4096은 이 예제의 제한입니다.

IdempotentDevice는 같은 command ID·같은 delta에 저장된 결과를 돌려주는 자체 장치 프로토콜입니다. ACK-IN STALL 뒤 같은 ID41을 쓰면 값 17·적용 1회, 새 ID42를 쓰면 값 24·적용 2회입니다. 실제 장치의 ACK·중복 처리·지속 저장 계약이 없는 임의 명령에 이 성질을 보장하지 않습니다.

UsbEndpoint의 token=(generation,serial)은 callback 소유권을 구분합니다. cancel 요청 뒤에도 pending이며, disconnect는 명시적 session 사건입니다. 실제 USB 주소를 읽어 generation을 자동 결정한 기능이 아닙니다. 옛 callback은 옛 slot만 반환하고 새 session 데이터에 섞지 않습니다. slot은 실제 메모리 할당이 아닌 소유 표시입니다. requested/actual의 용량 검사는 bulk_result가 담당하며, endpoint 상태 모델은 제출 buffer의 주소·용량을 구현하지 않습니다. 취소 경쟁은 지정된 사건 순서만 재현하며 다중 thread·실제 메모리 해제는 실행하지 않습니다.

## PCIe 계약

단일 Requester·tag 0~31·32비트 주소·길이 4~256바이트·DW 정렬·전체 byte-enable·SC·MPS 128·RCB 128의 해독된 필드만 지원합니다. tag 5의 32바이트는 16+16, tag 9의 8바이트는 그 사이에 도착합니다. Byte Count는 현재 조각 포함 남은 양, Lower Address는 다음 주소의 하위 7비트입니다. 미완료 buffer와 tag는 재사용하지 않습니다.

RCB는 중간 분할 위치의 경계이며 payload 크기 상한 MPS와 다릅니다. 단일 32바이트가 128 경계를 가로지르는 정상 대조도 있습니다. 4KiB 끝에 맞는 요청과 넘어서는 요청, 최대 256바이트 요청·128바이트 payload도 확인합니다. 원시 TLP·BCM·DW padding·partial byte-enable·4096의 zero 인코딩·Requester ID 다중화·TC·tag 재배정 뒤 비정상 늦은 응답·실제 DMA cache/주소 mapping·timeout·AER·링크는 구현하지 않습니다.

## 짧은 문법 안내

| 문법·함수 | 이 코드에서의 역할 |
| --- | --- |
| import / from ... import | argparse·json 등의 표준 기능과 같은 폴더의 모델을 불러옵니다. |
| def / class / self | 함수·객체 형과 개별 전송의 상태를 정의합니다. |
| [] / {} / () | 리스트·딕셔너리·함수 호출/tuple을 표현합니다. |
| [:6] / del / extend | 앞 6바이트를 꺼내고 소비한 부분을 지우며 새 bytes를 붙입니다. |
| in / not in / any | 상태·tag 존재와 slot 중복 사용을 확인합니다. |
| & / % | 하위 주소 비트를 남기고 정렬·분할 경계를 검사합니다. |
| `**event` | 딕셔너리 필드를 함수의 이름 붙은 인수로 전달합니다. |
| try / except / raise | 입력 형식 오류·전송 계약 거부·검증 실패를 구분합니다. |
| Path.mkdir(exist_ok=False) | 기존 결과를 덮지 않고 새 폴더만 만듭니다. |

## Sources and scope

[libusb 1.0.30 async](https://libusb.sourceforge.io/api-1.0/group__libusb__asyncio.html), [bulk sync](https://libusb.sourceforge.io/api-1.0/group__libusb__syncio.html), [clear_halt](https://libusb.sourceforge.io/api-1.0/group__libusb__dev.html), [PG346 descriptor](https://docs.amd.com/r/3.3-English/pg346-cpm-pcie/Completer-Completion-Descriptor-Format?contentId=pEh4XcohN3uFqiFePvYL_A), [PG054 RCB](https://docs.amd.com/r/en-US/pg054-7series-pcie/Read-Completion-Boundary)를 확인했습니다. 실제 읽은 판본·절과 제외한 기능은 두 사례 본문에 있습니다.

## English

Deterministic synthetic transactions exercise partial USB bulk results, duplicate-safe command retry, callback buffer ownership, and restricted PCIe split-completion accounting. Literal expectations, explicit exceptions under optimization, four failing implementation mutations, and new-output protection connect the code to evidence. Hardware, drivers, raw packets, and physical timing are outside the executed scope.
