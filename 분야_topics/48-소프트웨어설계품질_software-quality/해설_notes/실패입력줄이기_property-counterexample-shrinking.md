# 테스트가 실패한 뒤: 재현 가능한 반례와 shrinking

[분야 안내](../README.md) · [실행 예제](../../../예제_examples/심화_advanced/systems/advanced_models.py) · [독립 테스트](../../../예제_examples/심화_advanced/systems/test_advanced_models.py) · [실행 안내](../../../예제_examples/심화_advanced/systems/README.md)

## 한국어

### 실패를 많이 찾는 것과 이해하는 것은 다릅니다

무작위 입력 1,000개에서 오류를 찾았어도 실패한 입력을 저장하지 않으면 다음 실행에서 사라질 수 있습니다. 더구나 길이 200의 리스트에서만 오류가 보이면 어떤 조건이 원인인지 읽기 어렵습니다. property testing은 넓은 입력 영역에서 성질을 검사하고, shrinking은 실패를 유지하며 불필요한 부분을 제거해 반례를 작게 만드는 과정입니다.

성질 자체가 정확해야 합니다. 예를 들어 정렬 결과의 길이와 순서만 보면 원소를 전부 0으로 바꾸는 잘못된 구현을 놓칠 수 있습니다. 출력이 오름차순이고 입력의 multiset을 보존하며 다시 정렬해도 같다는 조건을 조합할 수 있습니다. 독립 참조 결과가 있으면 함께 비교합니다. 테스트는 코드를 닮은 주장보다 외부 계약을 확인해야 합니다.

### 실패 predicate를 하나의 입력 함수로 만듭니다

`fails(xs)`는 같은 입력에서 같은 실패 여부를 반환하는 결정적 predicate라고 가정합니다. 예제는 원소 0과 음수가 함께 있을 때 실패한다고 정의합니다. 이는 실제 프로그램의 발견된 결함이 아니라 shrinking 규칙을 설명하기 위한 구성 predicate입니다. 원본 [10,0,7,-8,4,-2]에는 실패와 무관한 값이 섞여 있습니다.

`shrink_failure()`는 원소 하나를 제거한 candidate가 여전히 실패하면 그 candidate를 채택하고 처음부터 다시 시도합니다. 더 이상 어느 한 원소도 제거할 수 없으면 멈춥니다. 불변식은 시작부터 끝까지 fails가 참이고 결과가 원본의 순서 보존 subsequence라는 것입니다. 길이가 성공적 축소마다 감소하므로 유한하게 끝납니다.

### 최소의 뜻을 정확하게 제한합니다

종료 결과는 한 번의 원소 삭제로 더 줄일 수 없는 1-deletion-minimal 반례입니다. 전역적으로 가장 짧거나 숫자가 가장 작은 반례라고 보장하지 않습니다. 여러 원소를 동시에 지워야만 더 줄어드는 비단조 predicate에서는 local minimum에 머물 수 있습니다. 값 자체를 0에 가깝게 만드는 숫자 shrinking도 이 구현에 없습니다.

원본 길이가 n이면 재시작을 포함해 predicate 호출은 최악 $`O(n^2)`$ 규모입니다. 각 candidate list 복사도 길이에 비례하므로 predicate 비용을 제외해도 단순 구현의 전체 최악 시간은 $`O(n^3)`$까지 갈 수 있습니다. 입력이 아주 크면 chunk 삭제와 단계별 축소 같은 더 효율적인 전략이 필요합니다. 최종 결과만 짧다고 탐색 자체도 싸다고 생각해서는 안 됩니다.

### 저장된 반례와 seed의 역할

