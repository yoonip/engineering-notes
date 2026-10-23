# 콜라츠 수열 만들기

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181919) · Level 0 · C++

## 풀이

시작값을 저장하고 짝수이면 절반, 홀수이면 3배에 1을 더하며 1까지 기록

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <vector>
using namespace std;

vector<int> solution(int n) {
    vector<int> answer{n};
    while (n != 1) {
        n = n % 2 == 0 ? n / 2 : 3 * n + 1;
        answer.push_back(n);
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <vector>  // 길이를 늘릴 수 있는 vector
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// vector<int> solution(int n) {  // 콜라츠 수열 만들기 풀이 시작
//     vector<int> answer{n};  // 중괄호 초기화로 시작값 n을 첫 원소로 저장
//     while (n != 1) {  // while과 !=로 현재 값이 1이 아닐 동안 다음 수열 값을 계산
//         n = n % 2 == 0 ? n / 2 : 3 * n + 1;  // 삼항 연산자 ?:로 짝수이면 절반, 홀수이면 3배에 1을 더한 값으로 바꾸기
//         answer.push_back(n);  // push_back으로 다음 콜라츠 수열 값을 vector 끝에 추가
//     }  // 블록 끝
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 시작값을 저장하고 짝수이면 절반, 홀수이면 3배에 1을 더하며 1까지 기록
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:45:07
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_181919_%EC%BD%9C%EB%9D%BC%EC%B8%A0_%EC%88%98%EC%97%B4_%EB%A7%8C%EB%93%A4%EA%B8%B0/README.md)
