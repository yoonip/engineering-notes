# 알고리즘과 코딩테스트

[전체 목차](../../CATALOG.md) · [처음으로](../../README.md)

코딩테스트는 제한된 시간과 메모리 안에서 입력을 올바른 출력으로 바꾸는 문제다. 프로그래머스·백준·LeetCode·Codeforces·AtCoder·HackerRank·Codility·SWEA는 문제 형식과 실행 환경이 달라 같은 알고리즘도 입출력 코드를 다르게 작성한다.

## 알고리즘을 선택하는 기준

완전탐색은 가능한 경우를 직접 조사하고, 정렬은 원소의 순서를 이용할 수 있게 한다. 해시는 빠른 키 조회에, 스택·큐는 처리 순서 유지에 쓰인다. BFS는 가중치가 같은 그래프의 최단 경로, Dijkstra는 음수 간선이 없는 그래프의 최단 경로에 쓰인다. 동적 계획법은 겹치는 부분 문제의 결과를 저장하며, 그리디는 각 단계의 선택이 전체 최적해로 이어진다는 근거가 필요하다.

## 이진 탐색의 경계

아래 함수는 정렬된 배열에서 `target` 이상인 첫 위치를 찾는다. 답이 항상 반열린 구간 `[left, right)`의 경계로 남도록 범위를 줄인다.

```python
def lower_bound(values, target):
    left, right = 0, len(values)
    while left < right:
        mid = (left + right) // 2
        if values[mid] < target:
            left = mid + 1
        else:
            right = mid
    return left
```

`[1, 3, 3, 7]`에서 3을 찾으면 1, 4를 찾으면 3, 8을 찾으면 4다. 시간 복잡도는 `O(log n)`, 추가 공간은 `O(1)`이다. 빈 배열, 중복 값, 범위 밖의 값이 경계 처리를 확인하는 입력이다. 실제 지원 전형과 관련된 내용은 [지원·시험 기록](../55-applications-assessments/README.md)에서 다룬다.

## 관련 기술

프로그래머스 / Programmers, 백준 / Baekjoon, LeetCode, Codeforces, AtCoder, HackerRank, Codility, SWEA

## 참고 자료

- [프로그래머스 코딩테스트 연습](https://school.programmers.co.kr/learn/challenges)

## Programmers 풀이

[Level 2 Python 풀이 100개](../../programmers/README.md)를 문제 번호와 공식 문제 링크로 정리했다. 각 파일에서 실행 코드와 풀이를 확인할 수 있다.
