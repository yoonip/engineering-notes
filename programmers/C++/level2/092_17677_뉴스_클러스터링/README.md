# [1차] 뉴스 클러스터링

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/17677) · Level 2 · C++

## 풀이

영문 두 글자 조각의 다중집합을 만들고 중복 빈도의 최소값과 최대값으로 자카드 유사도 계산

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <algorithm>
#include <cctype>
#include <map>
#include <string>
using namespace std;

int solution(string str1, string str2) {
    auto pairs = [](string text) {
        for (char& c : text) c = (char)tolower((unsigned char)c);
        map<string, int> counts;
        for (int i = 0; i + 1 < (int)text.size(); ++i) if (text[i] >= 'a' && text[i] <= 'z' && text[i + 1] >= 'a' && text[i + 1] <= 'z') ++counts[text.substr(i, 2)];
        return counts;
    };
    auto first = pairs(str1), second = pairs(str2);
    int intersection = 0, total = 0;
    for (const auto& entry : first) { total += entry.second; auto found = second.find(entry.first); if (found != second.end()) intersection += min(entry.second, found->second); }
    for (const auto& entry : second) total += entry.second;
    int united = total - intersection;
    return united == 0 ? 65536 : (int)(1LL * intersection * 65536 / united);
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <cctype>  // 문자 분류와 대소문자 변환
// #include <map>  // 키를 정렬해 보관하는 map
// #include <string>  // 문자열을 담는 string
// using namespace std;  // std:: 접두사 생략
// int solution(string str1, string str2) {  // 두 글자 다중집합의 교집합·합집합 크기 계산
// auto pairs = [](string text) {  // 두 글자씩 끊은 알파벳 다중집합 만들기
// for (char& c : text) c = (char)tolower((unsigned char)c);  // 대소문자를 통일
// map<string, int> counts;  // 두 글자 조각별 중복 횟수 저장
// for (int i = 0; i + 1 < (int)text.size(); ++i) if (text[i] >= 'a' && text[i] <= 'z' && text[i + 1] >= 'a' && text[i + 1] <= 'z') ++counts[text.substr(i, 2)];  // 두 문자 모두 영문 알파벳인 조각만 세기
// return counts;  // 조각의 다중집합 반환
// };  // 블록 끝
// auto first = pairs(str1), second = pairs(str2);  // 두 문자열의 다중집합 구하기
// int intersection = 0, total = 0;  // 교집합 크기와 두 집합 크기의 합 초기화
// for (const auto& entry : first) { total += entry.second; auto found = second.find(entry.first); if (found != second.end()) intersection += min(entry.second, found->second); }  // 공통 조각의 최소 빈도를 교집합에 더하기
// for (const auto& entry : second) total += entry.second;  // 두 번째 다중집합의 크기를 합계에 더하기
// int united = total - intersection;  // 합계에서 교집합을 한 번 빼 합집합 크기 구하기
// return united == 0 ? 65536 : (int)(1LL * intersection * 65536 / united);  // 공집합 예외를 처리하고 자카드 유사도를 정수로 반환
// }  // 블록 끝

// 풀이 요약
// 영문 두 글자 조각의 다중집합을 만들고 중복 빈도의 최소값과 최대값으로 자카드 유사도 계산
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:30:09
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level2/092_17677_%EB%89%B4%EC%8A%A4_%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0%EB%A7%81/README.md)
