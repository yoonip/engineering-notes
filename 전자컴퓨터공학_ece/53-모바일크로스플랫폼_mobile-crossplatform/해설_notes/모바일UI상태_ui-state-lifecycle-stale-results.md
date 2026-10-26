# 모바일 UI 상태: 생명주기와 늦게 도착한 결과

[Mobile & Cross-platform](../README.md) · [상태 구현](../../../예제_examples/확장기초_extended/systems/extended_models.py) · [순서 검증](../../../예제_examples/확장기초_extended/systems/test_extended_models.py)

## 한국어

### 화면은 현재 상태를 보여 주는 결과입니다

검색 화면을 입력 문자열·로딩 상태·검색 결과로 나누어 생각하면 동작을 설명하기 쉽습니다. 화면이 직접 네트워크 요청과 저장소를 모두 소유하기보다 상태를 보관하는 주체와 UI 표현을 구분합니다. 상태는 한곳에서 갱신하고 UI는 그 상태를 관찰하도록 하면 회전·재구성·다시 그리기에서 같은 데이터를 다르게 해석하는 일을 줄일 수 있습니다. Android의 ViewModel은 화면 수준 상태와 관련 동작을 보관하는 도구입니다. [Android ViewModel](https://developer.android.com/topic/libraries/architecture/viewmodel)

메모리 상태, 복구용 saved state, 영구 데이터도 다릅니다. Android ViewModel은 configuration change를 넘어 유지될 수 있지만 process death를 견디는 영구 저장소는 아닙니다. 작은 검색어·선택 ID 같은 복구 정보는 saved state로, 계속 보관할 데이터는 적절한 영구 저장으로 구분합니다. saved state에도 저장 시점·크기·직렬화 제약이 있으므로 모든 객체를 그대로 넣지 않습니다. [Android Save UI states](https://developer.android.com/topic/libraries/architecture/saving-states)

### 요청 순서와 완료 순서는 같지 않습니다

사용자가 `a`를 검색한 뒤 `ab`를 검색해도 첫 요청이 더 늦게 끝날 수 있습니다. 완료할 때마다 결과를 화면에 넣으면 최신 검색어는 `ab`인데 결과는 `a`인 모순이 생깁니다. 네트워크가 빨라지는 문제보다 어떤 요청이 현재 상태를 바꿀 권한이 있는지의 문제입니다.

간단한 규칙은 요청마다 증가하는 generation을 발급하고, 완료 때 현재 generation과 같은 결과만 반영하는 것입니다. 요청 시작은 query·generation·loading을 함께 갱신하고, 완료는 generation 일치와 화면 유효성을 확인한 뒤 ready·결과를 함께 바꿉니다. 같은 문자열을 다시 검색할 수도 있으므로 문자열 비교만으로 요청의 동일성을 정하지 않습니다.

| 사건 | 상태 변화 |
| --- | --- |
| 새 검색 | generation 증가, 결과 초기화, loading |
| 현재 요청 완료 | ready와 결과를 함께 반영 |
| 이전 요청 완료 | 상태 변경 없음 |
| 화면 종료 | 새 요청·완료 반영 차단 |

### 취소와 결과 차단은 목적이 다릅니다

이전 작업을 취소하면 불필요한 계산을 줄일 수 있습니다. Kotlin Flow의 `collectLatest`는 새 값이 들어오면 이전 값의 action을 취소합니다. 다만 실제 요청 API·콜백·작업의 취소 규약과 side effect도 확인해야 합니다. 취소 요청 하나로 이미 완료된 외부 효과가 되돌아가거나 모든 늦은 callback이 사라진다고 일반화하지 않습니다. generation 검사는 뒤늦은 결과가 UI를 덮는 문제를 별도로 막습니다. [Kotlin collectLatest](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/collect-latest.html)

실패 상태에서도 같은 규칙이 필요합니다. 오래된 요청의 오류가 현재 요청의 성공을 지우면 안 됩니다. 저장·결제 같은 외부 변경은 UI 결과 차단만으로 취소되지 않으며 서버의 요청 규약과 별도 처리가 필요합니다. 화면 상태의 일관성과 업무 효과의 일관성을 나눕니다.

### 구현과 검증

`LatestResults`는 단일 event loop에서 순차적으로 호출한다는 가정의 모형입니다. `begin`은 ticket을 발급하고, `finish`는 현재 loading 요청만 받아들이며, `close`는 이후 반영을 막습니다. 중복 완료도 거부합니다. 이 버전에는 오류·재시도 UI나 실제 통신이 없고, 여러 thread에서 동시에 호출하도록 동기화한 클래스도 아닙니다.

테스트는 세 요청의 완료 순서 여섯 가지를 모두 실행해 마지막 요청의 결과만 남는지 확인합니다. 화면이 닫힌 뒤 결과, 같은 ticket의 중복 완료와 새 요청 거부도 점검합니다. 특정한 sleep 시간에 기대는 테스트보다 순서를 직접 바꾸면 race의 원인을 드러내기 쉽습니다.

실제 Android 앱은 configuration change와 시스템에 의한 process 재생성, foreground/background 전환, 빠른 연속 입력과 네트워크 실패를 함께 시험해야 합니다. 다른 플랫폼에서는 상태 소유·복구 API가 다르므로 Android 수명을 그대로 옮기지 않습니다. 여기서 검증한 것은 순서 모형이며 모바일 빌드·emulator·실기기 실행을 대신하지 않습니다.

## English

### A screen renders state

A search screen can be described through query, loading status, and results. Separating state ownership from rendering reduces inconsistent interpretation across redraws and recreation. Android ViewModel holds screen-level state and related behavior. [ViewModel](https://developer.android.com/topic/libraries/architecture/viewmodel)

Memory, restoration state, and persistent data are different. A ViewModel can survive configuration changes but is not durable across process death. Save small restoration inputs such as a query or selection ID, and persist lasting application data appropriately. Saved state has timing, size, and serialization constraints. [Saving state](https://developer.android.com/topic/libraries/architecture/saving-states)

### Completion order can reverse request order

Search `a`, then `ab`: the first request may finish last. Updating on every completion can display an `ab` query with `a` results. The problem concerns which request may mutate current state.

Issue an increasing generation per request. Starting updates query, generation, and loading together. Completion checks generation and screen validity before updating results and ready status together. Query equality alone is insufficient because a user can repeat the same query. Old completions leave state unchanged; closing prevents new work and result acceptance.

### Cancellation and result gating differ

Cancellation can save work. Kotlin `collectLatest` cancels the previous action when a new value arrives. Nevertheless, examine the actual operation's cancellation/callback contract and side effects. Cancellation does not universally undo completed effects or erase late callbacks. Generation gating separately prevents stale UI updates. [collectLatest](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/collect-latest.html)

Failures need the same gate: an old error must not overwrite current success. Ignoring UI results also does not cancel remote saves or payments. Business effects require their own service contracts.

### Model and verification

`LatestResults` assumes sequential calls on one event loop. `begin` issues a ticket; `finish` accepts only the current loading request; `close` blocks later acceptance. Duplicate completion is rejected. The model has no error/retry UI or real network, and is not synchronized for concurrent threads.

Tests execute all six completion orders of three requests and require only the final request's result. They also cover closure and duplicate completion. Explicit scheduling permutations expose ordering defects without relying on sleep durations.

A real Android app additionally needs configuration change, process recreation, foreground/background, rapid input, and network-failure tests. Other platforms have different ownership/restoration APIs. These checks validate an ordering model, not a mobile build, emulator, or device execution.

## 출처 / Sources

Android의 상태 수명과 Kotlin의 최신 action 취소 규약을 분리해 대조했습니다. / Android state lifetime and Kotlin latest-action cancellation were checked separately. 확인 / checked: 2026-10-19.
