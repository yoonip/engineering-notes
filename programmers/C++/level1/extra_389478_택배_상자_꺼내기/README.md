# 택배 상자 꺼내기

[레벨 1 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/389478) · Level 1 · C++

## 풀이

상자의 줄과 열을 구한 뒤 위쪽 같은 열만 검사. 홀수 줄은 번호가 반대로 쌓이므로 열과 번호 계산을 뒤집음.

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <string>
#include <vector>
#include <algorithm>
#include <numeric>
#include <functional>
#include <unordered_set>
#include <unordered_map>
#include <sstream>
#include <cctype>
#include <cstdlib>
#include <cstdio>
#include <cmath>
#include <queue>
#include <set>
#include <climits>
#include <iostream>
using namespace std;

int solution(int n, int w, int num) {
    int row = (num - 1) / w, col = (num - 1) % w, answer = 0;
    if (row % 2) col = w - 1 - col;
    for (int r = row; r < (n + w - 1) / w; ++r) {
        int box = r % 2 == 0 ? r * w + col + 1 : (r + 1) * w - col;
        if (box <= n) ++answer;
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열 string 사용 준비
// #include <vector>  // 가변 길이 배열 vector 사용 준비
// #include <algorithm>  // 정렬·탐색·최솟값 등 표준 알고리즘 사용 준비
// #include <numeric>  // gcd·accumulate 등 수치 알고리즘 사용 준비
// #include <functional>  // 함수 래퍼와 greater 등 비교 함수 객체 사용 준비
// #include <unordered_set>  // 중복 없는 원소를 저장하는 해시 집합 사용 준비
// #include <unordered_map>  // 키로 값을 찾는 해시 맵 사용 준비
// #include <sstream>  // 문자열을 토큰으로 나눠 읽을 스트림 사용 준비
// #include <cctype>  // 숫자·대소문자 검사와 변환 함수 사용 준비
// #include <cstdlib>  // 정수 절댓값 등 표준 유틸리티 함수 사용 준비
// #include <cstdio>  // snprintf 등 형식 있는 입출력 함수 사용 준비
// #include <cmath>  // 제곱근 등 수학 함수 사용 준비
// #include <queue>  // FIFO 큐와 우선순위 큐 사용 준비
// #include <set>  // 중복 제거와 정렬을 함께 하는 집합 사용 준비
// #include <climits>  // 정수 범위 상수 사용 준비
// #include <iostream>  // cin·cout 표준 입출력 사용 준비
// using namespace std;  // 표준 이름의 std:: 접두사 생략
//
// int solution(int n, int w, int num) {  // 택배 상자 꺼내기 풀이 함수 정의
//     int row = (num - 1) / w, col = (num - 1) % w, answer = 0;  // num의 0기준 줄 row와 열 col을 계산하고 꺼낼 상자 수 answer를 0으로 시작
//     if (row % 2) col = w - 1 - col;  // 홀수 줄은 반대 방향이므로 실제 열 위치로 변환
//     for (int r = row; r < (n + w - 1) / w; ++r) {  // 찾은 상자의 줄부터 마지막으로 쌓인 줄까지 검사
//         int box = r % 2 == 0 ? r * w + col + 1 : (r + 1) * w - col;  // 줄의 짝홀에 따라 같은 열의 상자 번호 box 계산
//         if (box <= n) ++answer;  // 번호가 전체 상자 수 n 이하면 실제 상자이므로 하나 셈
//     }  // 블록 끝
//     return answer;  // 목표 상자를 포함해 같은 열에서 꺼낼 상자 수 반환
// }  // 함수 끝
//

// 풀이 요약
// 상자의 줄과 열을 구한 뒤 위쪽 같은 열만 검사. 홀수 줄은 번호가 반대로 쌓이므로 열과 번호 계산을 뒤집음.
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:01:48
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level1/extra_389478_%ED%83%9D%EB%B0%B0_%EC%83%81%EC%9E%90_%EA%BA%BC%EB%82%B4%EA%B8%B0/README.md)
