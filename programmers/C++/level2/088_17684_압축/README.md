# [3차] 압축

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/17684) · Level 2 · C++

## 풀이

현재 문자열을 사전에서 가능한 만큼 확장하고 더 확장할 수 없으면 번호를 출력한 뒤 새 문자열을 사전에 등록

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <string>
#include <unordered_map>
#include <vector>
using namespace std;

vector<int> solution(string msg) {
    unordered_map<string, int> dictionary;
    for (int i = 0; i < 26; ++i) dictionary[string(1, char('A' + i))] = i + 1;
    vector<int> answer; string word;
    int next_index = 27;
    for (char c : msg) {
        if (dictionary.count(word + c)) word += c;
        else {
            answer.push_back(dictionary[word]);
            dictionary[word + c] = next_index++;
            word = string(1, c);
        }
    }
    if (!word.empty()) answer.push_back(dictionary[word]);
    return answer;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 담는 string
// #include <unordered_map>  // 키로 값을 찾는 해시 맵
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// vector<int> solution(string msg) {  // 사전에서 가장 긴 문자열을 찾고 새 항목 추가
// unordered_map<string, int> dictionary;  // 문자열별 사전 번호 저장
// for (int i = 0; i < 26; ++i) dictionary[string(1, char('A' + i))] = i + 1;  // A부터 Z까지의 초기 사전 만들기
// vector<int> answer; string word;  // 출력 번호와 현재 가장 긴 사전 문자열 저장
// int next_index = 27;  // 새 문자열에 부여할 다음 번호 초기화
// for (char c : msg) {  // 메시지를 한 글자씩 읽기
// if (dictionary.count(word + c)) word += c;  // 현재 문자열을 더 길게 만들 수 있으면 이어 읽기
// else {  // 현재 문자열 뒤의 한 글자까지는 사전에 없음
// answer.push_back(dictionary[word]);  // 지금까지 찾은 가장 긴 문자열의 번호 출력
// dictionary[word + c] = next_index++;  // 한 글자를 확장한 새 문자열을 사전에 넣기
// word = string(1, c);  // 현재 글자부터 다음 문자열을 시작
// }  // 블록 끝
// }  // 블록 끝
// if (!word.empty()) answer.push_back(dictionary[word]);  // 마지막으로 남은 문자열의 번호 출력
// return answer;  // LZW 압축 번호 목록 반환
// }  // 블록 끝

// 풀이 요약
// 현재 문자열을 사전에서 가능한 만큼 확장하고 더 확장할 수 없으면 번호를 출력한 뒤 새 문자열을 사전에 등록
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:27:56
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level2/088_17684_%EC%95%95%EC%B6%95/README.md)
