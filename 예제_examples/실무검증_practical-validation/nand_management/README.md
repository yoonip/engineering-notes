# NAND 블록·마모·scrub 정책 / NAND blocks, wear and scrub policies

[불량 블록과 마모 분산](../../../설계와검증사례_engineering-cases/NAND의불량블록과마모분산_nand-bad-block-wear.md) · [읽기 징후와 데이터 이동](../../../설계와검증사례_engineering-cases/읽기교란의징후와데이터이동_nand-read-disturb-scrub.md) · [실행 기록](../../../설계와검증사례_engineering-cases/검증기록_evidence/NAND블록과교란모델검사_20261021.md)

## 실행하는 대상

Python 표준 라이브러리로 물리 블록 6개·블록당 페이지 2개·페이지당 4바이트를 관리하는 합성 모델입니다. 실제 NAND geometry, raw 명령, controller/MTD 드라이버, ECC codec, 물리 보드나 전원 차단 시험은 없습니다. 읽기 횟수와 corrected/UE 입력은 관리 정책의 입력이며 전압·오류율을 계산하지 않습니다.

| 파일 | 내용 |
|---|---|
| [models.py](models.py) | program·erase·bad 상태, 전체 블록 매핑, 동적/정적 이동과 scrub 정책입니다. |
| [fixtures.json](fixtures.json) | 직접 적은 이동 위치·소거 횟수·바이트 수·실패 결과의 리터럴입니다. |
| [runner.py](runner.py) | 두 마모 정책, 읽기 임계값, 이동 오류 4종, 33개 입력 거부, 바이트값 256개 경계를 검사합니다. |

모든 데이터는 자체 시험용입니다. 관리 정보는 Python 메모리에만 있으며 OOB marker·영속 BBT·매핑 저널·정전 원자성·재시작 복구를 구현하지 않습니다. `seed()`의 초기 자료와 소거 이력은 fixture 준비이고 `reset_metrics()` 이후를 비교 창으로 사용합니다.

## 블록과 매핑의 계약

논리 블록 번호 0~2는 물리 블록 하나씩을 가리킵니다. 각 호스트 쓰기는 두 페이지 전체를 대체합니다. 여러 논리 페이지를 한 블록에 섞는 일반 SSD FTL이나 부분 쓰기 GC는 없습니다. 새 목적지를 프로그램하고 검증한 다음에만 매핑을 바꾸고, 마지막에 옛 블록을 소거합니다.

| 상태·조건 | 처리 |
|---|---|
| FACTORY_BAD | 초기 입력으로 받은 출하 불량이며 free pool에서 제외합니다. 실제 marker를 스캔하지 않습니다. |
| GROWN_BAD | 주입한 program/erase 실패 또는 검증 실패로 격리한 블록입니다. 재사용하지 않습니다. |
| GOOD | 위 두 불량 상태가 아니라는 관리 분류입니다. UE가 있으면 별도의 unreadable 표시에 의해 자료 공개가 막힙니다. |
| free | 매핑되지 않고 프로그램한 페이지가 없으며 GOOD인 블록만 해당합니다. |
| 목적지 program/검증 실패 | 새 목적지를 격리하고 원래 매핑·원본 배열·원본 소거 횟수를 보존합니다. |
| 매핑 변경 후 옛 블록 erase 실패 | 새 데이터는 유지하고 옛 블록을 GROWN_BAD로 격리합니다. 이동 실패와 구분합니다. |

erase는 블록의 비트를 1로 되돌리고 program은 1→0만 허용합니다. 여기에 페이지당 한 erase 주기에서 program 1회, 페이지 0→1의 순서라는 자체 제한을 더했습니다. 일부 실제 NAND의 partial-page program 허용 횟수를 구현한 것이 아닙니다. `F0→FF`는 ERASE_REQUIRED, `F0→E0`도 같은 페이지에 다시 쓰면 PAGE_ALREADY_PROGRAMMED로 거부됩니다. erase 뒤에는 다시 쓸 수 있습니다.

