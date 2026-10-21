# 저장장치의 완료·오류·영속성 / Storage completion, errors and persistence

[NVMe 사례](../../../설계와검증사례_engineering-cases/NVMe의쓰기완료와영속성_nvme-write-persistence.md) · [eMMC·SD 사례](../../../설계와검증사례_engineering-cases/eMMC와SD의busy와쓰기실패_emmc-sd-write-status.md) · [실행 기록](../../../설계와검증사례_engineering-cases/검증기록_evidence/저장장치완료와영속성검사_20261021.md)

## 무엇을 실행하나요

Python 표준 라이브러리로 이미 해석한 명령·완료·상태 관측값을 처리합니다. raw NVMe/MMC/SD 명령, 운영체제 block API, 실제 저장장치 접근은 없습니다. `power_loss()`는 사전의 휘발 항목을 지우는 결정적 사건입니다. 이후 `read()`는 남은 내부 `media`를 조사하며, 전원이 꺼진 장치에 읽기 명령을 보내는 동작이 아닙니다.

| 파일 | 역할 |
|---|---|
| [models.py](models.py) | NVMe CID 매칭·완료·캐시, 카드 busy·상태·캐시 모델입니다. |
| [fixtures.json](fixtures.json) | 직접 적은 입력과 리터럴 기대값 12개 시나리오입니다. |
| [run_cases.py](run_cases.py) | 72개 단계의 반환값, 42개 입력 거부, 24개 경계와 별도 리터럴을 검사합니다. |

교육 단위는 8개 블록×4바이트=32바이트입니다. 실제 NVMe LBA 형식이나 카드 sector 크기가 아닙니다. `media`는 전원 상실 후 유지되는 자체 상태, `cache`는 이번 fault profile에서 잃는 상태입니다. 실제 장치는 배경 destage나 전원 보호 회로 때문에 다른 결과를 보일 수 있습니다. 여기서는 안전하다고 단정할 수 없는 경로의 반례를 고정했습니다.

## NVMe의 입력 계약

단일 Submission Queue와 namespace만 사용합니다. `submit_write(cid, lba, payload, fua)`는 0~65535 CID를 받고 진행 중 CID의 중복, 겹치는 진행 중 쓰기, 4개를 넘는 동시 명령을 거부합니다. CID는 Command Identifier이며, 실제 다중 SQ에서는 SQID와 함께 완료를 식별합니다. 같은 CID는 정상 완료 후 재사용할 수 있지만 reset 뒤 오래된 CQE·phase tag·세대 판정은 구현하지 않습니다.

VWC가 켜져 있고 FUA가 없는 성공 쓰기는 `cache`에만 들어갑니다. `durable_ack=false`는 호스트가 아직 영속성을 승인하지 않는다는 자체 판정입니다. FUA 성공은 해당 쓰기를 `media`에 반영합니다. 다른 LBA의 캐시를 함께 비우지 않습니다. Flush는 앞선 명령이 모두 완료된 뒤에만 제출하도록 제한했고, 진행 중 새 쓰기도 막습니다. 이 직렬화는 예제의 호스트 정책입니다. 규격이 모든 Flush 전후에 이 정책을 강제한다는 뜻이 아닙니다.

실패 완료는 `FAILED_UNCERTAIN`이며 자동 rollback을 주장하지 않습니다. `fault_prefix`는 실패 장치가 몇 블록을 내부적으로 바꿨는지 주입하는 시험 인자입니다. CQE에 그런 부분 완료 길이가 있다는 뜻이 아닙니다. 정상·정전 원자성 보장, AWUN/AWUPF, metadata, sanitize, FTL과 NAND는 모델에 없습니다. 실패 Flush의 내부 효과를 0으로 정한 것도 이 fixture의 선택입니다.

## 카드의 입력 계약

`family='emmc'/'sd'`는 기능을 확인해야 할 대상의 구분입니다. 두 카드에 같은 wire 명령이나 같은 레지스터를 쓰지 않습니다. `cache_supported`는 실제로 확인했다고 가정한 기능 입력이고, 기본은 꺼짐입니다. 기능이 없는 카드의 `enable_cache()`는 거부됩니다. eMMC CACHE_CTRL과 SD의 확장 기능을 raw 비트로 해석하는 코드는 없습니다.

카드의 `request_id`는 자체 추적 번호입니다. eMMC/SD의 CID는 Card Identification 레지스터이므로 NVMe Command Identifier와 혼동하지 않습니다. 여기서는 쓰기 하나씩 처리합니다.

1. busy가 남으면 `WAIT_BUSY`입니다.
2. busy가 풀려도 ready가 거짓이거나 state가 TRAN이 아니면 `WAIT_STATUS`입니다.
3. 관측한 WRITE_ERROR/WP_VIOLATION은 `FAILED_UNCERTAIN`입니다. 코드에서는 오류를 먼저 판정합니다.
4. 오류 없이 조건을 만족하면 쓰기 성공입니다. 캐시가 켜져 있으면 아직 영속성을 승인하지 않습니다.

busy와 상태를 모두 받는 것은 보수적인 자체 관측 정책입니다. 모든 실제 호스트가 매번 DAT0와 CMD13을 똑같이 읽어야 한다는 규칙으로 일반화하지 않습니다. `flush(success)`의 인자는 장치별 절차와 최종 오류 검사가 이미 끝났다는 decoded 결과입니다. Flush의 busy 파형·timeout·레지스터 처리는 모델 밖입니다.

`timeout()`은 명시적으로 넣는 시험 사건이며 실제 타이머를 실행하지 않습니다. timeout·쓰기 오류·실패 Flush 뒤에는 새 쓰기를 막는 `recovery_required`가 남습니다. 재초기화·재시도·파일시스템 복구는 구현하지 않습니다. 단순 재시도로 이전 실패가 무효가 되거나 다중 블록 쓰기가 원자적으로 바뀌지는 않습니다.

