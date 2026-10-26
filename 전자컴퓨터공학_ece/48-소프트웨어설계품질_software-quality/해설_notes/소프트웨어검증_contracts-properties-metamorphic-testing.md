# 소프트웨어 검증: 예제, 계약과 변환 성질

[Software Quality](../README.md) · [구현](../../../예제_examples/확장기초_extended/systems/extended_models.py) · [테스트](../../../예제_examples/확장기초_extended/systems/test_extended_models.py)

## 한국어

### 테스트 전에 맞는 동작을 정하기

테스트가 실행되어도 기대한 동작이 잘못되어 있으면 잘못된 코드를 통과시킬 수 있습니다. 계약은 허용 입력, 결과 조건, 상태 변화와 실패 동작을 분명히 하는 방식입니다. 예를 들어 “bytes 레코드를 직렬화한다”에는 길이 필드의 바이트 순서, 최대 길이, 빈 값 허용 여부와 잘린 입력의 처리가 더 필요합니다. NASA의 소프트웨어 검증 안내도 요구사항과 테스트 근거를 연결합니다. 여기서 NASA의 프로젝트별 규정을 일반 저장소의 인증 조건으로 옮기는 것은 아닙니다. [NASA SWE-066](https://swehb.nasa.gov/spaces/SWEHBVD/pages/102695449/SWE-066+-+Perform+Testing)

정확한 기대값을 한 번 적는 example test는 알려진 사례와 경계를 고정합니다. property test는 정해진 입력 범위에서 반복 성립해야 하는 관계를 확인합니다. 예를 들어 정렬 결과는 오름차순뿐 아니라 원소의 중복 횟수도 보존해야 합니다. 집합만 비교하면 `[1,1,2]`가 `[1,2]`로 줄어드는 오류를 놓칩니다. [University of Toronto: Property-Based Testing](https://www.teach.cs.toronto.edu/~csc148h/notes/testing/hypothesis.html)

### 정답을 얻기 어려우면 관계를 검사합니다

복잡한 계산은 입력마다 정확한 답을 구하는 oracle 자체가 어려울 수 있습니다. metamorphic test는 입력을 바꾸었을 때 출력이 어떤 관계를 가져야 하는지 이용합니다. 같은 노드의 비음수 최단 경로에서 모든 비용을 양의 정수 k배로 바꾸면 유한한 최단 거리도 k배입니다. 알고리즘이 반환한 값 하나를 다시 그대로 계산하는 테스트와는 다릅니다. [NIST: Metamorphic Testing](https://www.nist.gov/publications/metamorphic-testing-cybersecurity)

다만 관계를 만족하는 틀린 함수도 있습니다. 모든 거리를 0으로 반환하는 구현은 단순한 배율 성질만 통과할 수 있습니다. 따라서 알려진 작은 답, 다른 알고리즘의 기준해, 입력 변환 성질과 실패 사례를 조합합니다. Hypothesis 같은 도구는 입력 범위와 성질에서 많은 사례를 만들고 실패를 줄이는 데 도움을 주지만, 생성된 사례의 통과가 모든 입력의 증명은 아닙니다. [Hypothesis 공식 소개](https://hypothesis.readthedocs.io/en/latest/tutorial/introduction.html)

### 길이 기반 레코드로 계약 구현하기

예제 `encode_records`는 각 payload 앞에 길이를 2바이트 big-endian으로 붙입니다. 기본 제한은 레코드당 1,024바이트, 인코딩 전체 8,192바이트이며 빈 레코드도 허용합니다. `decode_records`는 길이 필드나 payload가 잘리면 거부하고, 선언한 길이를 확인한 뒤 그 범위를 읽습니다. 이 형식에는 전송 경계, CRC, 인증이나 재전송이 없으며 실제 네트워크 프로토콜을 대체하지 않습니다.

핵심 불변식은 항상 읽기 위치가 입력 범위 안에 있고, 다음 payload의 길이가 남은 입력과 제한 안에 있어야 한다는 것입니다. 남은 길이와 비교한 뒤 읽으면 C 계열의 고정 폭 구현에서도 무분별한 `offset + length` 계산보다 overflow 전제를 관리하기 쉽습니다. Python에서도 입력 크기를 먼저 제한해야 메모리·CPU 사용을 관리할 수 있습니다.

| 검사 | 잡으려는 오류 |
| --- | --- |
| 알려진 바이트열 | encoder와 decoder가 같은 잘못된 규칙을 공유 |
| decode(encode(x)) = x | 값·순서·빈 레코드 누락 |
| 잘린 입력·최대 길이 | 범위 밖 읽기와 과도한 할당 |
| 독립 기준해 | 같은 구현을 복사한 oracle |
| 변환 관계 | 일부 예제에서만 맞는 구현 |

테스트는 `[b"A", b""]`가 `00 01 41 00 00`인지 독립적으로 고정하고, 난수 레코드의 왕복, 잘린 길이, 크기 제한을 확인합니다. 같은 테스트 파일에서 Dijkstra와 Bellman–Ford의 대조 및 비용 배율 성질도 실행합니다. seed를 고정해 이 실행의 입력을 다시 만들 수 있게 하되, 한 seed가 입력 공간을 대표한다고 주장하지 않습니다.

### 검사 결과의 의미

테스트 실패는 계약 위반을 보여 주는 구체 근거가 됩니다. 반면 통과는 실행한 범위에서 위반을 찾지 못했다는 뜻입니다. 코드 커버리지가 높아도 기대값, 오류 처리와 실제 시스템 경계가 빠질 수 있습니다. 요구사항→검사→실행 환경→결과가 연결될 때 결과를 검토하고 다시 실행하기 쉬워집니다. 성능·동시성·실장치 동작은 해당 조건의 별도 검증이 필요합니다.

## English

### Define the contract before testing

A test can approve incorrect code when its expected behavior is wrong. Specify allowed inputs, postconditions, state changes, and failures. Byte-record serialization needs endianness, length limits, empty-value policy, and truncated-input behavior. NASA guidance connects tests to requirements; its project-specific rules are not presented as certification requirements for this repository. [SWE-066](https://swehb.nasa.gov/spaces/SWEHBVD/pages/102695449/SWE-066+-+Perform+Testing)

Example tests anchor known values and boundaries. Property tests examine relations across an input domain. Sorting should preserve multiplicities as well as order; set equality misses reducing `[1,1,2]` to `[1,2]`. [Toronto course notes](https://www.teach.cs.toronto.edu/~csc148h/notes/testing/hypothesis.html)

### Test relationships when an oracle is difficult

Metamorphic tests relate outputs after defined input transformations. Scaling all nonnegative edge costs by positive integer k scales finite shortest-path distances by k. This differs from copying the implementation to recompute its answer. [NIST](https://www.nist.gov/publications/metamorphic-testing-cybersecurity)

A wrong all-zero distance function could still satisfy scaling. Combine known cases, independent algorithms, transformations, and failures. Tools such as Hypothesis generate cases from domains and properties and can simplify failures, but passing generated cases is not a proof over every input. [Hypothesis](https://hypothesis.readthedocs.io/en/latest/tutorial/introduction.html)

### Implement a bounded record contract

`encode_records` prefixes each bytes payload with a two-byte big-endian length. Defaults allow 1,024 bytes per record and 8,192 encoded bytes overall, including empty records. The decoder rejects incomplete length fields, truncated payloads, and limit violations before reading payloads. The format supplies no transport framing, CRC, authentication, or retry behavior.

Its invariant keeps the offset within input bounds and requires the next size to fit both the remaining data and configured limit. Comparing against remaining length also helps manage fixed-width overflow assumptions in C-like implementations. Python still needs input limits for resource control.

Known-byte tests prevent an encoder and decoder agreeing on the same wrong format. Round trips preserve values, ordering, and empty records; malformed and oversized inputs test bounds. `[b"A", b""]` is independently fixed as `00 01 41 00 00`. Generated round trips supplement that oracle. The suite also compares Dijkstra with Bellman–Ford and checks cost scaling. A fixed seed supports replay, not representativeness of the whole domain.

### Interpret a pass precisely

A failure supplies a concrete contract violation. Passing means no violation was found in the executed scope. Coverage alone does not establish correct assertions, errors, or system boundaries. Connect requirements, checks, execution environment, and results. Performance, concurrency, and hardware behavior need their own conditions and evidence.

## 출처 / Sources

NASA의 요구사항 추적, 대학·도구의 property 검사, NIST의 oracle 문제를 서로 보완하는 관점으로 대조했습니다. / Requirements, properties, and oracle limitations were cross-checked as complementary methods. 확인 / checked: 2026-10-19.
