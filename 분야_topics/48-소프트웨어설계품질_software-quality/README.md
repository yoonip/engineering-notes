# 소프트웨어 설계와 품질 | Software Quality, Design & Testing

[전체 목차](../../분야별목차_CATALOG.md) · [처음으로](../../README.md)

소프트웨어 품질을 볼 때는 요구한 동작이 유지되는지, 변경의 영향을 파악할 수 있는지 살펴봅니다. 모듈 경계, 데이터 소유권, 오류 처리, 테스트 가능성이 유지보수에 영향을 줍니다.

## 테스트의 범위

단위 테스트는 작은 구성요소, 통합 테스트는 연결, 시스템 테스트는 전체 동작을 다룹니다. Property-based test는 특정 예시 대신 항상 성립해야 하는 성질과 입력 생성을 이용합니다. 회귀 테스트는 이전에 해결한 문제나 유지할 동작을 확인합니다. 구현을 그대로 복제한 테스트는 같은 오류를 함께 가질 수 있습니다.

## 분석과 진단

pytest·unittest는 Python, GoogleTest·Catch2·CTest는 C/C++ 테스트에 쓰입니다. Hypothesis는 속성 기반 입력 생성에 쓰입니다. ASan·UBSan·TSan·Valgrind는 메모리·정의되지 않은 동작·동시성 등의 진단에, clang-tidy·Ruff는 정적 검사와 코드 정리에 사용됩니다.

Profiler는 시간을 쓰는 위치, 메모리 도구는 할당·수명과 접근, log는 실행 중 사건을 보여줍니다. 코드 리뷰에서는 API 계약, 경계 입력, 실패한 뒤의 상태, 변경 범위를 함께 살핍니다. 주석은 코드가 이미 말하는 동작을 반복하기보다 선택의 이유와 제약을 남길 때 유용합니다.

## 관련 기술

pytest, unittest, GoogleTest, Catch2, CTest, Hypothesis, Valgrind, ASan/UBSan/TSan, clang-tidy, Ruff

## 참고 자료

