# x 사이의 개수

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181867) · Level 0 · C++

## 풀이

연속된 x 사이와 양 끝의 빈 조각도 길이 0으로 기록

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

vector<int> solution(string myString) {
    vector<int> answer(1, 0);
    for (char c : myString) {
        if (c == 'x') answer.push_back(0);
        else ++answer.back();
    }
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
// vector<int> solution(string myString) {  // x 사이의 개수 풀이 시작
//     vector<int> answer(1, 0);  // 첫 조각의 길이 0으로 시작하고 x를 만나면 다음 조각 추가
//     for (char c : myString) {  // x를 경계로 조각을 구분하며 문자 확인
//         if (c == 'x') answer.push_back(0);  // if로 조건을 검사하고 push_back으로 해당 원소를 결과 뒤에 추가
//         else ++answer.back();  // x가 아닌 문자는 현재 조각의 길이에 포함
//     }  // 블록 끝
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 연속된 x 사이와 양 끝의 빈 조각도 길이 0으로 기록
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:12:18
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_181867_x_%EC%82%AC%EC%9D%B4%EC%9D%98_%EA%B0%9C%EC%88%98/README.md)
