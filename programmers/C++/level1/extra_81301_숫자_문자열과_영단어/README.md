# 숫자 문자열과 영단어

[레벨 1 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/81301) · Level 1 · C++

## 풀이

현재 위치가 숫자면 바로 한 자리 추가. 영단어면 0~9 표와 대조해 해당 숫자를 추가하고 단어 길이만큼 건너뜀.

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

int solution(string s) {
    vector<string> words = {"zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"};
    int answer = 0;
    for (size_t i = 0; i < s.size(); ) {
        if (isdigit((unsigned char)s[i])) answer = answer * 10 + s[i++] - '0';
        else for (int d = 0; d < 10; ++d) if (s.compare(i, words[d].size(), words[d]) == 0) { answer = answer * 10 + d; i += words[d].size(); break; }
    }
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
// int solution(string s) {  // 숫자 문자열과 영단어 풀이 함수 정의
//     vector<string> words = {"zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"};  // 0부터 9까지의 영단어를 숫자 인덱스 순서로 저장
//     int answer = 0;  // 변환한 정숫값 answer를 0으로 시작
//     for (size_t i = 0; i < s.size(); ) {  // 현재 읽기 위치 i가 문자열 끝에 도달할 때까지 반복
//         if (isdigit((unsigned char)s[i])) answer = answer * 10 + s[i++] - '0';  // 숫자 문자이면 이전 값 × 10에 새 자릿수를 더하고 한 글자 이동
//         else for (int d = 0; d < 10; ++d) if (s.compare(i, words[d].size(), words[d]) == 0) { answer = answer * 10 + d; i += words[d].size(); break; }  // 영단어이면 일치하는 단어를 찾아 숫자를 추가하고 그 단어 길이만큼 위치 이동
//     }  // 블록 끝
//     return answer;  // 숫자와 영단어를 모두 처리한 정숫값 반환
// }  // 함수 끝
//

// 풀이 요약
// 현재 위치가 숫자면 바로 한 자리 추가. 영단어면 0~9 표와 대조해 해당 숫자를 추가하고 단어 길이만큼 건너뜀.
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:13:54
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level1/extra_81301_%EC%88%AB%EC%9E%90_%EB%AC%B8%EC%9E%90%EC%97%B4%EA%B3%BC_%EC%98%81%EB%8B%A8%EC%96%B4/README.md)
