# HTTP API의 계약: 멱등성, pagination, 입력 검증

## 요청이 한 번만 도착한다고 가정하지 않는다

API는 다른 프로그램이 호출할 수 있는 동작의 계약이다. HTTP에서는 method, 대상 URI, header, content, status code가 그 계약을 표현한다. JSON 형식이 맞다는 것만으로 API가 올바른 것은 아니다. 같은 요청의 재시도, 잘못된 필드, 데이터가 늘어나는 동안의 목록 조회가 무엇을 뜻하는지도 정해야 한다.

서버가 생성 작업을 마친 직후 응답이 끊겼다고 하자. 클라이언트는 성공 여부를 모르므로 다시 보낼 수 있다. 재시도가 새 항목을 하나 더 만드는지, 이전 작업의 결과를 돌려주는지에 따라 실제 데이터가 달라진다. 네트워크 timeout은 서버에서 아무 일도 하지 않았다는 증거가 아니다.

## 멱등성은 결과 효과의 성질이다

RFC 9110은 같은 요청을 여러 번 적용했을 때 서버에 의도한 효과가 한 번 적용한 것과 같으면 method가 idempotent라고 정의한다. PUT, DELETE와 safe method가 여기에 포함된다. 반환 status와 응답 body가 매번 같아야 한다는 뜻은 아니다. 예를 들어 같은 자원을 삭제할 때 첫 호출과 다음 호출의 응답은 달라도 최종 효과는 자원이 없는 상태다. [RFC 9110 §9.2.2](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.2)

POST가 이 성질을 자동으로 갖는 것은 아니다. 생성 API는 애플리케이션 계약으로 idempotency key를 둘 수 있다. 같은 사용자·동작 범위에서 키 $`k`$와 정규화한 요청 본문 $`b`$를 묶어 저장하고, 같은 쌍의 재시도에는 저장한 결과를 반환한다. 같은 키에 다른 본문이 오면 충돌로 처리한다. 여기서 body 정규화는 동등성 정책이며 단순 문자열 공백 차이와 JSON 객체의 key 순서를 구분할 수 있다.

중복 생성 방지 불변식은 같은 범위의 ((k,b))에 대해 생성 횟수가 최대 1이라는 것이다. 실제 서비스에서는 키 등록, 업무 변경, 결과 저장을 원자적으로 묶어야 동시 요청과 crash 사이의 틈을 막을 수 있다. 키의 사용자별 범위, 보관 시간, 만료 후 동작도 계약이다. 예제는 직렬 호출의 메모리 저장소이므로 이러한 영속·동시성 보장을 구현하지 않는다.

## 큰 목록은 안정된 순서로 나눈다

