# 중요한 단어를 스포 방지

[레벨 1 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/468370) · Level 1 · C++

## 풀이

가려진 구간은 차분 배열과 누적합으로 표시. 단어에 가려진 글자가 하나라도 있으면 숨은 단어로 분류하고, 보이는 곳에도 나온 단어는 제외.

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

int solution(string message, vector<vector<int>> spoiler_ranges) {
    int n = (int)message.size();
    vector<int> difference(n + 1, 0);
    for (const auto& range : spoiler_ranges) { ++difference[range[0]]; --difference[range[1] + 1]; }
    unordered_set<string> visible, hidden;
    int cover = 0, start = 0;
    bool covered = false;
    for (int i = 0; i <= n; ++i) {
        if (i < n) cover += difference[i];
        if (i == n || message[i] == ' ') {
            if (i > start) { string word = message.substr(start, i - start); if (covered) hidden.insert(word); else visible.insert(word); }
            start = i + 1; covered = false;
        } else if (cover > 0) covered = true;
    }
    int answer = 0;
    for (const string& word : hidden) if (!visible.count(word)) ++answer;
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
// int solution(string message, vector<vector<int>> spoiler_ranges) {  // 중요한 단어를 스포 방지 풀이 함수 정의
//     int n = (int)message.size();  // message의 문자 수 n 저장
//     vector<int> difference(n + 1, 0);  // 가려진 구간의 시작과 끝 변화를 기록할 차분 배열 준비
//     for (const auto& range : spoiler_ranges) { ++difference[range[0]]; --difference[range[1] + 1]; }  // 구간 시작에서 덮인 수를 늘리고 구간 끝 다음 위치에서 줄임
//     unordered_set<string> visible, hidden;  // 중복 없이 보이는 단어 visible과 가려진 단어 hidden을 따로 저장
//     int cover = 0, start = 0;  // 현재 위치의 덮인 수 cover와 현재 단어 시작 start를 0으로 초기화
//     bool covered = false;  // 현재 단어에 가려진 문자가 있는지 covered로 기록
//     for (int i = 0; i <= n; ++i) {  // 마지막 단어도 처리하도록 문자열 끝 위치 n까지 검사
//         if (i < n) cover += difference[i];  // 현재 위치에 걸친 가림 구간 수를 누적
//         if (i == n || message[i] == ' ') {  // 문자열 끝이나 공백이면 한 단어가 끝남
//             if (i > start) { string word = message.substr(start, i - start); if (covered) hidden.insert(word); else visible.insert(word); }  // 빈 단어가 아니면 substr로 꺼내 covered에 따라 hidden 또는 visible에 저장
//             start = i + 1; covered = false;  // 다음 단어 시작을 옮기고 가려짐 여부 초기화
//         } else if (cover > 0) covered = true;  // 공백이 아닌 문자가 가려졌으면 현재 단어 전체를 숨은 단어로 표시
//     }  // 블록 끝
//     int answer = 0;  // 보이는 곳에 없는 숨은 단어 수를 0부터 셈
//     for (const string& word : hidden) if (!visible.count(word)) ++answer;  // hidden의 각 단어 중 visible에 없는 단어만 하나씩 셈
//     return answer;  // 중복을 제외한 숨은 단어 수 반환
// }  // 함수 끝
//

// 풀이 요약
// 가려진 구간은 차분 배열과 누적합으로 표시. 단어에 가려진 글자가 하나라도 있으면 숨은 단어로 분류하고, 보이는 곳에도 나온 단어는 제외.
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:00:40
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level1/extra_468370_%EC%A4%91%EC%9A%94%ED%95%9C_%EB%8B%A8%EC%96%B4%EB%A5%BC_%EC%8A%A4%ED%8F%AC_%EB%B0%A9%EC%A7%80/README.md)