## 실행과 결과

Python 3.12와 표준 라이브러리를 사용했습니다. 이 폴더에서 설치된 Python 실행 파일로 실행하며 매번 새 출력 폴더를 고릅니다. 아래 `python`은 그 실행 파일을 가리켜야 합니다. 확인한 환경·인자·종료값은 실행 기록에 적었습니다. C:/temp는 독자가 정할 새 경로의 예입니다.

```powershell
python -X utf8 -B run_cases.py --out C:/temp/storage-normal-01
python -X utf8 -B -O run_cases.py --out C:/temp/storage-optimized-01
python -X utf8 -B run_cases.py --mutation nvme-fua-flushes-all --out C:/temp/storage-fault-01
```

정상 구현은 exit 0/PASS이고, 마지막 명령은 오류 구현을 검사가 발견하여 exit 1/ERROR가 되어야 합니다. `result.json`에는 실행 환경·명령 인자·소스/fixture SHA-256·실제 반환값이 들어갑니다. 기존 출력 폴더와 잘못된 fixture는 exit 2로 거부됩니다. `require()`가 직접 예외를 발생시키므로 `-O`에서도 검사가 남습니다. 공개 폴더에는 실행 결과를 덮어 넣지 않습니다.

| 의도적으로 틀린 구현 | 리터럴 검사가 발견하는 차이 |
|---|---|
| `nvme-completion-is-durable` | 일반 캐시 쓰기에 durable 승인을 잘못 반환합니다. |
| `nvme-fua-flushes-all` | FUA와 무관한 LBA 0의 `01020304`까지 남습니다. |
| `nvme-ignore-flush-error` | ABORTED Flush를 성공·영속성 승인으로 바꿉니다. |
| `card-ignore-status-error` | 쓰기 오류를 성공으로 승인합니다. |
| `card-busy-is-done` | busy만 풀린 PRG 상태를 성공으로 바꿉니다. |

2026-10-21 확인에서는 정상·`-O` 2회가 PASS였고, 5개 변이를 두 모드에서 실행한 10회가 모두 예상한 AssertionError/exit 1이었습니다. 결과 폴더 재사용은 exit 2였으며 기존 JSON 바이트가 유지되었습니다. 이는 합성 호스트 계약의 결과이며 저장장치 인증이나 실물 전원 차단 시험 결과가 아닙니다.

## 짧은 문법과 판정 예

```python
from models import Nvme                 # from/import는 모델 파일의 클래스를 가져옵니다.
device = Nvme(vwc=True)                 # 클래스 호출로 객체를 만들고 이름 인자를 전달합니다.
device.submit_write(7, 0, ['aabbccdd'])  # []는 블록 목록이며 문자열은 4바이트의 16진수 표현입니다.
result = device.complete(7, 'SUCCESS')  # 점 표기로 메서드를 호출하고 반환 사전을 저장합니다.
if not result['durable_ack']:           # []로 사전 값을 읽고 not으로 거짓 여부를 검사합니다.
    device.submit_flush(8)             # 들여쓰기는 if 조건 안에서 실행할 범위를 정합니다.
    device.complete(8, 'SUCCESS')       # 같은 CID 8의 Flush 완료를 관측합니다.
device.power_loss()                    # ()는 인자 없는 호출이며 휘발 캐시를 지웁니다.
remaining = device.read(0)             # 내부 media 관측값은 'aabbccdd'입니다.
```

소스의 `def`는 함수를 정의하고 `self`는 해당 객체를 받습니다. `{}`는 사전, `set()`은 중복 없는 집합, `in`은 포함 여부입니다. `@dataclass(frozen=True)`는 명령 필드의 재대입을 막는 자료 클래스를 만듭니다. 내부 사전까지 재귀적으로 불변으로 만드는 기능은 아니며 이 모델은 제출 이후 명령 데이터를 바꾸지 않습니다. `raise`는 오류를 알리고 `try/except`는 정해진 오류를 받아 검사합니다. 결과의 원시 데이터와 호스트 승인 여부를 별도 필드로 두는 이유도 여기에 있습니다.

## 확인 문제

1. `read()`로 새 값이 보이면 영속성 검사를 생략해도 되나요? 답: 안 됩니다. 같은 값이 휘발 캐시에서 나올 수 있습니다.
2. FUA 쓰기 전에 완료된 다른 LBA가 반드시 함께 남나요? 답: 아닙니다. 이 모델의 반례에서는 그 LBA가 사라집니다.
3. 카드 timeout은 쓰기가 전혀 반영되지 않았다는 뜻인가요? 답: 아닙니다. 완료를 확정하지 못한 상태이며 주입한 반례에서는 일부가 남습니다.

## English

This standard-library exercise runs decoded synthetic host contracts, not NVMe/MMC/SD commands or physical devices. Eight four-byte blocks make the state visible; they are not device sector formats. Post-loss reads inspect internal persistent media. A volatile cached write can complete and be readable without a durability acknowledgement. FUA covers its own write, while the example serializes completed writes before a successful Flush. Failed writes have explicitly injected internal effects, never a fabricated CQE byte count.

The card policy separates busy, ready/state, error status and cache persistence. eMMC and SD share a teaching interface, not an on-wire command format. Cache capabilities must be supplied explicitly. The flush result is already decoded after device-specific completion checks; recovery and physical timing are outside scope. Twelve literal scenarios, forty-two rejected inputs and twenty-four boundaries pass in normal and optimized Python. Five faulty implementations are detected in both modes. See the linked cases for reasoning and primary sources, and the evidence page for exact commands and hashes.
