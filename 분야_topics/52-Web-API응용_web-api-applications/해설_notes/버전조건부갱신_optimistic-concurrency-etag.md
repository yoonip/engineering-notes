# 두 사용자의 수정이 겹치면: ETag와 조건부 갱신

[분야 안내](../README.md) · [실행 예제](../../../예제_examples/심화_advanced/systems/advanced_models.py) · [독립 테스트](../../../예제_examples/심화_advanced/systems/test_advanced_models.py) · [실행 안내](../../../예제_examples/심화_advanced/systems/README.md)

## 한국어

### 마지막 저장이 앞의 수정을 지울 수 있다

A와 B가 같은 설정 v1을 읽었다. A가 값을 바꿔 저장한 뒤 B가 예전 화면에서 저장하면 A의 수정이 사라질 수 있다. 서버가 요청을 차례로 처리해도 발생하는 lost update다. 동시 thread가 있어야만 생기는 문제가 아니다. 읽기와 저장 사이에 다른 변경이 있었는지 조건을 검사해야 한다.

optimistic concurrency는 읽을 때 얻은 version을 갱신 요청에 붙이고, 서버의 현재 version과 같을 때만 갱신하는 방식이다. “충돌이 없을 것”을 기대하되 충돌이 나면 무시하지 않고 클라이언트가 다시 읽도록 한다. lock을 화면 편집 시간 내내 잡는 대신 짧은 원자적 비교·갱신으로 경계를 만든다.

### HTTP에서는 strong ETag와 If-Match를 사용한다

