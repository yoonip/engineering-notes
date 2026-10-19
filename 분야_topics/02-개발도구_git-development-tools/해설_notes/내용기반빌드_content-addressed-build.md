# 바뀐 입력만 다시 만들기: 내용 기반 빌드와 캐시

[분야 안내](../README.md) · [실행 예제](../../../예제_examples/심화_advanced/systems/advanced_models.py) · [독립 테스트](../../../예제_examples/심화_advanced/systems/test_advanced_models.py) · [실행 안내](../../../예제_examples/심화_advanced/systems/README.md)

## 한국어

### 파일 시각보다 결과의 원인을 기록합니다

소스 한 줄을 바꾼 뒤 전체 프로젝트를 다시 빌드하면 오래 걸립니다. 반대로 수정 시각만 보고 빌드를 생략하면 시각이 보존된 복사나 clock 차이 때문에 변경을 놓칠 수 있습니다. 증분 빌드는 작업이 어떤 입력에 의존하는지 알고, 그 입력이 바뀐 작업만 다시 실행하는 방식입니다. 핵심은 “최근에 실행했는가”보다 “같은 결과를 기대할 조건이 같은가”입니다.

Git은 내용으로 object를 식별하는 저장 구조를 사용합니다. blob과 tree를 공유할 수 있다는 점은 빌드 결과도 내용으로 재사용하는 사고와 이어집니다. 다만 아래 SHA-256 action key는 Git object ID가 아닙니다. Git의 object header나 저장 형식을 흉내 내는 예제도 아닙니다. [Git Objects](https://git-scm.com/book/en/v2/Git-Internals-Git-Objects)

### action을 순수 함수처럼 다루기

한 작업의 결과를 개념적으로 $`y=F(s,t,o,e)`$라고 쓰겠습니다. $`s`$는 소스와 생성 입력, $`t`$는 toolchain, $`o`$는 인자, $`e`$는 결과에 영향을 주는 환경입니다. 캐시 키는 이 원인들을 정해진 순서와 형식으로 직렬화한 뒤 hash합니다. 한 항목이라도 누락되면 다른 작업을 같은 작업으로 오인할 수 있습니다. 실행 파일 이름이 `cc`로 같아도 compiler의 내용이나 버전, target, 표준 라이브러리가 다르면 같은 toolchain이라고 볼 수 없습니다.

예제의 `action_key()`는 입력 파일 경로와 각 파일의 SHA-256, 명령 인자 배열, toolchain 식별자, 환경 사전을 canonical JSON에 묶습니다. 사전 key 순서를 정렬하므로 사전 삽입 순서만 바뀌면 키는 유지됩니다. 명령은 문자열 하나보다 인자 배열로 보관해 공백이나 quoting의 모호함을 줄입니다. schema 번호도 포함해 키 구성 규칙이 바뀐 경우를 구분합니다.

불변식은 “기록한 입력이 같고 작업이 결정적이면 결과도 같다”입니다. 외부 네트워크, 현재 시각, 선언하지 않은 include 파일을 읽는 작업은 이 가정 밖입니다. Bazel 문서는 action 환경과 선언되지 않은 도구, 빌드 중 입력 수정이 원격 캐시의 정확성에 영향을 줄 수 있음을 설명합니다. 내용 hash만 붙였다고 환경이 격리되는 것은 아닙니다. [Bazel remote caching](https://bazel.build/remote/caching)

### 키와 결과의 무결성을 따로 검사합니다

`ArtifactCache`는 action key에서 결과 bytes와 결과 digest를 찾습니다. 복원할 때 digest를 다시 계산하므로 저장된 bytes가 변형된 경우를 검출합니다. 그러나 공격자가 bytes와 digest를 함께 바꿀 수 있으면 이 검사만으로 출처를 인증할 수 없습니다. 공유 캐시에는 접근 권한과 신뢰 경계가 필요합니다. 실패한 작업이나 일부만 써진 결과를 성공 캐시로 게시해서도 안 됩니다.

입력 전체가 $`N`$바이트이면 처음 hash하는 비용은 $`O(N)`$입니다. 이미 안정적인 입력 digest를 가진 상위 빌드 시스템은 이를 재사용할 수 있지만, 이 작은 예제는 호출 때마다 입력을 읽습니다. 캐시 조회 자체를 평균 상수 시간 사전 조회로 모델링했으며 실제 네트워크 시간, 압축, compiler 실행은 포함하지 않습니다.

### 독립 검증과 범위

테스트는 사전 순서가 달라도 같은 key인지 확인한 뒤 소스 bytes, compiler ID, 옵션, 환경을 각각 한 번씩 바꾸어 key가 달라지는지 검사합니다. 결과 digest를 유지하고 내용만 변조한 fixture도 거부합니다. demo의 결과물은 문자열 fixture이며 실제 C 빌드 결과가 아닙니다. 실제 빌드의 재현성을 확인하려면 별도 디렉터리에서 빌드를 두 번 실행하고 산출물 bytes를 비교해야 합니다. 차이가 있으면 timestamp나 경로 같은 원인을 찾되, 의미가 다른 출력을 임의로 제거해서 같게 만들면 안 됩니다.

저장소 루트에서 실행합니다. 첫 명령은 입력과 계산 결과를 출력하고, 두 번째 명령은 이 디렉터리의 전체 테스트를 실행합니다.

```sh
python "예제_examples/심화_advanced/systems/demo.py" build
python "예제_examples/심화_advanced/systems/test_advanced_models.py" -v
```

## English

### Record causes rather than just file times

Rebuilding an entire project after one source change is slow. Skipping work solely by modification times can miss changes after timestamp-preserving copies or clock differences. Incremental building tracks a task's dependencies and reruns tasks affected by changed inputs. The useful question is whether the conditions for expecting the same output still hold.

Git identifies stored objects by content and can share blobs and trees. This motivates reuse by content, but the SHA-256 action key below is not a Git object ID and does not reproduce Git's object headers or storage format. [Git Objects](https://git-scm.com/book/en/v2/Git-Internals-Git-Objects)

### Treat an action as a function of declared inputs

Conceptually write $`y=F(s,t,o,e)`$, where $`s`$ covers sources and generated inputs, $`t`$ the toolchain, $`o`$ arguments, and $`e`$ relevant environment. Serialize those causes unambiguously before hashing them. Omitting one can make different tasks appear identical. A compiler named `cc` is not a stable toolchain identity if its executable, version, target, or libraries differ.

`action_key()` includes input paths and their SHA-256 digests, an argument array, toolchain identity, environment, and a schema version in canonical JSON. Sorting dictionary keys makes insertion order irrelevant. An argument array avoids ambiguities introduced by treating a shell command as a single string. A schema version distinguishes changes in key construction.

The invariant is conditional: equal declared inputs produce equal outputs when the action is deterministic. Reading network state, the current time, or an undeclared header violates that premise. Bazel describes action-environment leaks, untracked tools, and inputs modified during a build as potential cache correctness problems. Hashing content does not isolate the environment. [Bazel remote caching](https://bazel.build/remote/caching)

### Check action identity and artifact integrity separately

`ArtifactCache` maps the action key to output bytes and their digest. Recomputing the output digest detects altered bytes. It does not authenticate origin when an attacker can replace both bytes and digest. Shared caches therefore need appropriate access controls and trust boundaries. Failed or partially written outputs must not become successful cache entries.

Hashing $`N`$ input bytes initially costs $`O(N)`$. A larger build system can reuse stable upstream digests, but this example hashes all supplied input bytes at every call. Dictionary lookup models average constant-time cache access; network latency, compression, and compiler execution are absent.

### Independent checks and scope

Tests preserve keys under dictionary reordering, then independently change source bytes, compiler identity, options, and environment to require different keys. They also corrupt artifact bytes while preserving the stored digest and require rejection. The demo artifact is a string fixture, not the output of an actual C build. Real reproducibility requires two builds in separate directories and byte-level artifact comparison. Differences should be traced to causes such as timestamps or paths; deleting semantically relevant differences merely to force equality would invalidate the check.

Run the following commands from the repository root. The first prints the input and computed observations; the second runs the complete test suite in this example directory.

```sh
python "예제_examples/심화_advanced/systems/demo.py" build
python "예제_examples/심화_advanced/systems/test_advanced_models.py" -v
```

## 출처 / Sources

- [Git: Git Objects](https://git-scm.com/book/en/v2/Git-Internals-Git-Objects): 내용 주소 방식 / content-addressed objects
- [Bazel: Remote caching](https://bazel.build/remote/caching): action identity·환경·캐시 정확성 / action identity, environment, cache correctness
