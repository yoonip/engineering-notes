# 할인 행사

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/131127) · Level 2 · C++

## 풀이

열흘 길이의 할인 창을 하루씩 이동하며 상품별 수량이 원하는 수량과 일치하는 시작일 세기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <string>
#include <unordered_map>
#include <vector>
using namespace std;

int solution(vector<string> want, vector<int> number, vector<string> discount) {
    unordered_map<string, int> needed, current;
    for (int i = 0; i < (int)want.size(); ++i) needed[want[i]] = number[i];
    int answer = 0;
    for (int day = 0; day < (int)discount.size(); ++day) {
        ++current[discount[day]];
        if (day >= 10 && --current[discount[day - 10]] == 0) current.erase(discount[day - 10]);
        if (day >= 9 && current == needed) ++answer;
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 담는 string
// #include <unordered_map>  // 키로 값을 찾는 해시 맵
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(vector<string> want, vector<int> number, vector<string> discount) {  // 열흘 창에서 원하는 상품 수량이 모두 맞는지 확인
// unordered_map<string, int> needed, current;  // 원하는 수량과 현재 열흘 할인 수량 저장
// for (int i = 0; i < (int)want.size(); ++i) needed[want[i]] = number[i];  // 상품 이름을 필요한 수량과 연결
// int answer = 0;  // 조건을 만족하는 시작일 수 초기화
// for (int day = 0; day < (int)discount.size(); ++day) {  // 할인 상품을 하루씩 창에 추가
// ++current[discount[day]];  // 현재 날짜의 상품 수 늘리기
// if (day >= 10 && --current[discount[day - 10]] == 0) current.erase(discount[day - 10]);  // 열흘 창 밖으로 나간 상품 제거
// if (day >= 9 && current == needed) ++answer;  // 열흘 수량이 원하는 수량과 정확히 같으면 세기
// }  // 블록 끝
// return answer;  // 가능한 회원 등록 시작일 수 반환
// }  // 블록 끝

// 풀이 요약
// 열흘 길이의 할인 창을 하루씩 이동하며 상품별 수량이 원하는 수량과 일치하는 시작일 세기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:36:31
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level2/042_131127_%ED%95%A0%EC%9D%B8_%ED%96%89%EC%82%AC/README.md)
