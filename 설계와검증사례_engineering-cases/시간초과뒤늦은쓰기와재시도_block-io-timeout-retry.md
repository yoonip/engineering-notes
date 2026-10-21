# 시간 초과 뒤 늦은 쓰기와 재시도 / Late writes and retries after timeout

[사례 목차](README.md) · [실행 코드](../예제_examples/실무검증_practical-validation/io_retry/README.md) · [검증 기록](검증기록_evidence/IO재시도와늦은완료검사_20261021.md)

저장장치 쓰기 요청의 시간이 초과되었다고 해서 쓰기가 취소된 것은 아닙니다. 옛 요청이 뒤늦게 값을 바꾸면, 나중에 성공한 쓰기를 다시 덮을 수 있습니다. 완료 callback에서 요청 세대를 구별하는 것과 장치에 남은 작업을 멈추는 것은 서로 다른 문제입니다. 이 사례는 4바이트 주소 하나의 사건 순서로 그 차이를 재현합니다.

## 요청 하나와 제출 시도 하나는 다릅니다

LBA는 저장장치의 논리 블록 주소입니다. 여기서는 주소 하나와 4바이트 값만 사용합니다. 실제 sector 크기·namespace·원자적 쓰기 단위를 그대로 옮긴 숫자가 아닙니다. 응용 요청 R1은 `AAAA`, R2는 `BBBB`를 같은 주소에 쓰려는 목적입니다. R1의 최초 제출 A와 retry B는 같은 목적의 서로 다른 시도입니다.

Timeout은 기다리는 쪽이 정한 기한을 넘겼다는 관측입니다. 실패를 확정하는 성공 반대말로 취급하면 안 됩니다. 이 모델에서 timeout 뒤 상태는 `UNKNOWN`입니다. 아직 적용하지 않았을 수도 있고, 적용했지만 callback이 늦었을 수도 있습니다. Retry는 같은 목적을 다시 제출하는 일이며, 옛 시도가 사라졌다는 뜻은 아닙니다.

Callback은 장치 작업의 결과를 호스트 코드에 알리는 호출입니다. 구현은 장치 효과인 `apply()`와 통지인 `complete()`를 별도 사건으로 둡니다. 둘 사이에서 다른 요청이 진행할 수 있다는 반례를 표현하기 위해서입니다. 실제 다중 스레드·타이머·드라이버를 실행하는 방식은 아니며, 목록의 사건을 순서대로 실행합니다.

## callback만 걸러도 남는 반례

초기 값은 `00000000`입니다. ASCII `A`는 16진수 `41`, `B`는 `42`이므로 `AAAA`는 `41414141`, `BBBB`는 `42424242`입니다. fixture에는 이 값을 직접 적었으며, 대상 모델의 쓰기 함수로 기대값을 만들지 않습니다.

| 순서 | 사건 | 내부 값 | 응용 관측 |
| --- | --- | --- | --- |
| 1 | R1의 A를 제출합니다. | `00000000` | 진행 중입니다. |
| 2 | A가 timeout입니다. | `00000000` | 완료 여부가 UNKNOWN입니다. |
| 3 | R1을 B로 재시도하고 B가 적용·완료됩니다. | `41414141` | R1 성공을 한 번 알립니다. |
| 4 | R2의 C가 적용·완료됩니다. | `42424242` | R2 성공을 한 번 알립니다. |
| 5 | 옛 A가 뒤늦게 적용됩니다. | `41414141` | 아직 callback은 없습니다. |
| 6 | A의 옛 callback을 무시합니다. | `41414141` | 완료 목록은 R1·R2 그대로입니다. |

마지막 callback을 무시했는데도 최종 값은 `AAAA`입니다. 응용 완료 횟수만 검사하면 이 오류를 놓칩니다. 세대 번호는 어느 요청의 통지인지 구별하는 표식이며, 이미 일어난 매체 쓰기를 되돌리는 명령이 아닙니다. 이 반례는 정상 검사 안에서도 `guard_writes=False`라는 의도한 오류 경로로 실행합니다.

