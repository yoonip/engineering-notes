# 단체사진 찍기

[Level 2 목록 / Level 2 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/1835) · Level 2 · C++

## 문제와 조건 / Task and conditions

친구는 A,C,F,J,M,N,R,T의 8명, 조건은 1~100개입니다. 간격은 사이 사람 수 0~6이고 연산은 =,<,>입니다. 모두 만족하는 일렬 배치 수를 반환합니다.

There are eight friends A,C,F,J,M,N,R,T and 1–100 constraints. A gap counts intervening people (0–6), compared with =,<,>. Return lineups satisfying every rule.

## 풀이 흐름 / Approach

친구 여덟 명의 40320가지 순서를 모두 검사합니다. 각 순서에서 친구별 위치를 기록한 뒤 두 친구 사이 사람 수 abs(위치 차이)−1이 조건을 만족하는지 확인합니다.

Inspect all 40320 orders of the eight friends. Build a position lookup for each order and check that abs(position difference)−1 satisfies every distance constraint.

## 정답이 되는 이유 / Why it works

여덟 명의 순열은 가능한 모든 사진 배치를 정확히 한 번씩 포함합니다. 모든 조건을 동시에 만족하는 배치만 더하므로 결과가 정확합니다.

The permutations contain every possible lineup exactly once. Counting only those satisfying every constraint gives exactly the valid lineups.

## 비용 / Complexity

조건 q개에 시간 O(8!·(8+q)), 공간 O(8+q) / O(8!·(8+q)) time, O(8+q) space

## 구현 / Implementation

[solution.cpp](solution.cpp)

```cpp
#include <string>
#include <vector>
#include <algorithm>
#include <cstdlib>
using namespace std;

// 조건 목록을 받아 가능한 순서 수를 반환하는 함수.
int solution(int n, vector<string> data) {
    string friends = "ACFJMNRT";
    // 최초 사전순 순열.
    vector<int> order{0, 1, 2, 3, 4, 5, 6, 7};
    int answer = 0;
    do {
        // 친구별 현재 위치 저장.
        int positions[8];
        for (int i = 0; i < 8; ++i) positions[order[i]] = i;
        // 현재 순서의 조건 만족 여부.
        bool valid = true;
        for (const string &condition : data) {
            // 첫 친구 번호 조회.
            int first = friends.find(condition[0]);
            int second = friends.find(condition[2]);
            // 위치 차이에서 본인 한 칸을 빼 두 친구 사이 사람 수 계산.
            int gap = abs(positions[first] - positions[second]) - 1;
            char op = condition[3];
            // 숫자 문자에서 '0'을 빼 정수 간격으로 변환.
            int wanted = condition[4] - '0';
            if ((op == '=' && gap != wanted) || (op == '<' && gap >= wanted) || (op == '>' && gap <= wanted)) {
                // 조건 하나라도 어기면 유효하지 않음.
                valid = false;
                break;
            }
        }
        if (valid) ++answer;
    // 다음 순열이 있으면 계속하고 마지막이면 종료.
    } while (next_permutation(order.begin(), order.end()));
    return answer;
}
```

## 다른 방법: 부분 배치 백트래킹 / Partial-lineup backtracking

한 명씩 놓으며 두 친구가 이미 배치된 조건만 먼저 검사합니다. 위반한 접두부는 끝까지 만들지 않아 강한 조건이 많을수록 순열 전수 검사보다 탐색을 줄입니다.

Place friends one at a time and check constraints whose endpoints are both placed. Rejecting invalid prefixes can prune much more than complete-permutation enumeration.

[alternative.py](alternative.py)

```python
def solution(n, data):
    positions = {}
    friends = 'ACFJMNRT'
    def valid():
        for rule in data:
            a, b, op, distance = rule[0], rule[2], rule[3], int(rule[4])
            if a not in positions or b not in positions:
                continue
            actual = abs(positions[a] - positions[b]) - 1
            if not {'=': actual == distance, '<': actual < distance, '>': actual > distance}[op]:
                return False
        return True
    def place():
        if len(positions) == 8:
            return 1
        count = 0
        for friend in friends:
            if friend not in positions:
                positions[friend] = len(positions)
                if valid():
                    count += place()
                del positions[friend]
        return count
    return place()
```

## 예시 / Example

공식 예제의 입력 인자와 결과입니다.

Input arguments and result from an official example.

```json
{
  "input": [
    2,
    [
      "N~F=0",
      "R~T>2"
    ]
  ],
  "output": 3648
}
```

## 검증 / Verification

```bash
python verify.py
```

원본 채점 기록과 별도로 로컬 검증 9개를 통과했습니다. 검증 입력·예상 결과는 [cases.json](cases.json), 재현 코드는 [verify.py](verify.py), 실행 기록은 [verification.json](verification.json)에 있습니다.

Separately from the original grading record, 9 local cases passed. Inputs and expected results are in [cases.json](cases.json), the reproducer is [verify.py](verify.py), and the run record is [verification.json](verification.json).

[Python 비교 구현](solution.py)도 함께 제공합니다. 로컬 검증 대상은 Python 비교 구현이며 C++ 원본 채점 기록은 별도입니다.

A [Python counterpart](solution.py) is included. Local Python checks are separate from the original C++ grading record.

비교 구현은 작은 입력 9개에서 함께 통과했습니다. 큰 입력용 제출 풀이와 전수 탐색 기준 코드는 파일명과 설명으로 구분합니다.

The comparison also passed 9 small-input cases. Exhaustive reference implementations are distinguished from the submission solution in their filenames and descriptions.

원본 채점 기록: 100점. [submitted_original.cpp](submitted_original.cpp)는 당시 원본 파일을 그대로 보존하며, `solution.cpp`는 설명을 정리한 구현입니다.

Original recorded grade: 100/100. [submitted_original.cpp](submitted_original.cpp) preserves the original file bytes; `solution.cpp` contains the documented implementation.

출처: [프로그래머스 문제 1835](https://school.programmers.co.kr/learn/courses/30/lessons/1835), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 1835](https://school.programmers.co.kr/learn/courses/30/lessons/1835), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.

[Python 비교 원본 / Stored Python comparison source](submitted_original.py)