seed와 generator 버전은 실패를 추적하는 단서지만 구체적인 입력 fixture보다 간접적입니다. generator 호출 순서나 버전이 바뀌면 같은 seed가 같은 입력을 가리키지 않을 수 있습니다. Hypothesis 문서는 실패 데이터베이스와 명시적인 `@example`의 역할을 구분하며, 업그레이드 때 내부 database 형식이 바뀔 수 있음을 설명합니다. 이 예제는 Hypothesis를 dependency로 설치하지 않고 작은 축소 규칙을 표준 라이브러리로 실행합니다. [Hypothesis failure replay](https://hypothesis.readthedocs.io/en/latest/tutorial/replaying-failures.html)

수정한 결함의 입력은 명시적인 회귀 테스트로 남깁니다. `unittest`는 개별 test method와 suite를 실행하고 assertion 실패를 보고하는 기본 도구입니다. fixture의 기대값은 수정된 코드로 다시 계산해 복사하지 않고 계약이나 독립 참조로 정해야 합니다. [Python unittest](https://docs.python.org/3/library/unittest.html)

### 독립적인 종료 조건 검사

테스트는 축소 결과가 여전히 실패하고 길이가 2인지 확인한 뒤, 결과의 각 원소를 하나씩 지운 모든 후보가 실패하지 않는지 다시 검사합니다. “원소 하나도 못 지운다”는 최종 조건을 shrinking loop 바깥에서 확인하는 방식입니다. 애초에 실패하지 않는 입력은 오류입니다. demo는 원본과 축소 결과를 함께 출력합니다. 이 확인은 선택한 순수 predicate와 삭제 전략에 한정되며 thread scheduling이나 network timeout처럼 비결정적인 실패를 일반적으로 최소화하지는 않습니다. 그런 실패는 event trace와 환경 조건까지 재현 입력에 포함해야 합니다.

저장소 루트에서 실행합니다. 첫 명령은 입력과 계산 결과를 출력하고, 두 번째 명령은 이 디렉터리의 전체 테스트를 실행합니다.

```sh
python "예제_examples/심화_advanced/systems/demo.py" property
python "예제_examples/심화_advanced/systems/test_advanced_models.py" -v
```

## English

### Finding a failure and understanding it differ

A random test can find a defect and then lose it on the next run unless the exact input is preserved. A 200-element failing list may also hide the cause. Property testing explores input families; shrinking preserves failure while removing irrelevant structure.

Properties must describe the contract correctly. Checking only sorted order and length can miss an implementation that replaces everything with zeros. Sortedness, multiset preservation, and idempotence can be combined, with an independent reference where available.

### Express failure as an input predicate

Assume deterministic `fails(xs)`. The illustration fails when zero and a negative value coexist. This is a constructed teaching predicate, not a reported application bug. The original [10,0,7,-8,4,-2] includes unnecessary elements.

`shrink_failure()` attempts one-element deletions. If a candidate still fails, it becomes the current input and scanning restarts. It stops when no single deletion preserves failure. Throughout, failure remains true and the result is an order-preserving subsequence. Every accepted reduction shortens the list, guaranteeing termination.

### State the kind of minimality

The result is 1-deletion-minimal: no single element can be removed. It is not guaranteed globally shortest or numerically smallest. A nonmonotone predicate may require removing several elements together to escape a local minimum. This implementation also lacks numeric-value shrinking.

For original length n, restart scanning can require $`O(n^2)`$ predicate calls. Candidate copying is linear in length, giving up to $`O(n^3)`$ total worst-case work even before predicate cost. Larger inputs benefit from chunk deletion and staged strategies. A short final counterexample does not imply cheap search.

### Preserve concrete counterexamples

A seed and generator version help investigation but are less direct than an input fixture. Changed call order or generator versions can change what a seed produces. Hypothesis distinguishes its failure database from explicit `@example` cases and notes that upgrades can invalidate internal database formats. This example uses the standard library to illustrate deletion shrinking without installing Hypothesis. [Hypothesis failure replay](https://hypothesis.readthedocs.io/en/latest/tutorial/replaying-failures.html)

A fixed defect's input belongs in an explicit regression test. `unittest` runs individual tests and suites and reports assertion failures. Expected output should follow a contract or independent reference rather than being copied from the implementation under test. [Python unittest](https://docs.python.org/3/library/unittest.html)

### Check the final condition independently

Tests require the result still to fail and have length two, then independently attempt every single deletion and require each candidate not to fail. This checks the stopping condition outside the shrink loop. A nonfailing starting input is rejected. The demo prints both original and reduced inputs. Verification covers this pure predicate and deletion strategy, not arbitrary nondeterministic thread or network failures; those may require an event trace and environment as part of the reproducible input.

Run the following commands from the repository root. The first prints the input and computed observations; the second runs the complete test suite in this example directory.

```sh
python "예제_examples/심화_advanced/systems/demo.py" property
python "예제_examples/심화_advanced/systems/test_advanced_models.py" -v
```

## 출처 / Sources

- [Hypothesis: Replaying failed tests](https://hypothesis.readthedocs.io/en/latest/tutorial/replaying-failures.html): 반례 보존·database·example / preserving failures
- [Python: unittest](https://docs.python.org/3/library/unittest.html): 회귀 assertion과 suite 실행 / assertions and suite execution
