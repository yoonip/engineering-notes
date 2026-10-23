# 주차 요금 계산

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/92341) · Level 2 · C++

## 풀이

차량별 입차 시각과 누적 주차 시간을 계산하고 기본 시간을 넘은 시간을 단위별로 올림해 요금 구하기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <algorithm>
#include <map>
#include <sstream>
#include <string>
#include <vector>
using namespace std;

vector<int> solution(vector<int> fees, vector<string> records) {
    map<int, int> entered, totals;
    for (const string& record : records) {
        string time, action; int car;
        istringstream input(record); input >> time >> car >> action;
        int now = stoi(time.substr(0, 2)) * 60 + stoi(time.substr(3, 2));
        if (action == "IN") entered[car] = now;
        else { totals[car] += now - entered[car]; entered.erase(car); }
    }
    for (const auto& entry : entered) totals[entry.first] += 1439 - entry.second;
    vector<int> answer;
    for (const auto& entry : totals) {
        int extra = max(0, entry.second - fees[0]);
        answer.push_back(fees[1] + (extra + fees[2] - 1) / fees[2] * fees[3]);
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <map>  // 키를 정렬해 보관하는 map
// #include <sstream>  // 문자열에서 공백 단위로 값을 읽는 스트림
// #include <string>  // 문자열을 담는 string
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// vector<int> solution(vector<int> fees, vector<string> records) {  // 차량별 주차 시간을 모아 기본·단위 요금 계산
// map<int, int> entered, totals;  // 차량 번호 순서로 입차 시각과 누적 주차 시간 저장
// for (const string& record : records) {  // 입출차 기록을 순서대로 읽기
// string time, action; int car;  // 시각, 차량 번호, 입출차 종류를 저장할 변수 선언
// istringstream input(record); input >> time >> car >> action;  // 공백으로 나뉜 기록을 스트림으로 읽기
// int now = stoi(time.substr(0, 2)) * 60 + stoi(time.substr(3, 2));  // 시각을 자정 이후의 분으로 바꾸기
// if (action == "IN") entered[car] = now;  // 입차이면 현재 시각 기록
// else { totals[car] += now - entered[car]; entered.erase(car); }  // 출차이면 주차 시간을 더하고 입차 기록 제거
// }  // 블록 끝
// for (const auto& entry : entered) totals[entry.first] += 1439 - entry.second;  // 출차 기록이 없는 차는 23시 59분에 출차한 것으로 계산
// vector<int> answer;  // 차량 번호 오름차순의 요금 저장
// for (const auto& entry : totals) {  // map이 제공하는 차량 번호 순서로 처리
// int extra = max(0, entry.second - fees[0]);  // 기본 시간을 넘은 분 수 구하기
// answer.push_back(fees[1] + (extra + fees[2] - 1) / fees[2] * fees[3]);  // 초과 시간을 올림 나눗셈해 기본 요금에 더하기
// }  // 블록 끝
// return answer;  // 차량별 주차 요금 반환
// }  // 블록 끝

// 풀이 요약
// 차량별 입차 시각과 누적 주차 시간을 계산하고 기본 시간을 넘은 시간을 단위별로 올림해 요금 구하기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:37:16
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level2/045_92341_%EC%A3%BC%EC%B0%A8_%EC%9A%94%EA%B8%88_%EA%B3%84%EC%82%B0/README.md)
