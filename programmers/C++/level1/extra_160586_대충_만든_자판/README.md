# 대충 만든 자판

[레벨 1 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/160586) · Level 1 · C++

## 풀이

각 문자를 가장 적게 눌러 입력할 수 있는 횟수를 미리 기록. 목표 문자열마다 이를 합하고, 입력 불가능한 문자가 있으면 -1.

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

vector<int> solution(vector<string> keymap, vector<string> targets) {
    int presses[26]; fill(presses, presses + 26, INT_MAX);
    for (const string& keys : keymap) for (int i = 0; i < (int)keys.size(); ++i) presses[keys[i] - 'A'] = min(presses[keys[i] - 'A'], i + 1);
    vector<int> answer;
    for (const string& target : targets) {
        int total = 0;
        for (char c : target) { if (presses[c - 'A'] == INT_MAX) { total = -1; break; } total += presses[c - 'A']; }
        answer.push_back(total);
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
// vector<int> solution(vector<string> keymap, vector<string> targets) {  // 대충 만든 자판 풀이 함수 정의
//     int presses[26]; fill(presses, presses + 26, INT_MAX);  // 26개 대문자의 최소 누름 수를 아직 찾지 못했다는 INT_MAX로 초기화
//     for (const string& keys : keymap) for (int i = 0; i < (int)keys.size(); ++i) presses[keys[i] - 'A'] = min(presses[keys[i] - 'A'], i + 1);  // 각 키의 문자 위치 i + 1을 누름 수로 보고 문자별 최솟값 갱신
//     vector<int> answer;  // 목표별 누름 수를 담을 결과 배열 준비
//     for (const string& target : targets) {  // 목표 문자열을 하나씩 처리
//         int total = 0;  // 현재 목표의 누름 수 합 total을 0으로 시작
//         for (char c : target) { if (presses[c - 'A'] == INT_MAX) { total = -1; break; } total += presses[c - 'A']; }  // 불가능한 문자가 있으면 -1로 끝내고, 가능한 문자는 최소 누름 수 합산
//         answer.push_back(total);  // 현재 목표의 결과를 배열에 추가
//     }  // 블록 끝
//     return answer;  // 각 목표 문자열의 최소 누름 수 반환
// }  // 함수 끝
//

// 풀이 요약
// 각 문자를 가장 적게 눌러 입력할 수 있는 횟수를 미리 기록. 목표 문자열마다 이를 합하고, 입력 불가능한 문자가 있으면 -1.
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:07:13
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level1/extra_160586_%EB%8C%80%EC%B6%A9_%EB%A7%8C%EB%93%A0_%EC%9E%90%ED%8C%90/README.md)
