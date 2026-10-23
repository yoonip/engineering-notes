# 영어 끝말잇기

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/12981) · Level 2 · C++

## 풀이

이전에 쓴 단어인지와 직전 단어의 마지막 글자가 현재 첫 글자와 같은지 검사해 최초 탈락자의 번호와 차례 구하기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <string>
#include <unordered_set>
#include <vector>
using namespace std;

vector<int> solution(int n, vector<string> words) {
    unordered_set<string> seen;
    for (int i = 0; i < (int)words.size(); ++i) {
        if (seen.count(words[i]) || (i > 0 && words[i - 1].back() != words[i].front())) return {i % n + 1, i / n + 1};
        seen.insert(words[i]);
    }
    return {0, 0};
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 담는 string
// #include <unordered_set>  // 중복을 걸러 낼 해시 집합
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// vector<int> solution(int n, vector<string> words) {  // 중복 단어와 첫·끝 글자로 최초 탈락자 찾기
// unordered_set<string> seen;  // 이미 사용한 단어 저장
// for (int i = 0; i < (int)words.size(); ++i) {  // 끝말잇기 단어를 시간순으로 검사
// if (seen.count(words[i]) || (i > 0 && words[i - 1].back() != words[i].front())) return {i % n + 1, i / n + 1};  // 중복이나 잘못된 연결을 발견하면 사람 번호와 차례 반환
// seen.insert(words[i]);  // 정상 단어를 사용한 집합에 넣기
// }  // 블록 끝
// return {0, 0};  // 탈락자가 없으면 0 두 개 반환
// }  // 블록 끝

// 풀이 요약
// 이전에 쓴 단어인지와 직전 단어의 마지막 글자가 현재 첫 글자와 같은지 검사해 최초 탈락자의 번호와 차례 구하기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:31:41
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level2/094_12981_%EC%98%81%EC%96%B4_%EB%81%9D%EB%A7%90%EC%9E%87%EA%B8%B0/README.md)
