# RAID 패리티의 부분 갱신과 복원 / RAID parity write hole and reconstruction

XOR 패리티가 있으면 데이터 하나를 복원할 수 있지만, 그 패리티와 남은 데이터가 같은 갱신 상태여야 합니다. 데이터와 패리티가 서로 다른 시점의 값이면 계산식은 맞아도 복원 결과는 틀립니다. 이 사례는 실제 호스트 파일 세 개로 그 차이를 재현하고, 새 stripe 전체와 대상 세대를 보관한 redo 기록으로 새 사본을 만드는 과정을 비교합니다.

[코드와 실행 방법](../예제_examples/실무검증_practical-validation/raid_parity/README.md) · [검증 기록](검증기록_evidence/RAID패리티중단과복원검사_20261021.md) · [메모리와 저장장치](../전자컴퓨터공학_ece/33-메모리저장장치_memory-storage/README.md)

## 패리티가 보관하는 정보

stripe는 여러 저장장치에 나누어 놓는 한 묶음입니다. 여기서는 데이터 D0·D1과 패리티 P를 각각 4바이트 파일 하나로 둡니다. XOR는 대응하는 두 비트가 다르면 1, 같으면 0을 만드는 연산입니다. 같은 값을 두 번 XOR하면 없어지는 성질 때문에 `P = D0 XOR D1`이면 `D1 = P XOR D0`입니다. 단일 멤버의 위치를 알고 그 멤버가 없어진 상황을 다룹니다. 어느 파일의 어느 비트가 틀렸는지 모르는 임의 손상은 다른 문제입니다.

| 상태 | D0 | D1 | P |
| --- | --- | --- | --- |
| 이전 세대 7 | `10111213` | `a0a1a2a3` | `b0b0b0b0` |
| 새 세대 8 | `20212223` | `a0a1a2a3` | `80808080` |
| D0만 갱신 | `20212223` | `a0a1a2a3` | `b0b0b0b0` |
| P만 갱신 | `10111213` | `a0a1a2a3` | `80808080` |

첫 바이트만 계산하면 이전에는 `0x10 XOR 0xa0 = 0xb0`, 새로는 `0x20 XOR 0xa0 = 0x80`입니다. D0만 새 값일 때 옛 P로 D1을 구하면 `0xb0 XOR 0x20 = 0x90`입니다. 나머지 바이트도 `91·92·93`이 되어 `90919293`입니다. P를 먼저 바꾸어도 `0x80 XOR 0x10 = 0x90`이므로 같은 잘못된 결과가 나옵니다. 기록 순서만 반대로 하면 문제가 없어지는 것은 아닙니다.

## 잘못 복원된 값이 그럴듯한 이유

세 멤버가 모두 있을 때에는 `D0 XOR D1 != P`로 불일치를 관측할 수 있습니다. 그러나 D1이 빠진 뒤 남은 두 값만으로 계산하면 새 D1이 그 두 값의 XOR이므로 다시 패리티 식을 만족합니다. 복원 뒤 패리티를 재검사하는 것만으로 원래 D1을 입증할 수 없는 이유입니다. `a0a1a2a3`라는 기대값은 복구 함수가 만든 값이 아니라 [fixture](../예제_examples/실무검증_practical-validation/raid_parity/fixtures.json)에 직접 적은 독립 리터럴입니다.

재현에서는 먼저 정상 seed 폴더를 만들고 각 시험에 사본을 씁니다. D0 우선·P 우선 순서에서 첫 멤버만 기록한 상태를 새 프로세스로 읽습니다. `unsafe-d1`은 위의 XOR 값을 보여 주되 `UNTRUSTED_DIAGNOSTIC`이라는 상태를 붙입니다. 그 뒤 시험용 사본의 D1 파일을 없애 결손을 나타냅니다. 실제 파일을 삭제하지만 모두 새 시험 폴더 안의 합성 자료이며 기존 사용자 볼륨이나 디스크에 접근하지 않습니다.

## dirty 표시와 복구 자료의 차이

