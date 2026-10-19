# UI 상태를 한곳에서 바꾸기: reducer와 비동기 효과

[분야 안내](../README.md) · [실행 예제](../../../예제_examples/심화_advanced/systems/advanced_models.py) · [독립 테스트](../../../예제_examples/심화_advanced/systems/test_advanced_models.py) · [실행 안내](../../../예제_examples/심화_advanced/systems/README.md)

## 한국어

### 화면 변경을 사건의 순서로 읽습니다

검색어를 빠르게 a→ab로 바꾸면 첫 요청이 나중에 끝날 수 있습니다. generation 번호로 오래된 결과를 막는 것만으로도 한 종류의 오류를 줄입니다. 다음 단계는 입력·로딩·성공·실패·화면 종료를 한 상태 전이 규칙으로 모아, 어느 event가 무엇을 바꾸는지 읽을 수 있게 만드는 것입니다.

reducer는 현재 state와 event를 받아 다음 state를 계산하는 순수 함수입니다. 실제 network 요청 같은 외부 효과는 직접 실행하지 않고 명령 값으로 반환합니다. Android의 단방향 데이터 흐름은 state가 화면으로 내려가고 event가 상태를 관리하는 쪽으로 올라오는 구조를 설명합니다. 화면에 보이는 값을 여러 callback에서 제각각 바꾸는 경우보다 갱신 경계를 분명히 할 수 있습니다. [Android Compose architecture](https://developer.android.com/develop/ui/compose/architecture)

### 상태의 의미를 먼저 고정합니다

`UIState`에는 query, generation, loading, result, error와 active가 있습니다. active는 이 예제의 화면 session 유효 여부이며 Android Activity lifecycle의 모든 상태를 대신하지 않습니다. search를 받으면 generation을 하나 증가시키고 loading을 켜며 이전 result/error를 비웁니다. 반환 effect는 `("fetch", generation, query)`입니다. 외부 실행기가 이 effect를 실행하고 같은 generation을 단 completion event를 돌려준다고 가정합니다.

success나 failure를 반영하는 조건은 active가 참이고 event generation이 현재 값과 같으며 아직 loading인 경우입니다. 이미 완료한 요청의 중복 completion은 무시합니다. stop은 active와 loading을 끄고 generation을 증가시켜 그 session의 늦은 결과를 무효화합니다. start는 새 화면 session을 열지만 예전 요청을 자동 재실행하지 않습니다. 재요청은 별도의 search event입니다.

| 사건 | state 변화 | 외부 효과 |
| --- | --- | --- |
| search | generation 증가, loading 시작 | fetch 명령 반환 |
| 현재 success | result 설정, loading 종료 | 없음 |
| 현재 failure | error 설정, loading 종료 | 없음 |
| 오래된 completion | 그대로 유지 | 없음 |
| stop | session 무효화 | 모델상 취소 명령 없음 |

### 순수 전이와 effect 실행을 분리합니다

같은 state와 event에는 같은 다음 state가 나와야 합니다. reducer 안에서 현재 시각을 읽거나 network 응답을 기다리면 이 조건을 흐릴 수 있습니다. `frozen` dataclass와 `replace()`를 사용해 기존 state를 직접 수정하지 않습니다. 작은 immutable 결과 fixture를 사용하며, 실제 앱에서는 result 내부 객체도 불변 규약을 따라야 합니다. tuple에 가변 객체를 넣었다고 깊은 불변성이 생기는 것은 아닙니다.

Android state production 문서는 event를 처리하는 state holder와 UI가 소비하는 state를 구분하고, lifecycle에 따라 관찰·작업을 관리하는 조건을 설명합니다. 이 Python 모델은 ViewModel·Compose·SwiftUI runtime을 실행하지 않습니다. 화면 회전이나 process death에서 보존할 query, 다시 얻을 result와 network 작업을 어디에 둘지는 해당 플랫폼의 수명 규칙과 맞춰야 합니다. [Android UI state production](https://developer.android.com/topic/architecture/ui-layer/state-production)

### 취소·직렬화·저장은 다른 계약입니다

old completion을 무시해도 이전 network 요청이 취소되지는 않습니다. 자원을 줄이는 취소와 화면의 정확성을 지키는 generation 검사는 목적이 다릅니다. event 처리도 한 줄의 순서로 직렬화한다는 전제가 있습니다. 여러 thread가 동시에 state를 읽고 reducer 결과를 대입하면 순수 함수여도 lost update가 생길 수 있습니다. state holder나 event queue가 그 갱신을 serialize해야 합니다.

테스트는 검색 세 번 뒤 가능한 completion 순서 6개를 모두 실행하고 마지막 검색 abc의 결과만 남는지 확인합니다. stop 후의 이전 결과, restart 뒤 새 검색, 성공 뒤 중복 failure도 따로 확인합니다. demo는 두 fetch 명령과 늦은 응답을 처리한 최종 state를 출력합니다. 전이당 scalar 상태 계산은 상수이며 result를 tuple로 복사하는 비용은 결과 길이에 비례합니다. 이 확인은 event 규칙의 검증이지 실제 모바일 lifecycle 통합이나 network 취소 테스트는 아닙니다.

저장소 루트에서 실행합니다. 첫 명령은 입력과 계산 결과를 출력하고, 두 번째 명령은 이 디렉터리의 전체 테스트를 실행합니다.

```sh
python "예제_examples/심화_advanced/systems/demo.py" ui
python "예제_examples/심화_advanced/systems/test_advanced_models.py" -v
```

## English

### Read a changing screen as an event sequence

Changing a search quickly from a to ab can let the first request finish last. Generation checks reject stale results. The next step is to collect input, loading, success, failure, and session termination into one readable transition rule.

A reducer maps current state and an event to next state. It returns descriptions of external effects rather than performing network work itself. Android's unidirectional data flow sends state down to the screen and events toward the state owner, making the update boundary explicit. [Android Compose architecture](https://developer.android.com/develop/ui/compose/architecture)

### Define state semantics first

`UIState` contains query, generation, loading, result, error, and active. Active represents this example's screen-session validity, not every Android Activity lifecycle state. Search increments generation, starts loading, clears prior result/error, and returns `("fetch", generation, query)`. An external executor is assumed to return a completion event carrying that generation.

Success/failure applies only while active, matching the current generation, and still loading. Duplicate completion after a request finishes is ignored. Stop deactivates loading and increments generation, invalidating late completions from that session. Start reopens the session but does not automatically rerun an old request; another search event does that.

| Event | State change | External effect |
| --- | --- | --- |
| Search | Increment generation, begin loading | Return fetch command |
| Current success | Set result, finish loading | None |
| Current failure | Set error, finish loading | None |
| Stale completion | Preserve state | None |
| Stop | Invalidate session | No cancellation command in this model |

### Separate pure transitions and effect execution

The same state and event should produce the same next state. Reading time or awaiting a network result inside the reducer weakens that property. A frozen dataclass and `replace()` avoid mutating the previous state. Fixtures use small immutable results; a tuple containing mutable objects would not make them deeply immutable.

Android's state-production guidance distinguishes state holders, events, UI consumption, and lifecycle-related work management. This Python model does not run ViewModel, Compose, or SwiftUI. Persisting a query, reloading results, and surviving process death require the platform's lifecycle contract. [Android UI state production](https://developer.android.com/topic/architecture/ui-layer/state-production)

### Cancellation, serialization, and persistence differ

Ignoring stale completion does not cancel the network request. Cancellation limits resource use; generation checks protect displayed state. Event application also assumes a serialized sequence. Concurrent threads can still lose updates if both read state and assign reducer outputs without coordination. The state owner or event queue must serialize application.

Tests enumerate all six completion orders after three searches and require only the latest abc result. Separate cases cover stop, restart with a new search, and duplicate failure after success. The demo prints two fetch commands and the final state after a late old response. Scalar transition work is constant; copying a result into a tuple scales with result length. These checks validate event rules, not actual mobile lifecycle integration or network cancellation.

Run the following commands from the repository root. The first prints the input and computed observations; the second runs the complete test suite in this example directory.

```sh
python "예제_examples/심화_advanced/systems/demo.py" ui
python "예제_examples/심화_advanced/systems/test_advanced_models.py" -v
```

## 출처 / Sources

- [Android: Compose UI Architecture](https://developer.android.com/develop/ui/compose/architecture): 단방향 state·event / unidirectional state and events
- [Android: UI State production](https://developer.android.com/topic/architecture/ui-layer/state-production): state holder·효과·lifecycle / state holders, effects, lifecycle
