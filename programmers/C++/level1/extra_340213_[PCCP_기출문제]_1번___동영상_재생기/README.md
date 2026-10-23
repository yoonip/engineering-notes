# [PCCP 기출문제] 1번 / 동영상 재생기

[레벨 1 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/340213) · Level 1 · C++

## 풀이

MM:SS를 초로 바꿔 계산. 명령마다 영상 범위 안에서 10초 이동하고, 시작 시각과 이동 후 시각이 오프닝 구간이면 끝으로 건너뜀.

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

static int seconds_of(const string& time) { return stoi(time.substr(0, 2)) * 60 + stoi(time.substr(3)); }
string solution(string video_len, string pos, string op_start, string op_end, vector<string> commands) {
    int end = seconds_of(video_len), current = seconds_of(pos), opening = seconds_of(op_start), closing = seconds_of(op_end);
    if (opening <= current && current <= closing) current = closing;
    for (const string& command : commands) {
        current = command == "prev" ? max(0, current - 10) : min(end, current + 10);
        if (opening <= current && current <= closing) current = closing;
    }
    char result[6];
    snprintf(result, sizeof(result), "%02d:%02d", current / 60, current % 60);
    return string(result);
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
// static int seconds_of(const string& time) { return stoi(time.substr(0, 2)) * 60 + stoi(time.substr(3)); }  // 분과 초 부분을 stoi로 읽어 전체 초로 바꾸는 보조 함수
// string solution(string video_len, string pos, string op_start, string op_end, vector<string> commands) {  // [PCCP 기출문제] 1번 / 동영상 재생기 풀이 함수 정의
//     int end = seconds_of(video_len), current = seconds_of(pos), opening = seconds_of(op_start), closing = seconds_of(op_end);  // 영상 끝 end, 현재 위치 current, 오프닝 시작 opening과 끝 closing을 초로 변환
//     if (opening <= current && current <= closing) current = closing;  // 처음 위치가 오프닝 구간 안이면 오프닝 끝으로 이동
//     for (const string& command : commands) {  // 이동 명령을 주어진 순서대로 처리
//         current = command == "prev" ? max(0, current - 10) : min(end, current + 10);  // prev면 0초 이상에서 10초 뒤로, next면 영상 끝 이하에서 10초 앞으로 이동
//         if (opening <= current && current <= closing) current = closing;  // 이동한 위치가 오프닝 구간 안이면 다시 오프닝 끝으로 이동
//     }  // 블록 끝
//     char result[6];  // MM:SS와 문자열 끝 문자를 담을 6칸 버퍼 준비
//     snprintf(result, sizeof(result), "%02d:%02d", current / 60, current % 60);  // 분과 초를 두 자리 숫자로 맞춰 결과 버퍼에 기록
//     return string(result);  // 결과 버퍼를 string으로 바꿔 반환
// }  // 함수 끝
//

// 풀이 요약
// MM:SS를 초로 바꿔 계산. 명령마다 영상 범위 안에서 10초 이동하고, 시작 시각과 이동 후 시각이 오프닝 구간이면 끝으로 건너뜀.
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:02:57
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level1/extra_340213_%5BPCCP_%EA%B8%B0%EC%B6%9C%EB%AC%B8%EC%A0%9C%5D_1%EB%B2%88___%EB%8F%99%EC%98%81%EC%83%81_%EC%9E%AC%EC%83%9D%EA%B8%B0/README.md)
