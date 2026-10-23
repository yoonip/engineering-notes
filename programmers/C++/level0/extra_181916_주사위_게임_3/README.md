# 주사위 게임 3

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181916) · Level 0 · C++

## 풀이

각 눈의 출현 횟수를 세어 네 개 같음, 세 개 같음, 두 쌍, 한 쌍, 모두 다름을 구분

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <cstdlib>
using namespace std;

int solution(int a, int b, int c, int d) {
    int counts[7] = {0};
    ++counts[a]; ++counts[b]; ++counts[c]; ++counts[d];
    for (int p = 1; p <= 6; ++p) {
        if (counts[p] == 4) return 1111 * p;
        if (counts[p] == 3) {
            for (int q = 1; q <= 6; ++q) if (counts[q] == 1) return (10 * p + q) * (10 * p + q);
        }
        if (counts[p] == 2) {
            int product = 1;
            for (int q = 1; q <= 6; ++q) {
                if (q != p && counts[q] == 2) return (p + q) * abs(p - q);
                if (counts[q] == 1) product *= q;
            }
            return product;
        }
    }
    for (int p = 1; p <= 6; ++p) if (counts[p]) return p;
    return 0;
}

// 전체 코드 줄별 설명
// #include <cstdlib>  // 정수 변환과 절댓값 등 표준 함수
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// int solution(int a, int b, int c, int d) {  // 주사위 게임 3 풀이 시작
//     int counts[7] = {0};  // 인덱스 1부터 6까지 각 주사위 눈의 횟수를 담을 배열을 0으로 초기화
//     ++counts[a]; ++counts[b]; ++counts[c]; ++counts[d];  // 전위 증가 연산자 ++로 네 눈 각각의 출현 횟수를 늘립니다
//     for (int p = 1; p <= 6; ++p) {  // for로 주사위 눈 1부터 6까지의 출현 횟수를 검사
//         if (counts[p] == 4) return 1111 * p;  // if로 네 눈이 모두 같은지 확인하고 해당 점수 1111p를 반환
//         if (counts[p] == 3) {  // if로 세 번 나온 눈을 찾아 나머지 한 눈과 함께 계산
//             for (int q = 1; q <= 6; ++q) if (counts[q] == 1) return (10 * p + q) * (10 * p + q);  // 한 번 나온 눈 q를 for로 찾아 세 번 나온 눈 p와 규칙에 맞게 제곱 점수를 계산
//         }  // 블록 끝
//         if (counts[p] == 2) {  // if로 두 번 나온 눈을 찾아 두 쌍 또는 한 쌍인 경우를 처리
//             int product = 1;  // 곱셈의 항등원인 1로 나머지 두 눈의 곱을 초기화
//             for (int q = 1; q <= 6; ++q) {  // for로 다른 눈의 횟수를 검사해 두 쌍 또는 한 쌍인 경우를 구분
//                 if (q != p && counts[q] == 2) return (p + q) * abs(p - q);  // 다른 눈도 두 번 나왔으면 두 쌍의 점수를 abs로 절댓값을 구해 반환
//                 if (counts[q] == 1) product *= q;  // 한 번 나온 눈만 골라 *=로 나머지 두 눈의 곱을 누적
//             }  // 블록 끝
//             return product;  // 한 쌍을 제외한 서로 다른 두 눈의 곱을 반환
//         }  // 블록 끝
//     }  // 블록 끝
//     for (int p = 1; p <= 6; ++p) if (counts[p]) return p;  // 1부터 순회하며 처음 발견한 눈을 반환해 모두 다른 경우의 최솟값을 구하기
//     return 0;  // 조건에 맞는 경우가 없으면 0 반환
// }  // 블록 끝

// 풀이 요약
// 각 눈의 출현 횟수를 세어 네 개 같음, 세 개 같음, 두 쌍, 한 쌍, 모두 다름을 구분
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:50:30
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181916_%EC%A3%BC%EC%82%AC%EC%9C%84_%EA%B2%8C%EC%9E%84_3/README.md)
