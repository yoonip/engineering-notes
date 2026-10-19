# [1차] 캐시

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/17680) · Level 2 · Python3

## 문제와 조건 / Task and conditions

용량은 0~30, 도시는 최대 100000개이며 영문 도시명은 최대 20자입니다. 대소문자는 무시하고 LRU를 쓰며 hit=1, miss=5의 총비용을 반환합니다.

Capacity is 0–30; there are at most 100000 city names of at most 20 letters. Ignore case, use LRU, and return total cost with hit=1 and miss=5.

## 풀이 흐름 / Approach

도시 이름을 소문자로 통일합니다. 최근에 쓴 항목을 순서 사전의 끝에 두고, 캐시 적중이면 맨 뒤로 옮깁니다. 누락이면 새 항목을 넣고 용량을 넘을 때 가장 오래된 첫 항목을 뺍니다.

Normalize city names to lowercase. Keep recently used entries at the end of an ordered dictionary, moving hits there and evicting the oldest front entry when capacity is exceeded.

## 정답이 되는 이유 / Why it works

순서 사전은 사용 시각이 오래된 순서를 항상 유지합니다. 맨 앞을 제거하는 동작은 정확히 LRU 정책이며 hit·miss마다 정해진 비용을 더하면 총 실행 시간입니다.

The ordered dictionary maintains entries from least to most recently used. Removing its first entry implements LRU exactly; adding the specified hit/miss costs gives the total.

## 비용 / Complexity

전체 도시 문자 수 L에 평균 시간 O(L), 공간 O(cacheSize) / Average O(L) time, O(cacheSize) space

## 구현 / Implementation

[solution.py](solution.py)

```python
from collections import OrderedDict

def solution(cacheSize, cities):
    cache = OrderedDict()
    time = 0
    for city in cities:
        city = city.lower()
        if city in cache:
            cache.move_to_end(city)
            time += 1
        else:
            time += 5
            if cacheSize:
                cache[city] = None
                if len(cache) > cacheSize:
                    cache.popitem(last=False)
    return time
```

## 다른 방법: 작은 deque 캐시 / Small deque cache

캐시에서 도시를 직접 찾고 적중한 항목을 지운 뒤 뒤로 붙입니다. 시간 O(n·cacheSize)이지만 문제의 작은 캐시 용량에서는 간단한 비교 구현입니다.

Find and remove a hit from a deque before appending it. This costs O(n·cacheSize), but is a simple comparison implementation for the problem’s small cache capacity.

[alternative.py](alternative.py)

```python
from collections import deque

def solution(cacheSize, cities):
    cache = deque(maxlen=cacheSize)
    time = 0
    for city in cities:
        city = city.lower()
        if city in cache:
            cache.remove(city)
            time += 1
        else:
            time += 5
        cache.append(city)
    return time
```

## 예시 / Example

공식 예제의 입력 인자와 결과입니다.

Input arguments and result from an official example.

```json
{
  "input": [
    3,
    [
      "Jeju",
      "Pangyo",
      "Seoul",
      "NewYork",
      "LA",
      "Jeju",
      "Pangyo",
      "Seoul",
      "NewYork",
      "LA"
    ]
  ],
  "output": 50
}
```

## 검증 / Verification

```bash
python verify.py
```

원본 채점 기록과 별도로 로컬 검증 34개를 통과했습니다. 검증 입력·예상 결과는 [cases.json](cases.json), 재현 코드는 [verify.py](verify.py), 실행 기록은 [verification.json](verification.json)에 있습니다.

Separately from the original grading record, 34 local cases passed. Inputs and expected results are in [cases.json](cases.json), the reproducer is [verify.py](verify.py), and the run record is [verification.json](verification.json).

비교 구현은 작은 입력 34개에서 함께 통과했습니다. 큰 입력용 제출 풀이와 전수 탐색 기준 코드는 파일명과 설명으로 구분합니다.

The comparison also passed 34 small-input cases. Exhaustive reference implementations are distinguished from the submission solution in their filenames and descriptions.

원본 채점 기록: 100점. [submitted_original.py](submitted_original.py)는 당시 원본 파일을 그대로 보존하며, `solution.py`는 설명을 정리한 구현입니다.

Original recorded grade: 100/100. [submitted_original.py](submitted_original.py) preserves the original file bytes; `solution.py` contains the documented implementation.

출처: [프로그래머스 문제 17680](https://school.programmers.co.kr/learn/courses/30/lessons/17680), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 17680](https://school.programmers.co.kr/learn/courses/30/lessons/17680), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.
