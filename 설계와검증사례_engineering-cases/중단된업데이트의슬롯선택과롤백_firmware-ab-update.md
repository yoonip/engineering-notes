# 중단된 업데이트의 슬롯 선택과 롤백 / A/B image selection after interrupted updates

새 파일을 모두 받았다는 사실과 그 이미지를 다음 부팅의 확정 대상으로 삼아도 된다는 사실은 다릅니다. 길이·바이트 손상 확인, 게시한 메타데이터, 첫 시험 선택, 업무 checkpoint 뒤의 확정을 구분해야 합니다. 이 사례는 실제 파일 I/O와 새 Python 프로세스로 그 경계를 비교합니다.

[실행 코드와 입력](../예제_examples/실무검증_practical-validation/firmware_update/README.md), [모형](../예제_examples/실무검증_practical-validation/firmware_update/models.py), [검사](../예제_examples/실무검증_practical-validation/firmware_update/verify.py), [실행 기록](검증기록_evidence/펌웨어업데이트중단과복구검사_20261021.md)을 연결했습니다. 직접 만든 바이트 이미지와 오류 경로이며 실제 제품 장애 보고가 아닙니다. 모델의 `BOOT`는 파일 선택 결과입니다. 실행 가능한 firmware·MCU·MCUboot·Linux kernel을 부팅하지 않았습니다.

## 1. 기존 A를 보존한 채 B를 준비합니다

A/B는 두 이미지 공간을 번갈아 사용하는 방식입니다. 모형의 기존 A는 8바이트, 새 B는 12바이트이고 각 슬롯의 자체 상한은 32바이트입니다. 실제 flash 주소나 erase 크기를 표현한 수치가 아닙니다. 두 이미지를 동시에 보관하는 payload만 8+12=20바이트이며 메타데이터 공간은 별도입니다.

확정된 A를 지운 뒤 B를 받기 시작하면 첫 바이트도 다 쓰기 전에 기존 복구 경로를 잃을 수 있습니다. 수정 경로는 inactive B만 기록하고, 받은 길이가 12인지와 선언한 SHA-256이 맞는지를 확인한 뒤 후보를 게시합니다. 이미지 한 바이트를 바꾼 채 해시는 그대로 두면 거부합니다. 11/13바이트 입력도 길이가 맞지 않아 거부하고 A는 그대로 선택할 수 있습니다.

```python
target = "B" if active == "A" else "A"  # 조건 표현식으로 현재 확정 슬롯의 반대쪽을 고릅니다.
data = (root / f"slot{target}.bin").read_bytes()  # /는 Path 연결, f 문자열은 슬롯 이름을 넣습니다.
require(len(data) == manifest["length"], "image length mismatch")  # len과 []로 실제 길이·선언 길이를 비교합니다.
require(hashlib.sha256(data).hexdigest() == manifest["sha256"], "image SHA256 mismatch")  # 바이트 지문을 비교합니다.
```

이 발췌의 길이·해시는 데이터 일치 검사입니다. firmware의 명령어가 올바른지, 초기 stack/entry 주소가 유효한지, kernel·DTB·rootfs가 호환되는지는 검사하지 않습니다. 그런 전제는 실제 업데이트 대상과 부팅 규약에서 추가해야 합니다.

## 2. 복사·시험 선택·확정을 다른 상태로 둡니다

모형의 generation은 메타데이터 기록의 순서를 나타내는 정수입니다. 이미지의 release version이나 보안 등급이 아닙니다. active는 마지막 확정 슬롯, pending은 아직 확정하지 않은 후보, attempted는 후보를 한 번 선택했다고 남긴 표시입니다.

| 상태 | generation | active/pending | 다음 선택 |
| --- | ---: | --- | --- |
| 기존 상태 | 0 | A/없음 | A를 stable로 선택합니다. |
| B 기록·검증 뒤 게시 | 1 | A/B, attempted=false | 시험 선택을 준비합니다. |
| 시험 선택 표시 기록 완료 | 2 | A/B, attempted=true | B를 trial로 선택합니다. |
| 업무 checkpoint 뒤 확정 | 3 | B/없음 | 다음 재시작에서도 B입니다. |
| 확정 없이 재시작 | 3 | A/없음 | A로 rollback합니다. |

시험 표시를 먼저 기록한 뒤 B를 선택합니다. 반대로 실행한 뒤에 표시하려고 하면 그 사이 중단돼 같은 후보를 무한히 처음인 것처럼 재시도할 수 있습니다. 기록은 끝났지만 실제 선택을 반환하기 전에 중단됐다면 다음 재시작은 보수적으로 A로 돌아갑니다. 시험을 실제 수행했는지 추측해 재시도하는 대신 정한 계약을 따릅니다.

confirm은 pending·attempted와 외부의 `application_ok` checkpoint를 모두 요구합니다. 모형 CLI의 `--application-ok`는 그 전제를 선언하는 입력이며 실제 자가진단을 실행한 결과는 아닙니다. 실제 제품은 저장장치·주요 서비스·주변장치·데이터 호환성을 어떤 조건에서 확인할지 정해야 합니다. 파일 해시만 맞았다는 이유로 이 업무 조건까지 참으로 만들지 않습니다.