dirty는 갱신이 끝나지 않았을 수 있다는 표시입니다. 이 예제의 `meta.json`은 현재 세대 7과 보류 세대 8을 함께 둡니다. dirty만으로는 어떤 멤버가 새 값인지 알 수 없습니다. 세 멤버가 모두 남았더라도 아직 쓰기를 시작하지 않은 상태인지, 두 쓰기를 끝내고 clean 표시만 못 남긴 상태인지를 표시 하나로 추측하지 않습니다. 자체 복구 정책은 유효한 redo가 없으면 `NEEDS_RECOVERY_DATA`로 거부합니다.

metadata는 시험에서 신뢰하는 독립 기준입니다. clean 세대는 1~65534, dirty는 다음 세대도 범위 안에 남도록 1~65533을 지원합니다. 소스 안에서 현재 세대와 로그 세대를 함께 임의로 바꿀 수 있는 공격자를 막지 않습니다. 서명·보호된 monotonic counter·독립 관리 서버도 없습니다. 여기서 세대 검사는 온전한 옛 로그를 실수로 적용하는 오류를 거부하는 계약이며 보안상 rollback 방지 전체를 구현한 것이 아닙니다.

## 전체 stripe redo의 적용 조건

redo는 이미 정한 새 결과를 다시 기록하는 복구 방식입니다. `redo.bin`에는 RDL1 식별자 4바이트, stripe 번호 4바이트, 대상 세대 4바이트, D0/D1/P 전체 12바이트, 앞 24바이트의 SHA-256 32바이트가 있습니다. 합계는 56바이트입니다. `<4sII12s`의 `<`는 little endian, `I`는 4바이트 unsigned 정수, `s`는 고정 바이트열을 뜻합니다. Python의 객체 메모리 배치를 그대로 저장하는 형식은 아닙니다.

복구기는 정확한 길이, digest, stripe 0, 대상 세대, 저장된 세 값의 XOR 정합성을 모두 확인합니다. SHA-256이 맞더라도 대상이 세대 6이면 보류 세대 8과 다르므로 거부합니다. 반대로 24바이트 header에 새 payload가 전부 들어 있더라도 뒤 digest가 없으면 불완전한 로그입니다. 시험은 56바이트 기록의 prefix 0~55를 각각 실제 파일에 쓰고 거부를 확인합니다. checksum이 없는 부분을 0으로 채우거나 남은 멤버를 섞어 로그를 완성하지 않습니다.

일반 경로는 dirty 표시→전체 redo→첫 멤버→둘째 멤버→clean 표시입니다. redo가 유효하게 남으면 현재 멤버에 옛 값이 섞여 있어도 새 stripe 전체를 새 목적지에 씁니다. clean 상태에서 남긴 redo는 현재 세대와 복원 결과에 맞아야 합니다. 두 멤버 이상이 빠진 입력은 로그가 정상이어도 먼저 거부합니다. 전체 새 stripe를 가지고 있으므로 이 제한이 수학적으로 필수인 것은 아니며, 이번 구현이 검사한 단일 결손 복구의 지원 범위를 명확히 고정한 정책입니다.

## 코드의 문법과 목적

다음은 모델의 XOR 계산을 읽기 쉽게 풀어 쓴 발췌입니다. `require`는 조건이 거짓이면 `ValueError`를 일으키는 함수이며 `assert`처럼 최적화에서 사라지지 않습니다.

```python
def xor(left, right):  # def는 함수 정의이며 두 바이트열을 인자로 받습니다.
    require(len(left) == len(right) == 4, "MEMBER_LENGTH")  # len과 연속 비교로 양쪽이 4바이트인지 확인합니다.
    return bytes(a ^ b for a, b in zip(left, right))  # zip으로 같은 위치를 묶고 ^ 결과를 bytes로 반환합니다.
```