## 마모와 쓰기량을 함께 비교합니다

factory bad 블록 5를 빼고 초기 소거 이력을 `[0,4,4,4,4]`로 가정합니다. 변하지 않는 cold 자료는 블록 0, 갱신하는 hot 자료는 블록 1에 놓습니다. 동적 선택은 비어 있는 블록 중 소거 횟수가 가장 작은 위치를 고르고, 같으면 번호가 작은 위치를 고릅니다. 정적 비교는 처음에 cold 자료를 소거 횟수가 높은 free 블록 2로 한 번 옮긴 뒤 같은 hot 갱신 네 번을 실행합니다.

| 비교 창 결과 | 동적 선택 | 정적 이동 1회 후 동적 선택 |
|---|---|---|
| hot 목적지 순서 | 2→3→4→1입니다. | 0→3→0→4입니다. |
| 정상 5블록의 소거 이력 | `[0,5,5,5,5]`입니다. | `[3,5,4,5,4]`입니다. |
| 최대−최소 | 5입니다. | 2입니다. |
| 성공 호스트 쓰기 | 32바이트입니다. | 32바이트입니다. |
| program 시도 자료량 | 32바이트입니다. | 40바이트입니다. |
| 자료량 비율 | 1.0입니다. | 1.25입니다. |

`program_attempt_bytes`는 실패도 포함해 발행한 페이지 자료 길이를 셉니다. 실패가 있으면 실제 프로그램된 비트 수를 뜻하지 않습니다. 위 비교 창에는 실패가 없으므로 `32/32`, `(32+8)/32`로 추가 복사 비용을 비교할 수 있습니다. 성공한 호스트 자료만 `host_bytes`에 셉니다. seed, ECC/OOB, 매핑 기록, erase, 읽기량은 이 비율의 분자에 넣지 않았으므로 제품 전체 WAF 측정값이 아닙니다. erase 시도 4회와 5회도 별도로 기록합니다.

## 읽기 징후와 scrub

기본 자체 정책은 물리 페이지 읽기 횟수 4회 이상 또는 한 읽기에서 관측한 정정 비트 수의 블록 내 최댓값 2 이상이면 이동을 검토합니다. 두 값은 작은 반례를 보이기 위한 숫자이며 어떤 제품의 정격도 아닙니다. `corrected_max`는 정정 횟수의 합계가 아닙니다. 호스트 읽기뿐 아니라 원본 복사와 목적지 검증 읽기도 `reads`에 포함합니다. 성공 이동 뒤 새 목적지는 검증 읽기 2회가 이미 기록되어 있습니다.

CE(Correctable Error)는 이 입력에서 정정 가능한 읽기, UE(Uncorrectable Error)는 신뢰 가능한 자료를 얻지 못했다는 입력입니다. ECC 계산·bit flip 생성은 하지 않습니다. 반복 읽기, retention, 마모 등 원인을 이 값 하나로 확정하지 않습니다. 이 보수 정책은 한 페이지 UE가 오면 그 물리 블록의 자료 공개를 모두 막고 이후에도 유지합니다. UE 반응이 모든 실제 장치에서 블록 전체 불량을 뜻한다는 주장은 아닙니다.

scrub은 정정 가능한 원본을 읽어 새 블록에 쓰고 검증한 뒤 매핑을 바꿉니다. UE가 발견되면 반환 자료는 `None`, 이동 결과는 SOURCE_UE이며 원본을 소거하지 않습니다. program·검증 실패도 원래 매핑과 원본을 유지합니다. 이때 원본 배열이 바뀌지 않았다는 검사와 그 데이터가 복구 가능하다는 판단은 다릅니다. UE 복구·중복 복사본 선택·관리 정보의 crash recovery는 구현하지 않습니다.

## 실행과 의도적 오류

이 폴더에서 설치된 Python 3.12로 실행합니다. C:/temp는 독자가 정할 새 결과 경로의 예입니다.

