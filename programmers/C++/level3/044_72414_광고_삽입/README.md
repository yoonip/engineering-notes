# 광고 삽입

[레벨 3 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/72414) · Level 3 · C++

## 풀이

시청 시작과 종료 변화량으로 누적 시청 시간을 계산하고 고정 길이 광고 구간의 시청량이 최대인 가장 이른 시작점 고르기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <iomanip>
#include <sstream>
#include <string>
#include <vector>
using namespace std;

string solution(string play_time, string adv_time, vector<string> logs) {
    auto seconds = [](const string& text) { return stoi(text.substr(0,2)) * 3600 + stoi(text.substr(3,2)) * 60 + stoi(text.substr(6,2)); };
    int play = seconds(play_time), adv = seconds(adv_time);
    vector<int> difference(play + 1, 0);
    for (const string& log : logs) { ++difference[seconds(log.substr(0,8))]; --difference[seconds(log.substr(9,8))]; }
    vector<long long> prefix(play + 1, 0); int viewers = 0;
    for (int time = 0; time < play; ++time) { viewers += difference[time]; prefix[time + 1] = prefix[time] + viewers; }
    int best_start = 0; long long best_total = -1;
    for (int start = 0; start + adv <= play; ++start) { long long total = prefix[start + adv] - prefix[start]; if (total > best_total) { best_total = total; best_start = start; } }
    ostringstream output; output << setfill('0') << setw(2) << best_start / 3600 << ':' << setw(2) << best_start / 60 % 60 << ':' << setw(2) << best_start % 60;
    return output.str();
}

// 전체 코드 줄별 설명
// #include <iomanip>  // 문자열 출력의 자리 수와 채움 문자 설정
// #include <sstream>  // 문자열에서 공백 단위로 값을 읽는 스트림
// #include <string>  // 문자열을 담는 string
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// string solution(string play_time, string adv_time, vector<string> logs) {  // 누적 시청 시간이 최대인 광고 시작 시각 찾기
// auto seconds = [](const string& text) { return stoi(text.substr(0,2)) * 3600 + stoi(text.substr(3,2)) * 60 + stoi(text.substr(6,2)); };  // 시, 분, 초 문자열을 전체 초로 바꾸기
// int play = seconds(play_time), adv = seconds(adv_time);  // 전체 재생 시간과 광고 길이 구하기
// vector<int> difference(play + 1, 0);  // 초별 시청자 수의 변화량 저장
// for (const string& log : logs) { ++difference[seconds(log.substr(0,8))]; --difference[seconds(log.substr(9,8))]; }  // 시청 시작에 더하고 종료에 빼기
// vector<long long> prefix(play + 1, 0); int viewers = 0;  // 누적 시청 시간과 현재 시청자 수 저장
// for (int time = 0; time < play; ++time) { viewers += difference[time]; prefix[time + 1] = prefix[time] + viewers; }  // 시청자 변화량을 적분해 누적 시청 시간 구하기
// int best_start = 0; long long best_total = -1;  // 최적 광고 시작점과 누적 시청량 초기화
// for (int start = 0; start + adv <= play; ++start) { long long total = prefix[start + adv] - prefix[start]; if (total > best_total) { best_total = total; best_start = start; } }  // 고정 길이 광고 구간의 최대 누적 시청량 찾기
// ostringstream output; output << setfill('0') << setw(2) << best_start / 3600 << ':' << setw(2) << best_start / 60 % 60 << ':' << setw(2) << best_start % 60;  // 최적 시작점을 두 자리 시각 형식으로 만들기
// return output.str();  // 광고 시작 시각 반환
// }  // 블록 끝

// 풀이 요약
// 시청 시작과 종료 변화량으로 누적 시청 시간을 계산하고 고정 길이 광고 구간의 시청량이 최대인 가장 이른 시작점 고르기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:56:34
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level3/044_72414_%EA%B4%91%EA%B3%A0_%EC%82%BD%EC%9E%85/README.md)
