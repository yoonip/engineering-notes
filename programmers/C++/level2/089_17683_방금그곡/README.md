# [3차] 방금그곡

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/17683) · Level 2 · C++

## 풀이

샵 음을 한 문자로 바꾸고 실제 재생 시간만큼 반복한 멜로디에서 기억한 멜로디를 찾아 가장 오래 재생된 곡 고르기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <cctype>
#include <sstream>
#include <string>
#include <vector>
using namespace std;

string solution(string m, vector<string> musicinfos) {
    auto normalize = [](const string& score) {
        string result;
        for (int i = 0; i < (int)score.size(); ++i) {
            if (i + 1 < (int)score.size() && score[i + 1] == '#') { result += char(tolower((unsigned char)score[i])); ++i; }
            else result += score[i];
        }
        return result;
    };
    string target = normalize(m), answer = "(None)"; int longest = -1;
    for (const string& info : musicinfos) {
        vector<string> fields; string part; istringstream input(info);
        while (getline(input, part, ',')) fields.push_back(part);
        auto minute = [](const string& time) { return stoi(time.substr(0, 2)) * 60 + stoi(time.substr(3, 2)); };
        int duration = minute(fields[1]) - minute(fields[0]);
        string melody = normalize(fields[3]), played;
        for (int i = 0; i < duration; ++i) played += melody[i % melody.size()];
        if (played.find(target) != string::npos && duration > longest) { answer = fields[2]; longest = duration; }
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <cctype>  // 문자 분류와 대소문자 변환
// #include <sstream>  // 문자열에서 공백 단위로 값을 읽는 스트림
// #include <string>  // 문자열을 담는 string
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// string solution(string m, vector<string> musicinfos) {  // 샵 음을 정규화해 재생 멜로디에서 일치 곡 찾기
// auto normalize = [](const string& score) {  // 샵이 붙은 음을 한 문자로 바꾸기
// string result;  // 음별로 한 문자가 되는 문자열 만들기
// for (int i = 0; i < (int)score.size(); ++i) {  // 악보의 음들 읽기
// if (i + 1 < (int)score.size() && score[i + 1] == '#') { result += char(tolower((unsigned char)score[i])); ++i; }  // 샵 음은 소문자로 바꾸고 샵 문자를 건너뛰기
// else result += score[i];  // 일반 음은 그대로 저장
// }  // 블록 끝
// return result;  // 정규화한 악보 반환
// };  // 블록 끝
// string target = normalize(m), answer = "(None)"; int longest = -1;  // 기억한 멜로디와 선택 결과 및 재생 시간 초기화
// for (const string& info : musicinfos) {  // 방송된 음악 정보를 순서대로 확인
// vector<string> fields; string part; istringstream input(info);  // 쉼표로 나뉜 정보를 읽을 스트림 만들기
// while (getline(input, part, ',')) fields.push_back(part);  // 시작, 끝, 제목, 악보를 분리
// auto minute = [](const string& time) { return stoi(time.substr(0, 2)) * 60 + stoi(time.substr(3, 2)); };  // 시각을 분으로 바꾸기
// int duration = minute(fields[1]) - minute(fields[0]);  // 재생 시간 구하기
// string melody = normalize(fields[3]), played;  // 정규화한 악보와 실제 재생 멜로디 저장
// for (int i = 0; i < duration; ++i) played += melody[i % melody.size()];  // 재생 시간만큼 악보를 반복
// if (played.find(target) != string::npos && duration > longest) { answer = fields[2]; longest = duration; }  // 기억한 멜로디를 포함하는 가장 긴 곡 고르기
// }  // 블록 끝
// return answer;  // 조건에 맞는 제목 또는 None 반환
// }  // 블록 끝

// 풀이 요약
// 샵 음을 한 문자로 바꾸고 실제 재생 시간만큼 반복한 멜로디에서 기억한 멜로디를 찾아 가장 오래 재생된 곡 고르기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:28:21
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level2/089_17683_%EB%B0%A9%EA%B8%88%EA%B7%B8%EA%B3%A1/README.md)
