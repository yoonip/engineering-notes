# 전화번호 목록

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/42577) · Level 2 · C++

## 풀이

전화번호를 사전순 정렬한 뒤 이웃한 번호 사이의 접두사 관계만 검사

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <algorithm>
#include <string>
#include <vector>
using namespace std;

bool solution(vector<string> phone_book) {
    sort(phone_book.begin(), phone_book.end());
    for (int i = 0; i + 1 < (int)phone_book.size(); ++i) {
        if (phone_book[i + 1].compare(0, phone_book[i].size(), phone_book[i]) == 0) return false;
    }
    return true;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <string>  // 문자열을 담는 string
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// bool solution(vector<string> phone_book) {  // 사전순 이웃 전화번호의 접두사 여부 확인
// sort(phone_book.begin(), phone_book.end());  // 접두사가 있는 번호들이 이웃하도록 사전순 정렬
// for (int i = 0; i + 1 < (int)phone_book.size(); ++i) {  // 이웃한 전화번호만 비교
// if (phone_book[i + 1].compare(0, phone_book[i].size(), phone_book[i]) == 0) return false;  // 앞 번호가 다음 번호의 접두사이면 일관성이 없음
// }  // 블록 끝
// return true;  // 접두사 관계가 없으면 참 반환
// }  // 블록 끝

// 풀이 요약
// 전화번호를 사전순 정렬한 뒤 이웃한 번호 사이의 접두사 관계만 검사
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:26:00
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level2/085_42577_%EC%A0%84%ED%99%94%EB%B2%88%ED%98%B8_%EB%AA%A9%EB%A1%9D/README.md)
