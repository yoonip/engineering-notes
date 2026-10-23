# 바탕화면 정리

[레벨 1 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/161990) · Level 1 · C++

## 풀이

파일 칸의 위·왼쪽 최솟값과 아래·오른쪽 다음 좌표의 최댓값을 구해 드래그 영역 생성.

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

vector<int> solution(vector<string> wallpaper) {
    int top = (int)wallpaper.size(), left = (int)wallpaper[0].size(), bottom = 0, right = 0;
    for (int r = 0; r < (int)wallpaper.size(); ++r) for (int c = 0; c < (int)wallpaper[r].size(); ++c) if (wallpaper[r][c] == '#') {
        top = min(top, r); left = min(left, c); bottom = max(bottom, r + 1); right = max(right, c + 1);
    }
    return {top, left, bottom, right};
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
// vector<int> solution(vector<string> wallpaper) {  // 바탕화면 정리 풀이 함수 정의
//     int top = (int)wallpaper.size(), left = (int)wallpaper[0].size(), bottom = 0, right = 0;  // 파일을 감쌀 위·왼쪽 경계는 큰 값, 아래·오른쪽 경계는 0으로 초기화
//     for (int r = 0; r < (int)wallpaper.size(); ++r) for (int c = 0; c < (int)wallpaper[r].size(); ++c) if (wallpaper[r][c] == '#') {  // 바탕화면 전체에서 파일 표시 #가 있는 칸만 검사
//         top = min(top, r); left = min(left, c); bottom = max(bottom, r + 1); right = max(right, c + 1);  // 행·열 최솟값과 칸 끝 좌표 r + 1·c + 1의 최댓값으로 네 경계 갱신
//     }  // 블록 끝
//     return {top, left, bottom, right};  // 파일을 모두 포함하는 시작 행·열과 끝 행·열 반환
// }  // 함수 끝
//

// 풀이 요약
// 파일 칸의 위·왼쪽 최솟값과 아래·오른쪽 다음 좌표의 최댓값을 구해 드래그 영역 생성.
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:06:16
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level1/extra_161990_%EB%B0%94%ED%83%95%ED%99%94%EB%A9%B4_%EC%A0%95%EB%A6%AC/README.md)