서버가 representation과 `ETag: "v1"`을 반환하면 client는 `If-Match: "v1"`을 붙여 갱신할 수 있다. RFC9110의 If-Match는 strong comparison을 사용한다. `W/"v1"` 같은 weak validator를 byte 변화 감지용 strong tag와 같게 취급해서는 안 된다. 조건이 거짓이면 일반적으로 412 Precondition Failed로 변경을 막는다. [RFC9110 §8.8.3·§13.1.1](https://www.rfc-editor.org/rfc/rfc9110.html)

Google AIP-154도 resource etag를 사용한 freshness validation을 설명한다. 다만 그 문서의 API error 규약과 HTTP의 status를 임의로 같은 것으로 옮겨 쓰지 않는다. 이 예제는 좁은 HTTP식 계약을 정하고 그 안에서 200·400·412·428을 사용한다. 조건 헤더를 필수로 요구하는 정책에서 428은 precondition required를 나타낸다. [Google AIP-154](https://google.aip.dev/154), [RFC6585 §3](https://www.rfc-editor.org/rfc/rfc6585.html#section-3)

### 비교와 쓰기를 한 단계로 모델링한다

`VersionedResource`는 문자열 value와 증가하는 정수 version을 가진다. read는 현재 값과 따옴표를 포함한 tag를 반환한다. put은 tag가 없으면 428, 현재 tag와 다르면 412, 값 계약에 맞지 않으면 400, 맞으면 value를 갱신하고 version을 1 증가시켜 200을 반환한다. 실패한 갱신은 값과 version을 바꾸지 않는다.

버전은 삭제 후 재생성이나 process 재시작 때 같은 값으로 되돌아가지 않는 범위여야 한다. 이 객체는 수명이 한 process에 한정된 모델이므로 영구 ETag 생성기를 구현하지 않는다. 같은 value로 다시 저장해도 새 version을 발급한다. representation이 달라질 때 tag가 같지 않도록 하는 것은 strong validator의 중요한 조건이고, 내용이 같을 때 매번 반드시 같은 tag일 필요는 없다.

실제 DB에서는 `UPDATE ... WHERE id=? AND version=?`와 영향 row 수 확인, 또는 적절한 transaction으로 compare와 write를 묶을 수 있다. 먼저 SELECT로 확인하고 나중에 조건 없는 UPDATE를 하면 그 사이 다른 writer가 끼어들 수 있다. local Python 호출이 순차적이라는 사실을 DB 동시성 보장으로 확대하지 않는다.

### 충돌 뒤에는 병합 의미가 필요하다

412를 받은 client는 현재 값을 다시 읽고 사용자의 변경과 함께 검토해야 한다. 새 tag만 가져와 예전 body를 자동 재전송하면 형식적으로 조건을 통과하면서 다른 사람의 수정을 덮어쓸 수 있다. 분야에 따라 field 단위 merge, 사용자 확인, 작업 재계산이 필요하다. ETag는 권한 검사를 대체하지 않으며 resource를 볼 수 없는 client에게 version만 공개해서도 안 된다.

테스트는 A→B와 B→A의 두 저장 순서를 검사한다. 첫 저장은 성공하고 같은 옛 tag를 쓴 두 번째 저장은 412여야 하며 첫 값이 남아 있어야 한다. 새로 읽은 tag로만 다음 갱신을 허용한다. weak tag, 헤더 누락과 빈 값에서도 상태가 변하지 않는지 확인한다. demo는 local 상태 객체를 호출하며 HTTP 서버·인증·DB transaction을 실행하지 않는다. 문자열 길이 상한 256의 이 모델에서 비교·갱신 비용은 상한으로 제한되지만 실제 representation과 저장장치 비용은 따로 계산해야 한다.

저장소 루트에서 실행한다. 첫 명령은 입력과 계산 결과를 출력하고, 두 번째 명령은 이 디렉터리의 전체 테스트를 실행한다.

```sh
python "예제_examples/심화_advanced/systems/demo.py" api
python "예제_examples/심화_advanced/systems/test_advanced_models.py" -v
```

## English

### The last save can erase an earlier edit

A and B read configuration v1. A saves a change, then B saves from the old screen and overwrites A. This lost update occurs even if the server processes requests sequentially: the read and write are separated in time.

Optimistic concurrency attaches the read version to an update and accepts it only if it still matches. It expects conflicts to be uncommon but handles them explicitly. A short atomic compare-and-write replaces a lock held throughout user editing.

### Use strong ETags and If-Match

After receiving `ETag: "v1"`, a client can update with `If-Match: "v1"`. RFC9110 requires strong comparison for If-Match; `W/"v1"` is not equivalent to the strong tag. A false condition generally prevents the update with 412 Precondition Failed. [RFC9110 §8.8.3 and §13.1.1](https://www.rfc-editor.org/rfc/rfc9110.html)

Google AIP-154 also describes etag-based freshness validation, but its API error contract must not be blindly substituted for HTTP statuses. This example defines a narrow HTTP-style contract using 200, 400, 412, and 428. A policy requiring a precondition can use 428 Precondition Required. [Google AIP-154](https://google.aip.dev/154), [RFC6585 §3](https://www.rfc-editor.org/rfc/rfc6585.html#section-3)

### Model comparison and mutation as one step

`VersionedResource` stores a string and increasing integer version. Read returns the value and quoted tag. Put returns 428 for a missing tag, 412 for mismatch, 400 for invalid content, and otherwise updates value, increments version, and returns 200. Failed updates leave both fields unchanged.

Version identities must not unexpectedly repeat across deletion, recreation, or restart within their scope. This object lasts only for one process and is not a persistent ETag generator. Saving the same value still issues a new version. A strong validator must change when representation data change; it need not always remain identical whenever bytes happen to remain identical.

A real database can use a conditional `UPDATE ... WHERE id=? AND version=?` and check affected rows, or an appropriate transaction. A separate SELECT followed by an unconditional UPDATE leaves a race. Sequential Python calls do not establish database concurrency guarantees.

### Conflicts require meaningful resolution

After 412, reread the current value and reconcile the user's edits. Merely obtaining a fresh tag and automatically resending the stale body can still overwrite another person's work. Field-level merge, user review, or recomputation depends on application semantics. ETags do not replace authorization or justify exposing versions of inaccessible resources.

Tests exercise A→B and B→A save orders: the first succeeds, the second stale-tag update returns 412, and the first value survives. A fresh read permits the next update. Missing/weak tags and invalid empty values are nonmutating. The demo invokes a local state object, not an HTTP server, authentication service, or database transaction. String length is capped at 256, bounding this model's comparison and mutation cost; real representation and storage costs are separate.

Run the following commands from the repository root. The first prints the input and computed observations; the second runs the complete test suite in this example directory.

```sh
python "예제_examples/심화_advanced/systems/demo.py" api
python "예제_examples/심화_advanced/systems/test_advanced_models.py" -v
```

## 출처 / Sources

- [RFC9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html): strong ETag·If-Match·412
- [Google AIP-154](https://google.aip.dev/154): resource freshness와 etag / resource freshness
- [RFC6585 §3](https://www.rfc-editor.org/rfc/rfc6585.html#section-3): 428 Precondition Required