`bytes`를 순회하면 0~255 정수를 얻습니다. `^`는 정수의 비트 XOR이며 거듭제곱 연산이 아닙니다. `for a, b in ...`는 두 값을 각각 이름에 대입하는 반복 구문입니다. `()`는 함수 호출의 인자 범위를 나타내고, 여기서 generator 식은 결과를 차례로 bytes 생성자에 넘깁니다.

```python
before = snapshot(source)  # dict로 파일명별 SHA-256을 저장하며 원본의 비교 기준을 만듭니다.
meta, values, raw = load(source)  # tuple의 세 결과를 나누어 대입합니다.
if meta["dirty"]:  # []로 사전의 dirty 값을 읽고 True일 때 들여쓴 구문을 실행합니다.
    require(raw is not None, "NEEDS_RECOVERY_DATA")  # is not None으로 로그 부재를 구별합니다.
    generation, values = decode_redo(raw, meta["pending"])  # payload 공개 전에 길이·내용·세대를 확인합니다.
require(snapshot(source) == before, "SOURCE_CHANGED")  # ==로 파일명과 해시 사전 전체를 비교합니다.
```

이 발췌는 복구의 판단 부분입니다. 전체 함수는 [model.py](../예제_examples/실무검증_practical-validation/raid_parity/model.py)에 있으며 새 목적지를 먼저 확인하고, 지원 결손 수를 검사한 뒤 각 파일을 `xb` 모드로 만듭니다. `x`는 기존 파일을 덮어쓰지 않는 생성, `b`는 binary 모드입니다. `with`는 파일 사용 범위를 정하고, `flush`는 Python 버퍼를 내보내며, `os.fsync`는 호스트에 동기화를 요청합니다. 세 동작이 실제 디스크의 임의 정전 보장을 모두 대신하지는 않습니다.

## 복원 성공을 판단하는 방법

복구 출력은 원본 밖의 새 폴더에만 만듭니다. 기존 목적지를 발견하면 거부하고 그 안의 `KEEP` 파일이 그대로인지 시험합니다. 입력 이름 집합·각 멤버 길이·metadata 자료형·중복 JSON 키도 확인합니다. `True`와 `False`는 Python에서 정수처럼 비교될 수 있어 정수 번호에는 `type(value) is int`를 사용합니다. 이 구분 없이 값만 비교하면 False를 stripe 번호 0처럼 받아들일 수 있습니다.

기록 후 새 파일을 다시 읽어 기대 리터럴과 비교하고, 원본의 파일명·SHA-256도 전후 비교합니다. 복원된 사본을 다시 입력으로 한 번 더 복원하여 파일 해시가 같은지도 확인합니다. 이를 멱등성이라고 하며 같은 작업을 반복해도 결과가 변하지 않는 성질입니다. 다만 잘못된 내용을 매번 똑같이 만드는 코드도 멱등적일 수 있으므로 독립 기대값 비교를 빼지 않습니다.

복원 중 실제 호스트 I/O가 실패하면 새 목적지 일부가 남을 수 있습니다. 성공 상태는 반환하지 않지만 디렉터리 전체를 원자적으로 게시·롤백하는 기능은 구현하지 않습니다. 동시 writer도 지원하지 않습니다. 원본 해시의 전후 일치 검사는 이번 단일 writer 시험의 관측이며 임의의 동시 변경을 잠그는 기능이 아닙니다.

## 패리티 일치가 원본 증명은 아닌 반례

첫 D0 바이트를 10→11로 바꾸고 첫 P 바이트도 b0→b1로 바꾸면 `11111213 XOR a0a1a2a3 = b1b0b0b0`입니다. 검사기는 패리티 일치를 True로 보지만 고정 원본과 같은지 비교하면 False입니다. clean 표시가 남은 이 입력은 XOR 기준으로 복사할 수 있으나 원본 내용의 검증을 통과했다는 뜻은 아닙니다. 이 양성 반례를 정상 시험 안에서 따로 기록합니다.