```powershell
python -X utf8 -B runner.py --out C:/temp/nand-normal-new
python -X utf8 -B -O runner.py --out C:/temp/nand-optimized-new
python -X utf8 -B runner.py --mutation early-remap --out C:/temp/nand-map-fault-new
```

정상은 PASS/exit 0이며 마지막 오류 구현은 ERROR/exit 1이어야 합니다. 결과 JSON에는 실제 관측·환경·인자·소스/fixture SHA-256이 들어갑니다. 기존 출력 폴더와 잘못된 fixture는 exit 2로 거부됩니다. `require()`가 직접 예외를 발생시켜 `-O`에서도 검사가 남습니다.

| 오류 변이 | 발견할 차이 |
|---|---|
| nand-zero-to-one | erase 없이 0→1을 허용합니다. |
| reuse-bad | 불량 블록을 free pool에 넣습니다. |
| early-remap | 목적지 program·검증 전에 매핑을 바꿉니다. |
| publish-ue | UE인 읽기의 자료를 공개합니다. |
| skip-scrub | 읽기 횟수·CE 임계값을 무시합니다. |

2026-10-21 실행에서 정상 2모드의 관측값은 같았고 다섯 변이는 두 모드에서 모두 검출됐습니다. 결과 보존과 별도 API 리터럴까지 포함한 실행 근거는 연결한 기록에 있습니다.

## 문법과 자료 구조

```python
from models import Manager                    # import는 모델 클래스를 가져옵니다.
device = Manager(read_limit=4, ce_limit=2)      # 클래스 호출로 객체를 만들고 이름 인자를 전달합니다.
device.seed(0, 0, ['cafebabe', '11223344'])      # []는 두 페이지 문자열을 담는 리스트입니다.
row = device.read_page(0, 0, corrected=2)       # 점 표기로 메서드를 호출하고 사전 결과를 저장합니다.
if row['scrub_due']:                          # []로 사전 값을 읽어 if 조건을 검사합니다.
    result = device.scrub(0)                  # 들여쓰기는 조건이 참일 때 수행할 범위입니다.
```

`def`는 함수를 정의하고 `self`는 객체 자신입니다. `{}`는 사전, `set()`은 중복 없는 집합입니다. `field(default_factory=...)`는 블록마다 별도 리스트·집합을 만들어 공유 변경을 피합니다. `min(..., key=...)`는 비교 기준 함수를 써서 블록을 선택합니다. `zip`은 이전·새 바이트를 짝짓고 `&`는 비트 AND입니다. `raise`와 `try/except`는 잘못된 입력을 거부하고 그 이유를 검사합니다.

## 확인 문제

1. 목적지의 첫 페이지만 프로그램한 뒤 실패하면 매핑을 바꿔도 되나요? 답: 안 됩니다. 원래 매핑을 유지하고 실패 목적지를 제외합니다.
2. 소거 횟수 차이가 줄었으므로 추가 쓰기 비용이 없나요? 답: 아닙니다. 이 입력에서는 cold 복사 8바이트가 추가됐습니다.
3. UE의 원본 배열이 그대로이면 읽은 데이터를 공개해도 되나요? 답: 안 됩니다. 배열 보존과 자료의 신뢰성은 별도 조건입니다.

## English

This deterministic standard-library model manages six teaching blocks with two four-byte pages each. It does not run NAND commands, an ECC decoder, an MTD driver or a physical board. Factory and grown bad states are excluded from the free pool. Copy and verification precede mapping publication; failed destinations retain the source mapping. Cleanup erase failure after publication retires the old block while keeping the new mapping.

One fixed workload reduces erase-count spread from five to two by adding a static move, but program-attempt bytes rise from 32 to 40 for 32 committed host bytes. The failure-free ratios 1.0 and 1.25 exclude metadata and initial state. Read-count and corrected-error thresholds are teaching policy, not universal NAND limits. UE data is withheld. Target verification reads count toward telemetry. See the cases for primary sources and the evidence for hashes, rejected inputs and mutation runs.
