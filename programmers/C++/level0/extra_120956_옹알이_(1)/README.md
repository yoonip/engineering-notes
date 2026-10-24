# 옹알이 (1)

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120956) · Level 0 · C++

## 풀이

앞에서부터 허용 발음을 맞추며 읽은 길이만큼 이동. 사용한 발음은 비트로 기록해 중복 사용을 막고, 단어 끝까지 도달한 경우만 세기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <string>
#include <vector>
#include <algorithm>
#include <numeric>
#include <cmath>
#include <sstream>
#include <climits>
#include <cctype>
#include <iostream>
#include <functional>

using namespace std;

int solution(vector<string> babbling) {
    vector<string> sounds = {"aya", "ye", "woo", "ma"};
    int answer = 0;
    for (const string& word : babbling) {
        size_t pos = 0;
        unsigned used = 0;
        while (pos < word.size()) {
            bool matched = false;
            for (int j = 0; j < 4; ++j)
                if (!(used & (1u << j)) && word.compare(pos, sounds[j].size(), sounds[j]) == 0) {
                    pos += sounds[j].size(); used |= 1u << j; matched = true; break;
                }
            if (!matched) break;
        }
        answer += pos == word.size();
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 다룰 string
// #include <vector>  // 길이를 늘릴 수 있는 vector
// #include <algorithm>  // 정렬·검색·뒤집기 알고리즘
// #include <numeric>  // accumulate·iota 등 수치 연산
// #include <cmath>  // 제곱근 등 수학 함수
// #include <sstream>  // 문자열을 항목별로 읽을 스트림
// #include <climits>  // INT_MIN·INT_MAX 등 정수 범위 상수
// #include <cctype>  // 문자 검사와 대소문자 변환
// #include <iostream>  // cin·cout 표준 입출력
// #include <functional>  // greater·multiplies 등 함수 객체
//
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// int solution(vector<string> babbling) {  // 옹알이 (1) 풀이 시작
//     vector<string> sounds = {"aya", "ye", "woo", "ma"};  // 각 단어에서 한 번씩만 사용할 수 있는 네 발음 목록
//     int answer = 0;  // 허용 발음으로 끝까지 읽을 수 있는 단어 수
//     for (const string& word : babbling) {  // 옹알이 단어를 하나씩 판정
//         size_t pos = 0;  // 현재 단어에서 아직 읽지 않은 시작 위치
//         unsigned used = 0;  // 이미 사용한 네 발음을 비트로 기록
//         while (pos < word.size()) {  // 단어 끝에 닿거나 발음을 못 찾을 때까지 진행
//             bool matched = false;  // 이번 위치에서 허용 발음을 찾았는지 표시
//             for (int j = 0; j < 4; ++j)  // 다음 부분이 허용된 네 발음 중 무엇인지 확인
//                 if (!(used & (1u << j)) && word.compare(pos, sounds[j].size(), sounds[j]) == 0) {  // 아직 쓰지 않은 발음이 현재 위치와 일치할 때만 선택
//                     pos += sounds[j].size(); used |= 1u << j; matched = true; break;  // 읽은 길이만큼 이동하고 사용 표시·매칭 성공을 기록한 뒤 후보 탐색 종료
//                 }  // 블록 끝
//             if (!matched) break;  // 일치한 발음이 없으면 남은 부분을 읽을 수 없으니 이번 단어 판정 중단
//         }  // 블록 끝
//         answer += pos == word.size();  // 단어를 남김없이 읽었을 때만 정답 수 추가
//     }  // 블록 끝
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 앞에서부터 허용 발음을 맞추며 읽은 길이만큼 이동. 사용한 발음은 비트로 기록해 중복 사용을 막고, 단어 끝까지 도달한 경우만 세기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:30:08
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_120956_%EC%98%B9%EC%95%8C%EC%9D%B4_%281%29/README.md)
