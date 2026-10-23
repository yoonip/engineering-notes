# 브라이언의 고민

[레벨 3 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/1830) · Level 3 · C++

## 풀이

소문자 표식의 전체 등장 위치를 확인해 단어 내부 교대 규칙과 바깥 감싸기 규칙을 검사하고 접두사별 가능한 단어 경계 복원

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <algorithm>
#include <array>
#include <string>
#include <vector>
using namespace std;

string solution(string sentence) {
    int n = (int)sentence.size(); if (n == 0) return "invalid";
    array<vector<int>,26> positions;
    for (int i = 0; i < n; ++i) { char c = sentence[i]; if (c >= 'a' && c <= 'z') positions[c - 'a'].push_back(i); else if (c < 'A' || c > 'Z') return "invalid"; }
    auto read_word = [&](int left,int right) {
        if (left >= right || sentence[left] < 'A' || sentence[left] > 'Z') return string();
        bool uppercase = true; for (int i = left; i < right; ++i) if (sentence[i] < 'A' || sentence[i] > 'Z') uppercase = false;
        if (uppercase) return sentence.substr(left,right - left);
        int length = right - left; if (length % 2 == 0 || sentence[left + 1] < 'a' || sentence[left + 1] > 'z') return string();
        char marker = sentence[left + 1]; const auto& found = positions[marker - 'a'];
        if (found.front() != left + 1 || found.back() != right - 2 || (int)found.size() != length / 2) return string();
        string result;
        for (int i = 0; i < length; ++i) { char c = sentence[left + i]; if (i % 2 == 0) { if (c < 'A' || c > 'Z') return string(); result += c; } else if (c != marker) return string(); }
        return result;
    };
    vector<int> previous(n + 1,-2); vector<string> words(n + 1); previous[0] = -1;
    for (int start = 0; start < n; ++start) if (previous[start] != -2) {
        char c = sentence[start];
        if (c >= 'A' && c <= 'Z') {
            int end = start; while (end < n && sentence[end] >= 'A' && sentence[end] <= 'Z') { ++end; if (previous[end] == -2) { previous[end] = start; words[end] = sentence.substr(start,end - start); } }
            if (start + 1 < n && sentence[start + 1] >= 'a' && sentence[start + 1] <= 'z') {
                int finish = positions[sentence[start + 1] - 'a'].back() + 2;
                if (finish <= n) { string word = read_word(start,finish); if (!word.empty() && previous[finish] == -2) { previous[finish] = start; words[finish] = word; } }
            }
        } else {
            const auto& found = positions[c - 'a'];
            if (found.size() == 2 && found[0] == start) { int close = found[1]; string word = read_word(start + 1,close); if (!word.empty() && previous[close + 1] == -2) { previous[close + 1] = start; words[close + 1] = word; } }
        }
    }
    if (previous[n] == -2) return "invalid";
    vector<string> result; for (int end = n; end > 0; end = previous[end]) result.push_back(words[end]);
    reverse(result.begin(), result.end()); string answer; for (const string& word : result) { if (!answer.empty()) answer += ' '; answer += word; }
    return answer;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <array>  // 크기가 고정된 array
// #include <string>  // 문자열을 담는 string
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// string solution(string sentence) {  // 소문자 표식 규칙에 맞는 단어 경계 복원
// int n = (int)sentence.size(); if (n == 0) return "invalid";  // 비어 있는 문장은 유효하지 않음
// array<vector<int>,26> positions;  // 각 소문자 표식의 전체 등장 위치 저장
// for (int i = 0; i < n; ++i) { char c = sentence[i]; if (c >= 'a' && c <= 'z') positions[c - 'a'].push_back(i); else if (c < 'A' || c > 'Z') return "invalid"; }  // 영문 대소문자만 허용하고 표식 위치 모으기
// auto read_word = [&](int left,int right) {  // 반열린 구간이 한 단어의 내부 규칙을 만족하는지 검사
// if (left >= right || sentence[left] < 'A' || sentence[left] > 'Z') return string();  // 단어는 대문자로 시작하는 비어 있지 않은 구간이어야 함
// bool uppercase = true; for (int i = left; i < right; ++i) if (sentence[i] < 'A' || sentence[i] > 'Z') uppercase = false;  // 표식 없는 일반 대문자 단어인지 검사
// if (uppercase) return sentence.substr(left,right - left);  // 일반 단어이면 그대로 반환
// int length = right - left; if (length % 2 == 0 || sentence[left + 1] < 'a' || sentence[left + 1] > 'z') return string();  // 교대 표식 규칙의 길이와 첫 표식 확인
// char marker = sentence[left + 1]; const auto& found = positions[marker - 'a'];  // 내부 표식의 전체 위치 목록 읽기
// if (found.front() != left + 1 || found.back() != right - 2 || (int)found.size() != length / 2) return string();  // 같은 표식이 구간 밖이나 잘못된 수로 나타나면 제외
// string result;  // 표식을 제거한 대문자 단어 만들기
// for (int i = 0; i < length; ++i) { char c = sentence[left + i]; if (i % 2 == 0) { if (c < 'A' || c > 'Z') return string(); result += c; } else if (c != marker) return string(); }  // 대문자와 같은 표식이 번갈아 나오는지 검사
// return result;  // 규칙을 만족하는 원래 단어 반환
// };  // 블록 끝
// vector<int> previous(n + 1,-2); vector<string> words(n + 1); previous[0] = -1;  // 접두사를 해석할 수 있는지와 직전 단어 저장
// for (int start = 0; start < n; ++start) if (previous[start] != -2) {  // 해석 가능한 접두사 뒤에서 다음 단어 찾기
// char c = sentence[start];  // 다음 구간의 첫 문자 읽기
// if (c >= 'A' && c <= 'Z') {  // 대문자로 시작하면 일반 단어 또는 내부 표식 단어
// int end = start; while (end < n && sentence[end] >= 'A' && sentence[end] <= 'Z') { ++end; if (previous[end] == -2) { previous[end] = start; words[end] = sentence.substr(start,end - start); } }  // 연속 대문자 구간의 모든 단어 경계 등록
// if (start + 1 < n && sentence[start + 1] >= 'a' && sentence[start + 1] <= 'z') {  // 다음 글자가 내부 표식일 수 있는지 확인
// int finish = positions[sentence[start + 1] - 'a'].back() + 2;  // 표식 전체를 포함하는 단어 끝 구하기
// if (finish <= n) { string word = read_word(start,finish); if (!word.empty() && previous[finish] == -2) { previous[finish] = start; words[finish] = word; } }  // 내부 규칙이 맞으면 새 단어 경계 등록
// }  // 블록 끝
// } else {  // 소문자로 시작하면 단어를 감싸는 표식이어야 함
// const auto& found = positions[c - 'a'];  // 같은 표식의 모든 위치 읽기
// if (found.size() == 2 && found[0] == start) { int close = found[1]; string word = read_word(start + 1,close); if (!word.empty() && previous[close + 1] == -2) { previous[close + 1] = start; words[close + 1] = word; } }  // 정확히 두 표식 사이의 내부 단어를 해석
// }  // 블록 끝
// }  // 블록 끝
// if (previous[n] == -2) return "invalid";  // 전체 문장을 단어들로 나눌 수 없으면 유효하지 않음
// vector<string> result; for (int end = n; end > 0; end = previous[end]) result.push_back(words[end]);  // 저장한 이전 경계를 따라 단어들을 역순 복원
// reverse(result.begin(), result.end()); string answer; for (const string& word : result) { if (!answer.empty()) answer += ' '; answer += word; }  // 원래 순서의 단어를 공백으로 연결
// return answer;  // 복원한 문장 반환
// }  // 블록 끝

// 풀이 요약
// 소문자 표식의 전체 등장 위치를 확인해 단어 내부 교대 규칙과 바깥 감싸기 규칙을 검사하고 접두사별 가능한 단어 경계 복원
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:50:18
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level3/extra_1830_%EB%B8%8C%EB%9D%BC%EC%9D%B4%EC%96%B8%EC%9D%98_%EA%B3%A0%EB%AF%BC/README.md)
