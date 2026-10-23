# 점 찍기

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/140107) · Level 2 · C++

## 풀이

k의 배수인 x좌표마다 원 안의 y상한을 정수 제곱근으로 구해 k의 배수인 y좌표 수를 더하기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <cmath>
using namespace std;

long long solution(int k, int d) {
    long long answer = 0;
    for (long long x = 0; x <= d; x += k) {
        long long square = 1LL * d * d - x * x;
        long long max_y = (long long)sqrtl((long double)square);
        while ((max_y + 1) * (max_y + 1) <= square) ++max_y;
        while (max_y * max_y > square) --max_y;
        answer += max_y / k + 1;
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <cmath>  // 제곱근·거듭제곱 같은 수학 함수
// using namespace std;  // std:: 접두사 생략
// long long solution(int k, int d) {  // 원 안의 k 간격 격자점 개수 계산
// long long answer = 0;  // 조건을 만족하는 격자점 수 초기화
// for (long long x = 0; x <= d; x += k) {  // x좌표를 k의 배수로 순회
// long long square = 1LL * d * d - x * x;  // 원 안쪽에서 허용하는 y제곱의 상한 계산
// long long max_y = (long long)sqrtl((long double)square);  // y상한의 정수 제곱근 후보 구하기
// while ((max_y + 1) * (max_y + 1) <= square) ++max_y;  // 부동소수점 오차로 작은 후보를 보정하기
// while (max_y * max_y > square) --max_y;  // 부동소수점 오차로 큰 후보를 보정하기
// answer += max_y / k + 1;  // y=0을 포함해 k의 배수인 좌표 수를 더하기
// }  // 블록 끝
// return answer;  // 전체 격자점 수 반환
// }  // 블록 끝

// 풀이 요약
// k의 배수인 x좌표마다 원 안의 y상한을 정수 제곱근으로 구해 k의 배수인 y좌표 수를 더하기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:34:23
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level2/034_140107_%EC%A0%90_%EC%B0%8D%EA%B8%B0/README.md)