같은 값을 여러 번 쓰면 결과가 같다는 멱등성만으로도 설명이 끝나지 않습니다. 멱등성은 같은 연산을 반복할 때의 성질입니다. 사이에 다른 값의 쓰기가 끼어드는 `A, B, A`의 순서까지 최신 값 B를 보장하지는 않습니다. 네트워크 요청의 중복 제거 ID도 실제 block 작업을 취소하는 신호와 구별해야 합니다.

## 미해결 쓰기의 장벽과 정지 증거

수정 경로는 미해결 쓰기가 있을 때 같은 주소의 새 쓰기를 받지 않습니다. 이것이 이 예제의 장벽입니다. 주소가 하나뿐이므로 모든 쓰기를 직렬화하는 보수적인 호스트 정책입니다. 처리량을 높이는 스케줄러나 서로 다른 LBA의 병렬성은 구현하지 않습니다.

A가 timeout이면 먼저 A의 버퍼 소유권을 유지합니다. `retry(R1, B)`와 `start(R2, C)`를 모두 거부합니다. `quiesce(A, stopped=False)`도 장벽을 풀지 않습니다. 여기서 `stopped=True`는 옛 시도가 이후 데이터를 적용하거나 버퍼를 건드리지 못한다는 외부 증거를 입력했다는 전제입니다. 코드가 장치에 abort·reset을 보내고 그 성공을 판독하는 기능은 없습니다.

명시적 증거 뒤 A는 자체 상태 `QUIESCED`가 됩니다. A의 이후 `apply()`는 거부됩니다. 그때에도 R1은 아직 성공하지 않았으므로 R2가 앞지르지 못합니다. R1을 B로 재시도하여 완료한 뒤 R2를 처리하면 최종 값은 `BBBB`이고 응용 완료는 R1·R2 각각 한 번입니다.

정지 증거는 이미 적용한 값을 없애는 rollback도 아닙니다. 별도 흐름에서는 A 적용 → timeout → QUIESCED 뒤에도 값 `AAAA`가 남습니다. 같은 payload의 B를 다시 적용해 논리 요청을 해결합니다. 따라서 ‘응용 완료 한 번’과 ‘장치 적용 정확히 한 번’을 같은 결과로 쓰지 않습니다. 확인한 안전성은 옛 시도가 나중 요청을 다시 덮지 못한다는 사건 계약입니다.

Linux 6.12의 `blk_mq_quiesce_queue()`는 dispatch가 끝나기를 기다리고 새 dispatch를 막지만 `end_io()` callback 발생까지 막지는 않습니다. 이 글의 자체 `QUIESCED`를 그 API 호출의 효과라고 해석하면 안 됩니다. 실제 복구에서는 사용한 장치·전송·드라이버가 어떤 활동 종료를 보장하는지 별도로 확인해야 합니다.

## 버퍼와 읽기 retry의 차이

버퍼 소유권은 진행 중 시도가 아직 사용할 수 있는 자원을 누구에게 반환할지 정하는 계약입니다. `owners` 사전은 `slot → attempt`를 보관합니다. slot은 실제 메모리 주소가 아닌 소유 표식입니다. timeout만으로 이를 지우면 retry가 아직 사용 중인 slot을 다시 얻을 수 있습니다. 조기 반환 변이는 실제로 이 계약 검사에서 실패합니다.

읽기는 이 모델의 매체 값을 바꾸지 않습니다. 그래서 옛 읽기를 기다리면서 새 읽기를 시도하는 대조를 허용합니다. 다만 새 시도 QB는 새 slot b를 사용하고, 옛 QA의 slot a는 QA 완료까지 보유합니다. QB 성공 뒤 QA가 도착하면 옛 slot만 정리하고 응용 완료를 반복하지 않습니다. 이는 부작용 없는 단순 메모리 읽기의 비교입니다. 읽으면 지워지는 상태 레지스터나 읽기 명령 자체가 상태를 바꾸는 장치에 일반화하지 않습니다.

