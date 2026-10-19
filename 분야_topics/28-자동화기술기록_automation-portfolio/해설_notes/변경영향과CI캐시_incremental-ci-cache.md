# CI를 줄여도 검증은 빠뜨리지 않기: 변경 영향과 캐시

[분야 안내](../README.md) · [실행 예제](../../../예제_examples/심화_advanced/systems/advanced_models.py) · [독립 테스트](../../../예제_examples/심화_advanced/systems/test_advanced_models.py) · [실행 안내](../../../예제_examples/심화_advanced/systems/README.md)

## 한국어

### 바뀐 파일 이름만 보는 규칙은 쉽게 빠진다

`a.c`가 바뀌었으니 a만 compile하면 된다는 판단은 a가 어떤 header나 생성 파일을 읽는지 알고 있을 때에만 맞다. CI도 같다. 문서 링크 검사, 코드 테스트와 artifact 생성은 서로 의존한다. 변경 파일의 확장자만 보고 job을 생략하면 공유 설정이나 도구 버전 변경이 반영되지 않을 수 있다. 검증 시간을 줄이려면 먼저 의존성과 재사용 조건을 명확히 해야 한다.

여기서는 target에서 직접 의존 입력으로 가는 DAG를 정의한다. `link`가 `compile-a`, `compile-b`에 의존하고 `compile-a`가 `a.c`, `a.h`에 의존한다면 `a.h` 변화는 `compile-a`와 `link`를 다시 보게 만든다. 반면 `compile-b`의 입력에는 영향이 없다. 단, 이 graph가 실제 의존성을 빠짐없이 담는다는 것이 먼저 필요한 가정이다.

### 역방향 도달 가능성으로 영향 범위를 구한다

원래 edge가 target→dependency라면 변경에서 영향을 찾을 때에는 dependency→target의 역방향으로 이동한다. 바뀐 입력을 queue에 넣고 그 입력을 쓰는 target을 차례로 추가한다. 이미 본 노드는 다시 넣지 않아 한 번의 탐색으로 transitive closure를 얻는다. 모든 vertex와 edge를 합쳐 $`O(V+E)`$ 시간과 공간이다.

`affected_targets()`는 먼저 cycle을 거부하고 unknown 변경 이름도 오류로 처리한다. 모르는 파일이 나오면 무조건 영향이 없다고 결론내리지 않는다. 실제 CI에서는 graph 바깥 설정 변경을 전체 실행으로 보내는 정책을 둘 수도 있지만 이 모델은 그런 fallback을 추측하지 않고 명시적인 오류를 반환한다. 함수의 반환값은 재검사할 target 목록이지 위상 정렬된 실행 순서가 아니다.

### 캐시는 정답의 근거가 아니라 입력 재사용이다

GitHub Actions cache는 정확한 key hit 외에 restore key의 prefix로 이전 cache를 찾아 복원할 수 있다. prefix hit를 “이번 dependency가 이미 설치·검증되었다”는 뜻으로 사용하면 안 된다. 예를 들어 package download cache를 복원한 뒤 lockfile에 맞는 설치와 무결성 검사는 여전히 수행한다. 성공적으로 끝난 job의 cache 생성 조건, branch와 scope 제약도 구분한다. [GitHub dependency caching](https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching)

