# 배열 만들기 6

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181859) · Level 0 · C++

## 풀이

새 값과 마지막 값이 같으면 마지막 값을 제거하고, 다르면 추가. 각 입력을 한 번씩 처리

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <string>
#include <vector>
#include <algorithm>
#include <numeric>
#include <functional>
#include <unordered_set>
#include <sstream>
#include <cctype>
#include <cstdlib>
using namespace std;

vector<int> solution(vector<int> arr) {
    vector<int> answer;
    for (int value : arr) {
        if (!answer.empty() && answer.back() == value) answer.pop_back();
        else answer.push_back(value);
    }
    if (answer.empty()) answer.push_back(-1);
    return answer;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 다룰 string
// #include <vector>  // 길이를 늘릴 수 있는 vector
// #include <algorithm>  // 정렬·검색·뒤집기 알고리즘
// #include <numeric>  // accumulate·iota 등 수치 연산
// #include <functional>  // greater·multiplies 등 함수 객체
// #include <unordered_set>  // 중복을 거를 해시 집합
// #include <sstream>  // 문자열을 항목별로 읽을 스트림
// #include <cctype>  // 문자 검사와 대소문자 변환
// #include <cstdlib>  // 정수 변환과 절댓값 등 표준 함수
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// vector<int> solution(vector<int> arr) {  // 배열 만들기 6 풀이 시작
//     vector<int> answer;  // 같은 이웃 값을 취소하며 남길 스택
//     for (int value : arr) {  // 입력 순서대로 새 값을 스택 끝과 비교
//         if (!answer.empty() && answer.back() == value) answer.pop_back();  // 끝 값이 새 값과 같으면 둘을 상쇄해 끝 원소 삭제
//         else answer.push_back(value);  // 비었거나 끝 값과 다르면 새 값 추가
//     }  // 블록 끝
//     if (answer.empty()) answer.push_back(-1);  // if로 조건을 검사하고 push_back으로 해당 원소를 결과 뒤에 추가
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 새 값과 마지막 값이 같으면 마지막 값을 제거하고, 다르면 추가. 각 입력을 한 번씩 처리
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:15:34
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181859_%EB%B0%B0%EC%97%B4_%EB%A7%8C%EB%93%A4%EA%B8%B0_6/README.md)