목록이 커지면 전부 반환하기보다 page 크기를 제한한다. Google AIP-158은 page size, page token, next token과 요청 조건의 일치를 설명하며, token을 권한 증명으로 취급하지 않는다. [Google pagination](https://google.aip.dev/158)

Offset 방식 `LIMIT k OFFSET j`는 이해하기 쉽지만 앞쪽에 삽입·삭제가 생기면 다음 page에서 중복이나 누락이 생길 수 있다. Keyset 방식은 마지막으로 받은 정렬 키 $`c`$ 이후를 읽는다.

```sql
SELECT id, name
FROM items
WHERE id > :cursor
ORDER BY id
LIMIT :page_size;
```

ID가 고유하고 정렬 순서가 안정적이라는 가정이다. `(time,id)`로 정렬한다면 cursor도 두 값을 포함해야 동일 시각의 여러 행을 빠짐없이 구분한다. Keyset이라고 조회 중 바뀐 값까지 일관된 snapshot이 저절로 제공되는 것은 아니다. 변경 없는 전체 목록이 필요하면 snapshot/version 정책을 별도로 둔다. 예제는 고정된 오름차순 unique ID 목록을 전제로 한다.

[`page_after`](../../../예제_examples/확장기초_extended/ai_data/models.py)는 이진 탐색으로 cursor 뒤 시작점을 찾으므로 준비된 배열에서 $`O(\log N+k)`$에 page를 얻는다. 정렬·유일성 검사를 매 page마다 다시 하면 (O(N)) 비용이 생기므로 입력 계약으로 두었다. 실제 API의 token은 내부 key를 감춘 opaque 값일 수 있지만, base64 인코딩만으로 무결성이나 비밀성이 생기지는 않는다.

## 입력 검증은 문법과 의미를 모두 다룬다

객체의 필드 이름, 자료형, 길이, 수치 범위와 업무 조건을 확인한다. Python에서 Boolean은 정수의 하위형이므로 단순 `isinstance(x,int)`만으로 숫자 필드에 `True`가 통과할 수 있다는 점도 고려한다. 예제는 허용한 필드만 받고 비어 있는 이름과 너무 긴 이름을 거부한다. API의 오류 응답은 재시도 가능한 일시 오류인지, 고쳐 보내야 하는 요청 오류인지 구분할 수 있어야 한다. [Google API errors](https://google.aip.dev/193)

| 상황 | 계약에서 정할 항목 |
|---|---|
| 누락·잘못된 형식 | 필드와 원인, 일관된 요청 오류 |
| 같은 키·같은 본문 | 저장된 결과 재사용 |
| 같은 키·다른 본문 | 요청 충돌 |
| 마지막 page | 다음 token 없음 |
| 권한 없는 자원 | 인증·인가 정책에 맞는 오류 |

## 구현과 검증

[`IdempotencyStore`, `page_after`](../../../예제_examples/확장기초_extended/ai_data/models.py)의 [테스트](../../../예제_examples/확장기초_extended/ai_data/test_models.py)는 같은 요청의 재전송에서 생성 수가 늘지 않는지, 반환 dict를 수정해도 내부 결과가 변하지 않는지, 본문 충돌과 잘못된 입력이 거부되는지 확인한다. Page를 끝까지 이어 붙여 원래 snapshot과 비교하고 빈 목록·범위 밖 cursor도 검사한다. HTTP 서버, 인증, 저장소 장애, 동시 요청은 실행하지 않은 계약 모델이다. 단위 테스트와 실제 네트워크·영속 저장소의 통합 검증은 구분한다.

## English

### Requests can be retried

An API specifies behavior accessible to another program. HTTP expresses it through methods, target URIs, headers, content and status codes. Valid JSON alone does not define retry behavior, invalid fields or listing while data changes.

If a response disappears after the server creates an item, the client may retry without knowing whether creation happened. The contract determines whether that creates another item or returns the original result. A timeout is not proof that the server performed no action.

### Idempotence concerns intended effect

RFC 9110 defines an idempotent method by the same intended server effect after repeated identical requests as after one request. PUT, DELETE and safe methods are idempotent. Response statuses and bodies need not be identical: deleting an already absent resource can have a different response while leaving the same final state. [RFC §9.2.2](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.2)

POST does not automatically provide this property. An application can define an idempotency-key contract, storing a scoped key and canonical body with the result. Repeating the same pair returns the result; reusing a key with a different body is a conflict. Canonicalization defines which representations are equivalent, including JSON object key order.

The invariant is at most one creation for the same scoped pair. Production implementations need atomic coordination of key registration, business changes and response storage, plus user scope, retention and expiration rules. The example is an in-memory serial model and provides no crash-safe or concurrent execution guarantee.

### Pagination and ordering

Large lists need bounded pages. Google AIP-158 describes sizes, continuation tokens, matching request parameters and the distinction between tokens and authorization. [Pagination](https://google.aip.dev/158)

Offsets can duplicate or skip records if earlier rows change. Keyset pagination requests ordered keys after the last key, as in the SQL above. Unique stable IDs support this example. Ordering by `(time,id)` needs both cursor components to disambiguate equal timestamps. Keyset traversal does not itself create a consistent snapshot under mutation; snapshot/version semantics are separate.

The linked function assumes a fixed sorted unique array, locates the cursor with binary search and returns $`k`$ items in $`O(\log N+k)`$. Rechecking sortedness on every page would add (O(N)), so sorted uniqueness is an input contract. Real continuation tokens may be opaque; base64 alone provides neither integrity nor secrecy.

### Validate syntax and meaning

Validation covers allowed fields, types, lengths, ranges and business rules. Python Boolean values are integer subclasses, so a naive integer type check may accept `True`. The example accepts only the defined field and rejects empty or oversized names. Error contracts should distinguish malformed requests from transient failures that may be retried. [Google API errors](https://google.aip.dev/193)

The table covers invalid fields, repeat requests, conflicting bodies, terminal pages and unauthorized resources. The local model does not implement authentication or authorization.

### Independent checks

Tests repeat creation and verify the count stays one, modify a returned dictionary to ensure the stored response is protected, and reject body conflicts and invalid inputs. Pagination is checked by concatenating every page and comparing with the original fixed snapshot, including empty lists and cursors beyond the end. No HTTP server, storage failure or concurrent client is exercised. Unit-level contract verification and network/persistent-store integration testing remain distinct.

## Sources

- [IETF RFC 9110 §9.2.2](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.2): HTTP method idempotence.
- [Google AIP-158](https://google.aip.dev/158): pagination contracts, token semantics and authorization boundary.
- [Google AIP-193](https://google.aip.dev/193): structured error contracts. Reference date: 2026-10-19.
