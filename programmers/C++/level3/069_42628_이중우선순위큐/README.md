# 이중우선순위큐

[레벨 3 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/42628) · Level 3 · C++

## 풀이

중복을 허용하는 정렬 집합으로 삽입과 최솟값 또는 최댓값 한 개 삭제 처리

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <set>
#include <string>
#include <vector>
using namespace std;

vector<int> solution(vector<string> operations) {
    multiset<int> values;
    for (const string& operation : operations) {
        int value = stoi(operation.substr(2));
        if (operation[0] == 'I') values.insert(value);
        else if (!values.empty()) { if (value == 1) values.erase(prev(values.end())); else values.erase(values.begin()); }
    }
    if (values.empty()) return {0,0};
    return {*values.rbegin(),*values.begin()};
}

// 전체 코드 줄별 설명
// #include <set>  // 정렬된 집합과 중복을 허용하는 multiset
// #include <string>  // 문자열을 담는 string
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// vector<int> solution(vector<string> operations) {  // 최솟값·최댓값 삭제를 함께 지원하는 정렬 집합
// multiset<int> values;  // 중복 값을 허용하며 최솟값과 최댓값을 함께 관리
// for (const string& operation : operations) {  // 삽입과 삭제 명령을 순서대로 처리
// int value = stoi(operation.substr(2));  // 명령의 정수 인자 읽기
// if (operation[0] == 'I') values.insert(value);  // 삽입 명령이면 값 추가
// else if (!values.empty()) { if (value == 1) values.erase(prev(values.end())); else values.erase(values.begin()); }  // 비어 있지 않으면 지정한 최대 또는 최소 원소 하나를 삭제
// }  // 블록 끝
// if (values.empty()) return {0,0};  // 빈 큐는 0 두 개 반환
// return {*values.rbegin(),*values.begin()};  // 남은 최댓값과 최솟값 반환
// }  // 블록 끝

// 풀이 요약
// 중복을 허용하는 정렬 집합으로 삽입과 최솟값 또는 최댓값 한 개 삭제 처리
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:45:44
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level3/069_42628_%EC%9D%B4%EC%A4%91%EC%9A%B0%EC%84%A0%EC%88%9C%EC%9C%84%ED%81%90/README.md)
