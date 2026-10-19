# 인증된 메시지의 재전송: replay window

[분야 안내](../README.md) · [실행 예제](../../../예제_examples/심화_advanced/systems/advanced_models.py) · [독립 테스트](../../../예제_examples/심화_advanced/systems/test_advanced_models.py) · [실행 안내](../../../예제_examples/심화_advanced/systems/README.md)

## 한국어

### 올바른 MAC은 새 명령이라는 뜻이 아닙니다

장치가 “밸브 열기” 명령과 MAC을 검증했다고 하겠습니다. 누군가 그 bytes를 그대로 다시 보내면 내용과 MAC은 여전히 일치합니다. 메시지 인증은 변조 검출과 키에 연결된 출처 검증을 제공하지만 “이번에 처음 받은 요청”이라는 수신 이력을 대신하지 않습니다. 처음 요청인지 판단하려면 인증된 sequence와 receiver 상태가 필요합니다.

IPsec ESP의 anti-replay window는 이 문제를 sequence 범위와 bitmap으로 다루는 표준 사례입니다. 여기서는 그 아이디어를 단순화한 HMAC 예제를 만들며, ESP packet format이나 ESN rollover를 구현하지는 않습니다. replay 상태는 무결성 검사가 성공한 packet에 의해서만 갱신되어야 합니다. 공격자가 큰 sequence 숫자만 보내 정상 packet을 창 밖으로 밀어내지 못하게 하기 위해서입니다. [RFC4303 §3.4.3·Appendix A](https://www.rfc-editor.org/rfc/rfc4303.html)

### 순서가 조금 바뀌어도 중복은 거부합니다

최고로 받아들인 번호를 T, window 너비를 W, bit 0을 T의 수신 여부로 둡니다. 처음 state는 T=0, bitmap=0이며 전송 번호는 1부터 시작합니다. 인증 성공 후 S가 T보다 크면 차이만큼 bitmap을 이동하고 새 bit 0을 켭니다. 큰 점프로 W 이상 이동하면 이전 bit는 전부 버립니다.

S가 T 이하이면 $`d=T-S`$를 계산합니다. $`d\ge W`$면 너무 오래된 메시지고, 그렇지 않으면 bit d가 켜져 있는지 봅니다. 켜져 있으면 이미 받은 번호이므로 거부하고, 꺼져 있으면 받아들여 그 bit를 켭니다. 따라서 window 안의 순서 뒤바뀜을 허용하면서 같은 sequence를 두 번 받아들이지 않습니다.

```math
\mathrm{accepted\ range}=\lbrace S:T-W+1\le S\le T\rbrace.
```

이 집합의 모든 번호를 이미 받았다는 뜻은 아닙니다. bitmap의 빈 bit가 아직 오지 않은 번호를 나타냅니다. 아직 보지 못했어도 window보다 오래되면 거부됩니다. 그러므로 이 기능은 완전한 reliable delivery나 명령 실행 순서 보장이 아닙니다. 서로 순서가 중요한 명령은 따로 정렬·ACK·재전송 규약이 필요합니다.

### sequence와 nonce의 역할을 섞지 않습니다

예제는 context, sequence, payload를 모호하지 않은 canonical JSON에 넣고 HMAC-SHA-256으로 인증합니다. payload 상한은 4,096바이트, sequence는 양의 64비트 범위입니다. 비밀성은 제공하지 않습니다. 공개된 테스트 키는 fixture일 뿐 실제 비밀 키로 쓸 값이 아닙니다.

AEAD의 nonce는 특정 key 아래 암호화 호출별 유일성 같은 알고리즘 규칙을 지켜야 합니다. receiver의 replay window를 둔다고 sender가 nonce를 재사용해도 되는 것은 아닙니다. 반대로 nonce가 매번 달라도 receiver가 이전 ciphertext를 기억하지 않으면 재전송을 구별하지 못할 수 있습니다. RFC5116은 nonce와 associated data 규약을 분리해 정의합니다. [RFC5116 §2.1·§3](https://www.rfc-editor.org/rfc/rfc5116.html)

### 재부팅과 외부 효과는 별도 경계입니다

`ReplayReceiver`의 상태는 RAM에만 있습니다. 같은 키로 새 인스턴스를 만들면 예전 message를 다시 받아들이는 테스트도 의도적으로 포함합니다. 실제 설계는 재부팅 뒤의 상태 복원, key/session 변경, rollback 방지와 sequence 소진을 다뤄야 합니다. 같은 session에서 sequence를 0으로 돌리면 안 됩니다. 동시에 들어오는 packet의 인증·상태 검사·갱신도 원자적으로 처리해야 합니다.

테스트는 549개의 sequence 입력에서 “본 적 없는 번호이며 현재 window 안인가”를 독립 set 참조로 판정하고 결과를 비교합니다. 위조 tag의 큰 번호가 T를 바꾸지 않는지도 검사합니다. bitmap 연산 비용은 너비에 따라 달라지며 코드에서는 최대 4,096bit로 제한합니다. 이 검증은 순차적인 수신 모델입니다. “한 번 수락”과 “결제·모터 동작이 장애에도 정확히 한 번 수행됨”은 다른 계약이며 이 예제는 후자를 보장하지 않습니다.

저장소 루트에서 실행합니다. 첫 명령은 입력과 계산 결과를 출력하고, 두 번째 명령은 이 디렉터리의 전체 테스트를 실행합니다.

```sh
python "예제_examples/심화_advanced/systems/demo.py" replay
python "예제_examples/심화_advanced/systems/test_advanced_models.py" -v
```

## English

### A valid MAC does not mean a fresh command

Replaying an unchanged valve-open command and its MAC still passes message authentication. Authentication does not replace receive history. Freshness requires an authenticated sequence and receiver state.

IPsec ESP provides a standard example of an anti-replay window using sequence ranges and a bitmap. This HMAC model simplifies that idea; it implements neither ESP packet format nor ESN rollover. Replay state changes only after successful authentication so a forged large sequence cannot move legitimate traffic out of the window. [RFC4303 §3.4.3 and Appendix A](https://www.rfc-editor.org/rfc/rfc4303.html)

### Allow reordering while rejecting duplicates

Let T be the highest accepted sequence, W the window width, and bit zero represent T. Initial state is T=0 and bitmap=0, with transmitted numbers starting at one. After authentication, S greater than T shifts the bitmap by S-T and sets bit zero. A jump of at least W discards all old bits.

For S at or below T, compute $`d=T-S`$. If $`d\ge W`$, reject it as too old. Otherwise an already-set bit d indicates a duplicate; an unset bit is accepted and marked.

```math
\mathrm{accepted\ range}=\lbrace S:T-W+1\le S\le T\rbrace.
```

This range does not mean every contained number has arrived: unset bits represent gaps. Even an unseen packet is rejected once too old. The window is therefore neither reliable delivery nor command-order enforcement. Order-sensitive commands require additional ordering, acknowledgment, and retransmission rules.

### Do not conflate sequences and nonces

The example authenticates context, sequence, and payload in unambiguous canonical JSON using HMAC-SHA-256. Payload is capped at 4,096 bytes and sequences at positive 64-bit values. It provides no confidentiality. The public test key is a fixture, not an operational secret.

AEAD nonces have algorithm-specific requirements such as uniqueness per encryption call under a key. A receiver replay window does not permit sender nonce reuse. Conversely, unique nonces do not automatically make a receiver remember old ciphertext. RFC5116 distinguishes nonce and associated-data requirements. [RFC5116 §2.1 and §3](https://www.rfc-editor.org/rfc/rfc5116.html)

### Reboot and external effects are separate boundaries

`ReplayReceiver` stores state only in RAM. A test intentionally shows that a new instance using the same key accepts an old message again. A deployed protocol needs reboot persistence or fresh sessions/keys, rollback handling, and sequence exhaustion rules. Resetting the sequence in the same session is invalid. Concurrent authentication, state checks, and updates also need atomic coordination.

Tests compare 549 sequence inputs with an independent set-based reference for unseen numbers within the current window. A forged high sequence must leave T unchanged. Bitmap cost depends on width, capped here at 4,096 bits. Verification covers sequential reception. Accepting once differs from executing a payment or motor effect exactly once across failures; the latter is not guaranteed.

Run the following commands from the repository root. The first prints the input and computed observations; the second runs the complete test suite in this example directory.

```sh
python "예제_examples/심화_advanced/systems/demo.py" replay
python "예제_examples/심화_advanced/systems/test_advanced_models.py" -v
```

## 출처 / Sources

- [RFC4303: ESP](https://www.rfc-editor.org/rfc/rfc4303.html): anti-replay window와 인증 / authenticated anti-replay window
- [RFC5116: AEAD interface](https://www.rfc-editor.org/rfc/rfc5116.html): nonce 유일성·associated data / nonce uniqueness and associated data
