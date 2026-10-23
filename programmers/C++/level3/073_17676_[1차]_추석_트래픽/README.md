# [1차] 추석 트래픽

[레벨 3 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/17676) · Level 3 · C++

## 풀이

소수 초를 정수 밀리초로 정확히 읽고 각 처리 종료 시각부터 1초 동안 겹치는 구간 수 비교

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <algorithm>
#include <sstream>
#include <string>
#include <utility>
#include <vector>
using namespace std;

int solution(vector<string> lines) {
    auto milliseconds = [](string text) {
        size_t dot = text.find('.'); string whole = dot == string::npos ? text : text.substr(0,dot), fraction = dot == string::npos ? "" : text.substr(dot + 1);
        while (fraction.size() < 3) fraction += '0';
        return stoi(whole) * 1000 + stoi(fraction.substr(0,3));
    };
    vector<pair<int,int>> intervals;
    for (const string& line : lines) {
        string date, clock, duration; istringstream input(line); input >> date >> clock >> duration;
        int end = (stoi(clock.substr(0,2)) * 3600 + stoi(clock.substr(3,2)) * 60) * 1000 + milliseconds(clock.substr(6));
        duration.pop_back(); int length = milliseconds(duration);
        intervals.push_back({end - length + 1,end});
    }
    int answer = 0;
    for (const auto& interval : intervals) {
        int time = interval.second, count = 0;
        for (const auto& other : intervals) count += other.first <= time + 999 && other.second >= time;
        answer = max(answer,count);
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <sstream>  // 문자열에서 공백 단위로 값을 읽는 스트림
// #include <string>  // 문자열을 담는 string
// #include <utility>  // 두 값을 묶는 pair와 이동 유틸리티
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(vector<string> lines) {  // 각 종료 시각의 1초 창에 겹치는 요청 수 비교
// auto milliseconds = [](string text) {  // 소수 초를 부동소수점 없이 밀리초로 읽기
// size_t dot = text.find('.'); string whole = dot == string::npos ? text : text.substr(0,dot), fraction = dot == string::npos ? "" : text.substr(dot + 1);  // 정수 부분과 소수 부분을 분리
// while (fraction.size() < 3) fraction += '0';  // 소수 세 자리까지 뒤에 0 채우기
// return stoi(whole) * 1000 + stoi(fraction.substr(0,3));  // 정수 밀리초 반환
// };  // 블록 끝
// vector<pair<int,int>> intervals;  // 각 처리의 양 끝을 포함하는 시간 구간 저장
// for (const string& line : lines) {  // 로그별 종료 시각과 처리 시간 읽기
// string date, clock, duration; istringstream input(line); input >> date >> clock >> duration;  // 공백으로 날짜와 시각 및 소요 시간을 분리
// int end = (stoi(clock.substr(0,2)) * 3600 + stoi(clock.substr(3,2)) * 60) * 1000 + milliseconds(clock.substr(6));  // 종료 시각을 정수 밀리초로 바꾸기
// duration.pop_back(); int length = milliseconds(duration);  // 초 단위 접미사를 제거하고 처리 길이 읽기
// intervals.push_back({end - length + 1,end});  // 시작과 종료를 모두 포함하는 처리 구간 저장
// }  // 블록 끝
// int answer = 0;  // 1초 안의 최대 동시 처리 수 초기화
// for (const auto& interval : intervals) {  // 각 종료 시각에서 시작하는 1초 창 검사
// int time = interval.second, count = 0;  // 창의 시작 시각과 겹치는 로그 수 초기화
// for (const auto& other : intervals) count += other.first <= time + 999 && other.second >= time;  // 1000밀리초 닫힌 창과 겹치는 구간 세기
// answer = max(answer,count);  // 최대 동시 처리 수 갱신
// }  // 블록 끝
// return answer;  // 초당 최대 처리량 반환
// }  // 블록 끝

// 풀이 요약
// 소수 초를 정수 밀리초로 정확히 읽고 각 처리 종료 시각부터 1초 동안 겹치는 구간 수 비교
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:46:41
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level3/073_17676_%5B1%EC%B0%A8%5D_%EC%B6%94%EC%84%9D_%ED%8A%B8%EB%9E%98%ED%94%BD/README.md)