- [pytest documentation](https://docs.pytest.org/en/stable/)

## 기초 해설

- [소프트웨어 검증: 예제, 계약과 변환 성질](해설_notes/소프트웨어검증_contracts-properties-metamorphic-testing.md)

## 복구 프로그램의 종료값을 해석하는 방법

프로그램의 종료값은 그 프로그램이 정한 계약으로 읽습니다. 모든 도구에서 0만 정상, 나머지는 같은 실패라는 해석을 적용하면 결과를 잘못 분류할 수 있습니다. [e2fsck의 EXIT CODE](https://man7.org/linux/man-pages/man8/e2fsck.8.html)는 오류 없음 0, 수정됨 1, 수정 후 재부팅 필요 2, 미수정 오류 4, 실행 오류 8 등의 조건을 합산한다고 설명합니다.

아래는 문서의 종료값을 해석하는 계산입니다. e2fsck를 실행하거나 실제 파일시스템을 고치는 코드가 아닙니다. 예를 들어 5는 `1+4`여서 일부를 수정했어도 미수정 오류가 남았다는 뜻입니다. 3은 `1+2`이므로 수정 여부와 재부팅 조건을 함께 읽어야 합니다.

```python
flags = {1: "corrected", 2: "reboot", 4: "uncorrected", 8: "operational", 16: "usage", 32: "cancelled", 128: "library"}  # {}는 비트 값과 의미를 연결하는 사전입니다.
def explain(code):  # def는 종료값 하나를 받는 함수를 정의합니다.
    if type(code) is not int or not 0 <= code <= 255 or code & 64:  # bool·범위 밖·문서에 없는 비트는 거부합니다.
        raise ValueError("unsupported exit code")  # raise는 지원 범위 밖 입력을 알립니다.
    return [name for bit, name in flags.items() if code & bit] or ["clean"]  # &로 켜진 비트를 골라 리스트로 만듭니다.
for code in (0, 1, 3, 4, 5, 8):  # ()는 순서가 있는 tuple이며 for로 순회합니다.
    print(code, explain(code))  # 코드와 모든 적용 조건을 함께 출력합니다.
```

도구 실행의 성공, 파일시스템 구조의 일관성, 모든 파일의 내용 보존은 서로 다른 판정입니다. 검사기가 정상 종료해도 아직 복구할 오류가 있을 수 있고, 구조를 고쳤어도 원래 이름이나 자료를 잃었을 수 있습니다. 결과에는 적용한 도구·옵션·종료값·검사 보고서·입력과 출력의 식별자를 함께 남깁니다.

## 빠진 파일을 놓치는 검사와 멱등성의 한계

복구한 파일 하나의 자료가 맞다는 검사만으로 필요한 파일이 모두 돌아왔는지 알 수 없습니다. 직접 만든 기대 파일은 a·b 두 개인데 결과가 a만 있는 경우를 보겠습니다.

```python
expected = {"a": b"A", "b": b"B"}  # b 접두사는 bytes이며 사전은 기대 이름과 자료를 묶습니다.
for restored in ({"a": b"A"}, {}):  # 파일 하나가 빠진 결과와 빈 결과를 차례로 살펴봅니다.
    matching = all(data == expected[name] for name, data in restored.items())  # 실제 결과에 있는 자료만 검사합니다.
    complete = set(restored) == set(expected)  # set은 이름의 집합이며 누락·추가를 함께 비교합니다.
    print(matching, complete)  # 두 경우 모두 True False이며 내용 비교만으로는 부족합니다.
```

[Python의 all](https://docs.python.org/3.12/library/functions.html#all)은 빈 입력에서도 True입니다. 관측 표본이 없다는 사실과 모든 기대 표본이 일치했다는 사실을 구분해야 합니다. 반대로 실제 환경에 원래 이름과 자료의 신뢰할 목록이 없다면, 목록을 알고 있는 시험의 기대값을 현장에서도 알고 있는 것처럼 취급하지 않습니다.

멱등성은 같은 복구를 두 번 적용해도 결과가 더 바뀌지 않는 성질입니다. 그러나 모든 파일을 지우는 잘못된 복구도 두 번째에는 같은 빈 상태가 되므로 멱등성 하나만으로 정답을 증명할 수 없습니다. 원본 불변, 허용한 변경 범위, 구조 검사, 기대 자료 보존, 정보가 부족한 경우의 거부를 함께 비교합니다.

[파일시스템 검사와 복구](../../설계와검증사례_engineering-cases/파일시스템의손상검사와복구계획_filesystem-check-repair.md)와 [파일 이름·블록 소유권](../../설계와검증사례_engineering-cases/파일이름과블록소유권의복구_filesystem-orphans-block-ownership.md)은 이 차이를 실제로 생성한 교육용 이미지 파일에서 다룹니다. 실제 ext4와 e2fsck의 실행 결과는 별개입니다.

## English

### Software design and quality

Software quality depends on preserving required behavior and understanding the effects of changes. Module boundaries, data ownership, error handling, and testability all affect maintainability.

### Test scope

Unit tests cover small components, integration tests cover their connections, and system tests cover overall behavior. Property-based testing generates inputs and checks properties that should always hold. Regression tests check behavior that must be preserved, including previously fixed problems. A test that simply duplicates the implementation can duplicate its errors as well.

### Analysis and diagnosis

pytest and unittest support Python testing. GoogleTest, Catch2, and CTest serve C/C++ workflows, while Hypothesis generates inputs for property-based tests. ASan, UBSan, TSan, and Valgrind help diagnose memory errors, undefined behavior, and concurrency problems. clang-tidy and Ruff provide static checks and code cleanup.

A profiler shows where time is spent. Memory tools examine allocations, lifetimes, and accesses, while logs record runtime events. Code review considers API contracts, boundary inputs, state after failures, and the scope of a change. Comments are useful when they explain reasons and constraints that the code alone does not show.

### Foundation article

- [소프트웨어 검증: 예제, 계약과 변환 성질](해설_notes/소프트웨어검증_contracts-properties-metamorphic-testing.md#english)


### Repair results, completeness and idempotence

Exit codes belong to a tool's contract. e2fsck combines condition bits, so 5 reports both correction and remaining errors. The example decodes documented values without running e2fsck. A successful process, structurally consistent metadata and preserved original content are separate observations.

Checking only returned files misses omissions; Python all also returns true for an empty iterable. Expected identities and content must be checked when a trusted inventory exists. Repair idempotence is useful but insufficient: deleting everything is also idempotent. The linked educational image cases combine unchanged originals, bounded repair actions, structural checks, content expectations and explicit refusal of ambiguous repairs.


## 심화 해설 | Advanced article

- [테스트가 실패한 뒤: 재현 가능한 반례와 shrinking](해설_notes/실패입력줄이기_property-counterexample-shrinking.md) · [English](해설_notes/실패입력줄이기_property-counterexample-shrinking.md#english)
