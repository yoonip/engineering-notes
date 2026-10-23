# 두 원 사이의 정수 쌍

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181187) · Level 2 · C++

## 풀이

각 양의 x좌표에서 큰 원의 y상한과 작은 원 바깥의 y하한을 정수 제곱근으로 구해 세고 네 방향의 대칭 적용

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <algorithm>
#include <cmath>
using namespace std;

static long long integer_sqrt(long long value) {
    long long root = (long long)sqrtl((long double)value);
    while ((root + 1) * (root + 1) <= value) ++root;
    while (root * root > value) --root;
    return root;
}

long long solution(int r1, int r2) {
    long long answer = 0;
    for (long long x = 1; x <= r2; ++x) {
        long long high = integer_sqrt(1LL * r2 * r2 - x * x);
        long long inner = max(0LL, 1LL * r1 * r1 - x * x);
        long long low = integer_sqrt(inner);
        if (low * low < inner) ++low;
        answer += high - low + 1;
    }
    return answer * 4;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <cmath>  // 제곱근·거듭제곱 같은 수학 함수
// using namespace std;  // std:: 접두사 생략
// static long long integer_sqrt(long long value) {  // 반올림 오차를 보정해 정수 제곱근 구하기
// long long root = (long long)sqrtl((long double)value);  // 실수 제곱근으로 정수 제곱근 후보 구하기
// while ((root + 1) * (root + 1) <= value) ++root;  // 반올림으로 작게 잡힌 후보를 보정하기
// while (root * root > value) --root;  // 반올림으로 크게 잡힌 후보를 보정하기
// return root;  // 바닥 정수 제곱근 반환
// }  // 블록 끝
// long long solution(int r1, int r2) {  // 두 원 사이의 정수 좌표를 한 사분면에서 세기
// long long answer = 0;  // 한쪽 사분면에서 세는 격자점 수 초기화
// for (long long x = 1; x <= r2; ++x) {  // y축을 제외한 양의 x좌표를 순회
// long long high = integer_sqrt(1LL * r2 * r2 - x * x);  // 큰 원 안쪽의 최대 y좌표 구하기
// long long inner = max(0LL, 1LL * r1 * r1 - x * x);  // 작은 원 경계 밖에 필요한 y제곱의 하한 구하기
// long long low = integer_sqrt(inner);  // y좌표 하한의 바닥 제곱근 구하기
// if (low * low < inner) ++low;  // 제곱수가 아니면 올림해 작은 원 내부를 제외
// answer += high - low + 1;  // 두 경계 사이의 정수 y좌표 개수를 더하기
// }  // 블록 끝
// return answer * 4;  // 대칭인 네 방향의 격자점 수 반환
// }  // 블록 끝

// 풀이 요약
// 각 양의 x좌표에서 큰 원의 y상한과 작은 원 바깥의 y하한을 정수 제곱근으로 구해 세고 네 방향의 대칭 적용
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:28:13
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level2/015_181187_%EB%91%90_%EC%9B%90_%EC%82%AC%EC%9D%B4%EC%9D%98_%EC%A0%95%EC%88%98_%EC%8C%8D/README.md)
