# 숫자 카드 나누기

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/135807) · Level 2 · C++

## 풀이

두 배열 각각의 최대공약수를 구하고 반대 배열의 어떤 원소도 나누지 않는 후보 중 큰 값 선택

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <algorithm>
#include <numeric>
#include <vector>
using namespace std;

int solution(vector<int> arrayA, vector<int> arrayB) {
    int a = 0, b = 0;
    for (int value : arrayA) a = gcd(a, value);
    for (int value : arrayB) b = gcd(b, value);
    for (int value : arrayB) if (value % a == 0) { a = 0; break; }
    for (int value : arrayA) if (value % b == 0) { b = 0; break; }
    return max(a, b);
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <numeric>  // 누적합·최대공약수 같은 수치 알고리즘
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(vector<int> arrayA, vector<int> arrayB) {  // 반대 배열을 나누지 않는 최대공약수 후보 선택
// int a = 0, b = 0;  // 두 배열의 최대공약수 누적값 초기화
// for (int value : arrayA) a = gcd(a, value);  // A의 모든 원소의 최대공약수 구하기
// for (int value : arrayB) b = gcd(b, value);  // B의 모든 원소의 최대공약수 구하기
// for (int value : arrayB) if (value % a == 0) { a = 0; break; }  // A의 공약수가 B의 어떤 수를 나누면 후보에서 제외
// for (int value : arrayA) if (value % b == 0) { b = 0; break; }  // B의 공약수가 A의 어떤 수를 나누면 후보에서 제외
// return max(a, b);  // 두 방향에서 가능한 최대 후보 반환
// }  // 블록 끝

// 풀이 요약
// 두 배열 각각의 최대공약수를 구하고 반대 배열의 어떤 원소도 나누지 않는 후보 중 큰 값 선택
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:34:58
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level2/036_135807_%EC%88%AB%EC%9E%90_%EC%B9%B4%EB%93%9C_%EB%82%98%EB%88%84%EA%B8%B0/README.md)
