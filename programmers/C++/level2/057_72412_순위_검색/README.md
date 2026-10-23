# 순위 검색

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/72412) · Level 2 · C++

## 풀이

각 지원자를 모든 값 허용 여부의 16개 조건에 등록하고 조건별 점수를 정렬해 질의 점수 하한을 이분 탐색

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <algorithm>
#include <array>
#include <sstream>
#include <string>
#include <unordered_map>
#include <vector>
using namespace std;

vector<int> solution(vector<string> info, vector<string> query) {
    unordered_map<string, vector<int>> table;
    for (const string& record : info) {
        array<string, 4> fields; int score;
        istringstream input(record); input >> fields[0] >> fields[1] >> fields[2] >> fields[3] >> score;
        for (int mask = 0; mask < 16; ++mask) {
            string key;
            for (int i = 0; i < 4; ++i) key += ((mask & (1 << i)) ? "-" : fields[i]) + "/";
            table[key].push_back(score);
        }
    }
    for (auto& entry : table) sort(entry.second.begin(), entry.second.end());
    vector<int> answer;
    for (const string& request : query) {
        string a, b, c, d, conjunction; int minimum;
        istringstream input(request); input >> a >> conjunction >> b >> conjunction >> c >> conjunction >> d >> minimum;
        string key = a + "/" + b + "/" + c + "/" + d + "/";
        auto found = table.find(key);
        if (found == table.end()) answer.push_back(0);
        else { const auto& scores = found->second; answer.push_back((int)(scores.end() - lower_bound(scores.begin(), scores.end(), minimum))); }
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <array>  // 크기가 고정된 array
// #include <sstream>  // 문자열에서 공백 단위로 값을 읽는 스트림
// #include <string>  // 문자열을 담는 string
// #include <unordered_map>  // 키로 값을 찾는 해시 맵
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// vector<int> solution(vector<string> info, vector<string> query) {  // 조건 조합별 점수를 모아 기준 이상 인원 검색
// unordered_map<string, vector<int>> table;  // 조건 조합별로 지원자 점수 목록 저장
// for (const string& record : info) {  // 지원자 정보 읽기
// array<string, 4> fields; int score;  // 네 속성과 점수를 저장할 변수 선언
// istringstream input(record); input >> fields[0] >> fields[1] >> fields[2] >> fields[3] >> score;  // 공백으로 나뉜 다섯 항목 읽기
// for (int mask = 0; mask < 16; ++mask) {  // 속성을 실제 값 또는 모든 값으로 처리하는 16개 조합 만들기
// string key;  // 현재 조건의 문자열 키 초기화
// for (int i = 0; i < 4; ++i) key += ((mask & (1 << i)) ? "-" : fields[i]) + "/";  // 구분자를 넣어 네 조건 연결
// table[key].push_back(score);  // 해당 조건에 맞는 지원자 점수 등록
// }  // 블록 끝
// }  // 블록 끝
// for (auto& entry : table) sort(entry.second.begin(), entry.second.end());  // 각 조건의 점수를 오름차순으로 정렬
// vector<int> answer;  // 요청별 지원자 수 저장
// for (const string& request : query) {  // 질의를 하나씩 처리
// string a, b, c, d, conjunction; int minimum;  // 조건, 연결어, 점수 하한 저장
// istringstream input(request); input >> a >> conjunction >> b >> conjunction >> c >> conjunction >> d >> minimum;  // and를 건너뛰며 네 조건과 점수 읽기
// string key = a + "/" + b + "/" + c + "/" + d + "/";  // 정보 등록 때와 같은 조건 키 만들기
// auto found = table.find(key);  // 조건에 해당하는 지원자 목록 찾기
// if (found == table.end()) answer.push_back(0);  // 목록이 없으면 0명 기록
// else { const auto& scores = found->second; answer.push_back((int)(scores.end() - lower_bound(scores.begin(), scores.end(), minimum))); }  // 이분 탐색으로 점수 하한 이상인 지원자 수 구하기
// }  // 블록 끝
// return answer;  // 모든 질의의 답 반환
// }  // 블록 끝

// 풀이 요약
// 각 지원자를 모든 값 허용 여부의 16개 조건에 등록하고 조건별 점수를 정렬해 질의 점수 하한을 이분 탐색
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:40:14
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level2/057_72412_%EC%88%9C%EC%9C%84_%EA%B2%80%EC%83%89/README.md)
