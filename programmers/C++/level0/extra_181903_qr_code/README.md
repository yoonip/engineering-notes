# qr code

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181903) · Level 0 · C++

## 풀이

인덱스를 q로 나눈 나머지가 r인 위치의 문자만 연결

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <string>
using namespace std;

string solution(int q, int r, string code) {
    string answer;
    for (size_t i = r; i < code.size(); i += q) answer += code[i];
    return answer;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 다룰 string
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// string solution(int q, int r, string code) {  // qr code 풀이 시작
//     string answer;  // 인덱스를 q로 나눈 나머지가 r인 문자
//     for (size_t i = r; i < code.size(); i += q) answer += code[i];  // for에서 r부터 q칸씩 이동하며 조건에 맞는 문자를 +=로 연결
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 인덱스를 q로 나눈 나머지가 r인 위치의 문자만 연결
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:59:26
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_181903_qr_code/README.md)