같은 build output을 재사용하려면 source뿐 아니라 toolchain과 영향을 주는 환경이 맞아야 한다. 재현 빌드의 environment 기록은 결과에 영향을 주는 항목을 정의하거나 기록하는 과정이다. OS 이름 하나만 같은 것으로 충분하다고 보기 어렵다. 반대로 사용자 이름처럼 출력에 영향을 주지 않도록 제거할 수 있는 항목은 변동을 없애는 편이 낫다. [Reproducible Builds environment recording](https://reproducible-builds.org/docs/recording/)

### 누락을 찾는 검증을 따로 둔다

독립 테스트는 작은 graph에서 “이 target의 재귀 dependency 중 변경이 포함되는가”를 직접 계산한 참조와 reverse BFS 결과를 비교한다. x·y·a의 모든 변경 부분집합을 검사하므로 직접 변경과 간접 변경이 함께 확인된다. 별도 cycle fixture는 거부되어야 한다. demo는 `a.h` 변경에 `compile-a`, `link`만 선택되는 결과를 보여 준다.

이 확인은 주어진 graph 안의 영향 계산을 검증한다. graph에 실제 include가 누락되었는지는 다른 문제다. dependency 파일 생성, 선언된 입력 검사, clean full build와 incremental build의 주기적 비교가 그 누락을 드러낼 수 있다. 테스트를 실행한 뒤 digest가 같다는 기록은 유용하지만 서로 다른 실행을 같은 cache key로 잘못 묶는 오류를 저절로 고치지는 못한다.

외부 artifact를 복원해 실행할 수 있다면 cache의 쓰기 권한도 중요하다. 이 예제는 GitHub workflow를 변경하거나 cache에 업로드하지 않는다. 로컬 dependency graph의 선택 결과만 계산하며, 효과의 원자성·동시 job 취소·외부 서비스 장애는 기존 CI의 별도 계약으로 남는다.

저장소 루트에서 실행한다. 첫 명령은 입력과 계산 결과를 출력하고, 두 번째 명령은 이 디렉터리의 전체 테스트를 실행한다.

```sh
python "예제_examples/심화_advanced/systems/demo.py" ci
python "예제_examples/심화_advanced/systems/test_advanced_models.py" -v
```

## English

### File names alone are an incomplete dependency rule

Recompiling only a after `a.c` changes is valid only when its headers and generated inputs are accounted for. CI jobs likewise depend on shared configuration, tools, documents, and artifacts. Skipping by extension can miss effects of tool-version or shared-setting changes. Reducing work requires explicit dependencies and reuse conditions.

The example defines a DAG from targets to direct dependencies. If `link` depends on `compile-a` and `compile-b`, and `compile-a` depends on `a.c` and `a.h`, changing `a.h` affects `compile-a` and `link`, but not `compile-b`. The graph must first include every relevant dependency.

### Compute reverse reachability

To propagate a change, reverse target→dependency edges into dependency→target edges. Start a queue with changed inputs and visit their dependents, inserting each vertex once. This computes transitive closure in $`O(V+E)`$ time and space.

`affected_targets()` rejects cycles and unknown change names instead of silently treating unknown files as irrelevant. A production policy could send unknown shared changes to a full run; this model chooses an explicit error. Its returned target list is not a topologically ordered execution schedule.

### Cache reuse is not independent evidence of correctness

GitHub Actions supports exact key hits and prefix fallback through restore keys. A prefix hit does not establish that current dependencies are installed or verified. Restoring a package-download cache should still be followed by lockfile-conforming installation and integrity checks. Cache creation after successful jobs and branch/scope restrictions are separate rules. [GitHub dependency caching](https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching)

Reusing build outputs requires compatible toolchains and relevant environments in addition to source. Recording a build environment means defining or recording the factors that influence output. Matching only the OS name is insufficient. Where a variable such as a user name can be made irrelevant, eliminating that variation is preferable. [Reproducible Builds environment recording](https://reproducible-builds.org/docs/recording/)

### Test selection and dependency completeness separately

Tests compare reverse BFS with an independent recursive query asking whether a target transitively depends on any changed input. Every subset of changes among x, y, and a is tested, along with a rejected cycle. The demo selects `compile-a` and `link` for an `a.h` change.

This establishes propagation within the supplied graph. Missing actual includes are a separate issue. Generated dependency files, declared-input checks, and periodic clean-versus-incremental comparisons can reveal omissions. Stored successful-test digests do not fix a key that incorrectly merges different actions.

Cache write permissions matter when restored artifacts may execute. This example neither modifies GitHub workflows nor uploads caches. It computes local target selection; atomic effects, concurrent cancellation, and external-service failure remain separate CI contracts.

Run the following commands from the repository root. The first prints the input and computed observations; the second runs the complete test suite in this example directory.

```sh
python "예제_examples/심화_advanced/systems/demo.py" ci
python "예제_examples/심화_advanced/systems/test_advanced_models.py" -v
```

## 출처 / Sources

- [GitHub: Dependency caching reference](https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching): key·restore key·scope / cache matching and scope
- [Reproducible Builds: Recording the build environment](https://reproducible-builds.org/docs/recording/): 영향 환경의 정의와 기록 / define and record relevant environment
