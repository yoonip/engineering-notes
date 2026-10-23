# 신규 아이디 추천

[레벨 1 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/72410) · Level 1 · C++

## 풀이

소문자 변환과 허용 문자 선택을 하면서 선두·연속 마침표를 제거. 마지막 마침표, 빈 문자열, 최대·최소 길이를 순서대로 처리.

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <string>
#include <vector>
#include <algorithm>
#include <numeric>
#include <functional>
#include <unordered_set>
#include <unordered_map>
#include <sstream>
#include <cctype>
#include <cstdlib>
#include <cstdio>
#include <cmath>
#include <queue>
#include <set>
#include <climits>
#include <iostream>
using namespace std;

string solution(string new_id) {
    string answer;
    for (unsigned char raw : new_id) {
        char c = tolower(raw);
        if (isalnum((unsigned char)c) || c == '-' || c == '_' || c == '.') {
            if (c == '.' && (answer.empty() || answer.back() == '.')) continue;
            answer += c;
        }
    }
    if (!answer.empty() && answer.back() == '.') answer.pop_back();
    if (answer.empty()) answer = "a";
    if (answer.size() > 15) answer.resize(15);
    if (answer.back() == '.') answer.pop_back();
    while (answer.size() < 3) answer += answer.back();
    return answer;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열 string 사용 준비
// #include <vector>  // 가변 길이 배열 vector 사용 준비
// #include <algorithm>  // 정렬·탐색·최솟값 등 표준 알고리즘 사용 준비
// #include <numeric>  // gcd·accumulate 등 수치 알고리즘 사용 준비
// #include <functional>  // 함수 래퍼와 greater 등 비교 함수 객체 사용 준비
// #include <unordered_set>  // 중복 없는 원소를 저장하는 해시 집합 사용 준비
// #include <unordered_map>  // 키로 값을 찾는 해시 맵 사용 준비
// #include <sstream>  // 문자열을 토큰으로 나눠 읽을 스트림 사용 준비
// #include <cctype>  // 숫자·대소문자 검사와 변환 함수 사용 준비
// #include <cstdlib>  // 정수 절댓값 등 표준 유틸리티 함수 사용 준비
// #include <cstdio>  // snprintf 등 형식 있는 입출력 함수 사용 준비
// #include <cmath>  // 제곱근 등 수학 함수 사용 준비
// #include <queue>  // FIFO 큐와 우선순위 큐 사용 준비
// #include <set>  // 중복 제거와 정렬을 함께 하는 집합 사용 준비
// #include <climits>  // 정수 범위 상수 사용 준비
// #include <iostream>  // cin·cout 표준 입출력 사용 준비
// using namespace std;  // 표준 이름의 std:: 접두사 생략
//
// string solution(string new_id) {  // 신규 아이디 추천 풀이 함수 정의
//     string answer;  // 정제한 아이디를 쌓을 빈 문자열 준비
//     for (unsigned char raw : new_id) {  // 문자 분류 함수에 안전하게 넘기도록 unsigned char로 입력 문자 순회
//         char c = tolower(raw);  // 현재 문자를 소문자로 변환
//         if (isalnum((unsigned char)c) || c == '-' || c == '_' || c == '.') {  // 영숫자 또는 허용 특수문자 -, _, .만 처리
//             if (c == '.' && (answer.empty() || answer.back() == '.')) continue;  // 마침표가 맨 앞이거나 직전에도 마침표가 있으면 건너뜀
//             answer += c;  // 조건을 통과한 문자를 결과에 추가
//         }  // 블록 끝
//     }  // 블록 끝
//     if (!answer.empty() && answer.back() == '.') answer.pop_back();  // 마지막 마침표가 있으면 제거
//     if (answer.empty()) answer = "a";  // 아무 문자도 남지 않으면 기본 문자 a 사용
//     if (answer.size() > 15) answer.resize(15);  // 15글자를 넘으면 앞 15글자만 유지
//     if (answer.back() == '.') answer.pop_back();  // 길이 제한으로 끝에 남은 마침표 제거
//     while (answer.size() < 3) answer += answer.back();  // 3글자 미만이면 마지막 문자를 반복해 길이 채움
//     return answer;  // 모든 규칙을 적용한 추천 아이디 반환
// }  // 함수 끝
//

// 풀이 요약
// 소문자 변환과 허용 문자 선택을 하면서 선두·연속 마침표를 제거. 마지막 마침표, 빈 문자열, 최대·최소 길이를 순서대로 처리.
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:14:46
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level1/extra_72410_%EC%8B%A0%EA%B7%9C_%EC%95%84%EC%9D%B4%EB%94%94_%EC%B6%94%EC%B2%9C/README.md)