RAID의 중복 정보, 장치 ECC, 파일의 내용 해시, payload를 가진 백업은 서로 다른 문제를 다룹니다. XOR 한 식만으로 두 데이터의 임의 손상이나 최신 문서의 삭제까지 되돌릴 수 없습니다. [백업 자료가 없는 파일시스템 복구](파일시스템의손상검사와복구계획_filesystem-check-repair.md)와 연결하면 구조 검사와 실제 자료 보존의 차이를 함께 볼 수 있습니다.

## Linux md의 bitmap과 PPL과 journal

Linux 6.12 [관리자 문서](https://docs.kernel.org/6.12/admin-guide/md.html)의 dirty/degraded 절과 `consistency_policy`·bitmap 절은 재동기화가 필요한 영역의 표시와 결손을 구분합니다. bitmap은 자료 전체의 사본이 아니므로 이번 예제의 `dirty=True`와 같이 그 표시만으로 사라진 D1을 만들어 내지 않습니다.

[PPL 문서](https://docs.kernel.org/6.12/driver-api/md/raid5-ppl.html)는 갱신하지 않은 데이터의 XOR을 먼저 남겨 write hole을 다룹니다. 새 데이터 전체의 journal과는 다르며 진행 중 데이터의 상실까지 모두 막지는 않습니다. [RAID cache 문서](https://docs.kernel.org/6.12/driver-api/md/raid5-cache.html)는 journal을 멤버 기록보다 먼저 쓰는 방식과 write-through·write-back의 완료 시점을 설명합니다. 여기의 56바이트 전체 stripe redo는 두 공식 형식의 구현이 아니라 별도로 정한 교육 형식입니다.

위 세 자료는 Linux 6.12 판본으로 2026-10-21에 열람했습니다. cache·PPL 문서 전체와 관리자 문서의 해당 절을 읽은 배경 설명이며 Linux md의 실행 결과를 주장하지 않습니다. 이 실험의 중단 경계에서는 동기화 뒤 함수가 정상 반환합니다. 프로세스 강제 종료·동기화 도중 kill·OS crash·물리 전원 제거·sector tearing·4바이트 쓰기 원자성·회전 패리티 배치·RAID6·실물 성능은 시험하지 않습니다.

## 확인 문제

1. D0만 새 값인 상태에서 D1을 `P XOR D0`로 계산하면 왜 패리티 검사를 통과해도 원본과 다릅니까? 남은 두 값을 기준으로 새 D1을 만들었기 때문에 같은 식을 다시 검사해도 독립 근거가 생기지 않습니다.
2. payload가 모두 들어 있는 24바이트 로그를 왜 거부합니까? 이번 형식의 완성 조건인 32바이트 digest와 길이 검사를 충족하지 않기 때문입니다. 새 stripe 전체가 보인다는 추측으로 불완전 기록을 승인하지 않습니다.
3. 재복원한 파일의 해시가 같으면 원본 복구를 입증합니까? 같은 결과의 반복만 입증합니다. 고정 원본 리터럴·신뢰하는 외부 manifest 등 별도의 내용 기준이 필요합니다.

## English

The fixed four-byte stripe changes from D0=10111213, D1=a0a1a2a3, P=b0b0b0b0 to D0=20212223, D1 unchanged, P=80808080. Updating only D0 or only P reconstructs a missing D1 as 90919293. A parity recheck of a freshly derived member cannot establish the original bytes.

Recovery uses an independently trusted metadata generation and a complete 56-byte own redo format containing all three new members. It rejects incomplete records, stale generations, parity disagreement, invalid lengths and more than one missing member. The last restriction is an explicit implementation boundary even when a complete redo exists. Source hashes are preserved and every recovery uses a new destination. Replaying recovered files checks idempotence in addition to independent byte literals.

A separate positive example changes D0 and parity by the same XOR mask. Parity still agrees, but content differs from the original. Neither a clean marker nor an unauthenticated digest proves original content or hostile anti-rollback security. Versioned Linux 6.12 documents explain bitmap, PPL and journal as distinct mechanisms; this program implements none of their on-disk formats. Selected host-file boundaries return normally after synchronization, without physical power cuts, sector atomicity or Linux md execution.