요청 ID·시도 ID·시도 세대를 함께 검사합니다. 잘못된 요청 ID나 세대는 거부하며 버퍼를 반환하지 않습니다. 같은 callback이 두 번 오면 두 번째는 `IGNORED_DUPLICATE`입니다. 실제 태그가 순환하는 드라이버 전체를 구현한 것은 아니며, 이 교육 모델의 시도 ID는 한 실행에서 재사용을 금지합니다.

## 재시도 예산과 실패 종료

기본 `max_attempts=2`는 최초 1회와 retry 1회입니다. retry를 두 번 더 허용한다는 뜻이 아닙니다. A가 오류 완료되어도 쓰기 효과를 확정하지 못하면 `FAILED_UNCERTAIN`입니다. B가 다시 timeout이면 정지 증거를 받기 전 `give_up()`도 거부합니다. 응용이 포기했다는 이유로 장치 활동이 없어지는 것은 아니기 때문입니다.

B를 QUIESCED로 만든 뒤 세 번째 시도 C는 예산 초과로 거부됩니다. 이후 응용 실패를 한 번 기록하고 R2를 처리합니다. 예산은 무한 복구를 막는 정책이며 저장장치의 물리 취소 보장이 아닙니다. 상한을 없앤 변이는 ‘세 번째 시도가 거부되어야 한다’는 독립 기대값에서 실패합니다.

## 실행과 검증 결과

실행 방법은 예제 README에 있습니다. 2026-10-21에 Python 3.12.14에서 기본 실행과 `-O` 실행이 각각 82개 검사·45개 계약 거부를 통과했습니다. `-O`는 일반 `assert`를 없앨 수 있으므로 검사기는 직접 예외를 발생시킵니다. 4종 오류 변이를 두 모드에서 실행한 8회는 모두 exit 1이었고 정상은 exit 0이었습니다.

완료가 timeout 바로 전·직후에 온 두 순서, duplicate·wrong ID·wrong generation, 완료 전 성공 통지, ID 재사용, 버퍼 조기 반환, retry 한도, 실패 후 다음 요청, 읽기 retry를 검사했습니다. 기존 결과 폴더 재사용은 두 모드 모두 exit 2였고 기존 JSON 바이트가 유지되었습니다. 잘못된 fixture의 LBA 수 역시 exit 2였습니다. 소스 해시·각 명령·실제 사건은 실행 기록과 비공개 원시 결과로 연결됩니다.

## 줄별 문법과 목적

```python
from model import IoModel                         # from/import는 model.py의 객체 형을 불러옵니다.
d = IoModel(max_attempts=2)                        # ()로 객체를 만들며 이름 인자로 총 시도 수를 정합니다.
d.start("R1", "A", "WRITE", "41414141", "a")        # 점 표기로 메서드를 호출하여 R1의 첫 시도 A를 만듭니다.
d.timeout("A")                                    # 문자열 A의 timeout 사건이며 완료 여부는 UNKNOWN입니다.
d.quiesce("A", stopped=True)                      # True는 외부 정지 증거를 입력하는 논리값입니다.
d.retry("R1", "B", "a")                           # 같은 응용 요청을 새 시도 B로 제출하고 반환된 slot a를 씁니다.
d.apply("B")                                      # 장치 효과 사건이 내부 값을 AAAA로 바꿉니다.
d.complete("B", "R1", 2, "SUCCESS")               # 정수 2는 자체 시도 세대이며 R1 성공을 한 번 기록합니다.
d.start("R2", "C", "WRITE", "42424242", "a")        # 이전 응용 요청이 해결된 뒤 R2를 받습니다.
d.apply("C")                                      # 같은 주소의 값을 BBBB로 바꿉니다.
d.complete("C", "R2", 1, "SUCCESS")               # R2의 첫 시도 완료를 기록합니다.
value = d.snapshot()["media"]                     # []로 반환 사전의 media 항목을 꺼내며 값은 42424242입니다.
```

