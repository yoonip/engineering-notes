# 오픈채팅방

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/42888) · Level 2 · C++

## 풀이

아이디별 최종 닉네임을 먼저 기록하고 시간순 입퇴장 사건에 최종 닉네임을 반영해 메시지 만들기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <sstream>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>
using namespace std;

vector<string> solution(vector<string> record) {
    unordered_map<string, string> names;
    vector<pair<string, string>> events;
    for (const string& entry : record) {
        string action, user, nickname; istringstream input(entry); input >> action >> user;
        if (action != "Leave") { input >> nickname; names[user] = nickname; }
        if (action != "Change") events.push_back({user, action});
    }
    vector<string> answer;
    for (const auto& event : events) answer.push_back(names[event.first] + (event.second == "Enter" ? "님이 들어왔습니다." : "님이 나갔습니다."));
    return answer;
}

// 전체 코드 줄별 설명
// #include <sstream>  // 문자열에서 공백 단위로 값을 읽는 스트림
// #include <string>  // 문자열을 담는 string
// #include <unordered_map>  // 키로 값을 찾는 해시 맵
// #include <utility>  // 두 값을 묶는 pair와 이동 유틸리티
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// vector<string> solution(vector<string> record) {  // 최종 닉네임을 입퇴장 기록에 적용
// unordered_map<string, string> names;  // 사용자 아이디별 최종 닉네임 저장
// vector<pair<string, string>> events;  // 입장과 퇴장 사건만 시간순으로 저장
// for (const string& entry : record) {  // 채팅방 기록을 순서대로 읽기
// string action, user, nickname; istringstream input(entry); input >> action >> user;  // 동작과 사용자 아이디를 분리
// if (action != "Leave") { input >> nickname; names[user] = nickname; }  // 입장이나 변경이면 최종 닉네임 갱신
// if (action != "Change") events.push_back({user, action});  // 닉네임 변경을 제외한 사건 기록
// }  // 블록 끝
// vector<string> answer;  // 최종 닉네임이 반영된 메시지 저장
// for (const auto& event : events) answer.push_back(names[event.first] + (event.second == "Enter" ? "님이 들어왔습니다." : "님이 나갔습니다."));  // 사건 종류에 맞는 한국어 메시지 만들기
// return answer;  // 모든 입퇴장 메시지 반환
// }  // 블록 끝

// 풀이 요약
// 아이디별 최종 닉네임을 먼저 기록하고 시간순 입퇴장 사건에 최종 닉네임을 반영해 메시지 만들기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:20:29
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level2/071_42888_%EC%98%A4%ED%94%88%EC%B1%84%ED%8C%85%EB%B0%A9/README.md)