MCUboot v2.2.0은 test/revert와 이미지의 “OK” 표시, direct-XIP 등 서로 다른 전략을 설명합니다. 이 글은 그 상태 구분을 참고했으며 MCUboot의 image trailer·swap·서명 형식을 재구현하지 않습니다. 실제 방식에 따라 새 이미지를 원래 primary 주소로 옮기거나 각 슬롯에서 실행할 수 있도록 빌드해야 합니다. [MCUboot v2.2.0 설계 문서](https://github.com/mcu-tools/mcuboot/blob/v2.2.0/docs/design.md)

## 3. 메타데이터 한 부를 덮는 중에도 이전 부가 남습니다

슬롯 B가 온전해도 어느 슬롯이 확정됐는지 알 수 없으면 부팅 결정을 내릴 수 없습니다. 모형은 `record0.json`과 `record1.json` 두 부를 사용합니다. 각 기록은 상태 사전과 그 canonical JSON 바이트의 CRC32를 담습니다. canonical은 키 순서·구분자를 정해 같은 상태가 같은 바이트가 되게 만든다는 뜻입니다.

```python
state["generation"] = previous["generation"] + 1  # 이전 기록보다 큰 순번을 새 사전에 넣습니다.
index = state["generation"] % 2  # %는 나머지이며 0·1 기록을 번갈아 고릅니다.
crc = zlib.crc32(canonical(state))  # CRC32는 정해진 바이트의 오류 검출값입니다.
```

새 기록을 쓰는 동안 직전 유효 기록은 다른 부에 남습니다. 재시작하면 JSON 해석·CRC·상태 schema를 확인한 기록 중 가장 큰 generation을 고릅니다. schema는 슬롯 이름·필드·정수 범위·manifest가 정한 구조에 맞는지 확인하는 규칙입니다. 같은 최대 세대에 서로 다른 유효 기록이 있으면 임의로 하나를 고르지 않고 거부합니다. 두 부 모두 손상됐을 때도 복구가 필요하다고 거부합니다.

이 파일 모형의 원자적 사건은 “완전한 유효 기록이 선택 가능해졌는가”입니다. OS의 파일 쓰기 자체가 전원 상실에 원자적이라는 주장은 아닙니다. CRC도 충돌 가능성이 있고 공격자가 다시 계산할 수 있습니다. 실제 flash에서 두 기록을 같은 erase block에 넣어 동시에 지울 수 있다면 이 모형의 독립 보존 전제부터 깨집니다.

## 4. 실제 파일에 남긴 34개 중단 지점

자식은 정한 prefix를 파일에 쓰고 `flush()`·`os.fsync()` 뒤 `os._exit(23)`으로 끝납니다. 다음 동작은 새 프로세스가 파일을 다시 읽어 수행합니다. Python 사전을 메모리에 남겨 재사용한 비교가 아닙니다. 다만 실제 컴퓨터 전원이나 flash 전원을 끊지 않았고 디렉터리 fsync·erase/program 단위·마모·ECC·컨트롤러 캐시의 내구성은 시험하지 않았습니다.

| 중단 위치 | 선택한 prefix | 재시작의 기대·실제 관측 |
| --- | --- | --- |
| B 이미지 기록 | 0~12바이트의 13개 | 아직 게시하지 않아 A·generation0입니다. |
| 이미지 검증 직후 | 1개 | B가 맞아도 pending이 없어 A입니다. |
| pending 기록 | 0·1·절반·N-1 | 이전 generation0으로 A를 고릅니다. |
| pending 기록 | N, 전체 | generation1을 읽고 trial 표시2를 기록한 뒤 B입니다. |
| trial 표시 기록 | 0·1·절반·N-1 | 완전한 이전 pending으로 시험 선택을 다시 준비합니다. |
| trial 표시 기록 | N | 이미 시도한 후보로 보아 A로 rollback합니다. |
| confirm 기록 | 0·1·절반·N-1 | 마지막 유효 trial 상태를 읽어 A로 rollback합니다. |
| confirm 기록 | N | B를 stable로 선택합니다. |
| rollback 기록 | 0·1·절반·N-1 | 이전 trial 상태에서 rollback을 다시 기록합니다. |
| rollback 기록 | N | 이미 돌아간 A를 stable로 선택합니다. |

13+1+4×5=34개입니다. 이 유한 집합을 모두 실행했으며 모든 메타데이터 바이트 위치나 임의의 전원 오류를 탐색한 것은 아닙니다. N은 해당 기록의 전체 바이트 수입니다. 이번 pending/trial/confirm/rollback은 각각 288/287/289/288바이트였고, N-1은 마지막 JSON 닫는 괄호 앞입니다. 전체를 쓴 뒤의 중단도 넣어 완료 전과 후를 구분했습니다.

기존 A 파일의 바이트는 이 34개에서 보존됐습니다. 기록이 완료된 confirm에서만 메타데이터의 active가 B로 바뀝니다. B를 확정한 뒤 A를 다시 후보로 삼는 재업데이트도 별도 입력에서 실행했습니다.

## 5. 검증기가 네 가지 잘못된 구현을 거부합니다

| 주입한 오류 | 실제 관측한 실패 | 잘못된 전제 |
| --- | --- | --- |
| `erase-active` | 이미지 prefix0에서 A가 빈 파일이 됩니다. 보존 literal이 실패합니다. | 업데이트 전 기존 슬롯을 지워도 된다고 가정합니다. |
| `confirm-early` | pending 전체 기록 뒤 B·stable·generation1입니다. 기대한 B·trial·generation2와 다릅니다. | 복사 검증이 업무 정상 확인을 대신한다고 가정합니다. |
| `skip-hash` | 바이트를 바꾼 입력을 거부3 대신 STAGED·종료0으로 받아들입니다. | 길이 일치만으로 데이터 일치도 보장한다고 가정합니다. |
| `single-record` | pending 기록을 비우는 지점에 유효 metadata가 없어 재시작이 거부됩니다. | 갱신 중인 한 부만으로도 이전 결정을 보존한다고 가정합니다. |

정상 기본/`-O` 실행은 각각 검사 102개·중단 34개·자식 178개로 종료0이며 의미상 결과가 같았습니다. 자식 178개는 정상134·의도한 거부10·중단23종료34로 나뉩니다. 네 mutation은 두 모드에서 모두 부모 종료1이었습니다. 의도한 거부·중단을 정상 업데이트 성공 횟수에 섞지 않습니다.

최신 기록의 CRC만 손상시킨 대조는 이전 유효 부를 사용했습니다. pending B의 데이터가 손상되면 A로 돌아갔고, 확정된 B가 나중에 손상된 경우에는 실행을 거부했습니다. 이 모형은 모든 손상에서 자동으로 다른 슬롯을 복구하는 기능을 약속하지 않습니다. 기존 출력 폴더 재사용은 종료2였고 기존 결과 해시는 유지됐습니다.

## 6. 해시·CRC·보안 순번은 서로 다른 계약입니다

해시를 모르는 공격자를 가정한 검사가 아닙니다. 실제 대조에서 이미지와 manifest 해시를 함께 바꾸면 이 모형은 그 바이트를 trial로 받아들였습니다. 또한 B를 확정한 뒤 예전 A 이미지를 새 후보로 넣는 downgrade도 허용했습니다. 두 결과는 해시가 인증이나 anti-rollback을 대신하지 못함을 보여 주는 한계 대조입니다.

서명은 누가 이미지를 승인했는지 신뢰 키로 확인하는 별도 기능이고, anti-rollback은 허용할 보안 세대와 신뢰된 저장 상태를 연결하는 별도 정책입니다. 여기의 generation은 쓰기 순서라서 보안 counter가 아닙니다. MCUboot v2.2.0의 서명·키 처리와 downgrade prevention 절을 읽어 이 차이를 구분했습니다. [MCUboot 키·이미지 사용 안내](https://github.com/mcu-tools/mcuboot/blob/v2.2.0/docs/readme-zephyr.md)

실제 서명 알고리즘이나 보안 boot chain을 직접 흉내 내서 구현하지 않았습니다. 보드 적용에는 검증된 구현·신뢰 키 보관·이미지 배치와 실제 reset/전원 시험이 필요합니다. 이 실행의 대상은 순서와 파일 상태이며 production secure boot의 검증 결과가 아닙니다.

## 확인 문제

1. B 파일의 길이와 해시가 맞으면 즉시 active를 B로 바꾸어도 됩니까?
2. trial 표시의 전체 기록 뒤 B를 선택하기 전에 중단되면 왜 다음 재시작이 A로 돌아갑니까?
3. CRC가 맞고 generation이 가장 큰 metadata가 있으면 악의적인 downgrade까지 막았습니까?

답: 1. 이 계약에서는 안 됩니다. pending·trial과 업무 checkpoint 뒤 confirm을 구분합니다. 2. 기록은 이미 시도한 상태이므로 보수적으로 rollback합니다. 실제 실행 여부를 추측해 무한 재시도하지 않습니다. 3. 아닙니다. CRC와 쓰기 순번은 인증·신뢰된 보안 counter가 아닙니다.

## English

Separate Python processes write and reopen two disk image files and alternating CRC metadata records. Thirty-four declared prefix/commit interruptions distinguish unpublished data, pending images, attempted trials, confirmations and rollback. The corrected path preserves A while staging B; four mutations fail independent literal checks in normal and optimized runs. Matching attacker-supplied hashes and older images remain accepted, explicitly demonstrating the absence of authentication and anti-rollback. This is a deterministic file/process model, not MCUboot execution, executable firmware boot or flash power-fault testing.