다음은 실제 모델의 시도 조회 함수입니다. `def` 뒤 이름·괄호는 함수의 이름과 입력을 정하고, 콜론 뒤 들여쓰기는 본문을 묶습니다.

```python
def _attempt(self, aid):                           # self는 객체 자신, aid는 조회할 시도 ID입니다.
    name(aid)                                     # 식별자의 형과 허용 문자를 먼저 검사합니다.
    if aid not in self.attempts:                  # if/not in은 사전에 해당 키가 없는 조건입니다.
        raise ContractError("unknown attempt")    # raise로 계약 오류를 발생시켜 잘못된 사건을 멈춥니다.
    return self.attempts[aid]                     # return은 []로 찾은 시도 객체를 호출자에게 돌려줍니다.
```

`@dataclass`는 상태를 담는 클래스의 초기화 메서드 등을 생성합니다. `field(default_factory=list)`는 요청마다 별도 빈 리스트를 만듭니다. 모든 요청이 같은 변경 가능한 리스트를 공유하는 일을 피합니다. `{}`는 사전, `[]`는 리스트 생성에도 쓰이며 `None`은 읽기 payload가 없다는 값입니다. `any(...)`는 조건 중 하나라도 참인지 검사하여 미해결 쓰기를 찾습니다.

## 확인 문제

1. 옛 callback을 무시하고 응용 완료가 각각 한 번이면 최신 값이 보장되나요? 답: 아닙니다. 반례는 최종 `AAAA`이며 옛 장치 효과를 따로 막아야 합니다.
2. timeout 뒤 버퍼를 즉시 반환해도 되나요? 답: 이 모델에서는 안 됩니다. 완료나 별도 활동 종료 증거가 필요합니다.
3. 기본 시도 한도 2에서 두 번째 시도도 timeout이면 무엇을 하나요? 답: 옛 활동 종료를 확인하기 전에는 실패 종료도 확정하지 않으며, 확인 후 세 번째 시도를 거부하고 정책에 따라 응용 실패를 알립니다.

## 출처

- [Linux Kernel 6.12 blk-mq](https://docs.kernel.org/6.12/block/blk-mq.html): Operation·Tag-based completion, timeout 반환 enum, `blk_mq_ops.timeout`, `blk_mq_quiesce_queue`와 `blk_mq_start_request` 설명을 읽었습니다. 요청 완료 순서·timeout 처리·queue dispatch의 범위에 사용했습니다.
- [Linux v6.12 include/linux/blk-mq.h](https://github.com/torvalds/linux/blob/v6.12/include/linux/blk-mq.h): `enum blk_eh_timer_return` 주석과 선언을 대조했습니다. 자체 상태 이름이나 `stopped=True` 계약이 커널 규격에 있다는 근거로 쓰지 않았습니다.
- [카드 busy·오류·timeout 사례](eMMC와SD의busy와쓰기실패_emmc-sd-write-status.md)와 [USB callback 소유권 사례](USB의부분전송과중복없는복구_usb-bulk-recovery.md)는 선행 모델입니다. 여기서는 매체 적용과 통지의 분리·겹침 쓰기의 순서를 추가했습니다.

## English

A timeout leaves an unknown outcome; ignoring an old callback does not undo an old device-side write. The fixed trace uses a barrier against unresolved overlapping writes, retained buffer ownership, and explicit external evidence that an old attempt can no longer take effect. Only then can the bounded retry resolve R1 before R2. Final bytes are `BBBB`, with one application completion for each request. The callback-only counterexample still ends in `AAAA`.

The model's `QUIESCED` is stronger than Linux queue quiescing: it is an explicit input contract about old effects, not an implementation of `blk_mq_quiesce_queue()`. Read retries retain separate buffers; attempt limits, identity errors, duplicate callbacks, and failure recovery are checked. These deterministic host events do not run a block driver, DMA engine, wall-clock timer, or power-loss test.
