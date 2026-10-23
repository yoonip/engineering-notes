# 수 조작하기 1

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181926) · Level 0 · C

## 풀이

조작 문자마다 정해진 증감량을 현재 수에 적용

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
int solution(int n, const char* control) {
    for (; *control; ++control) {
        if (*control == 'w') ++n;
        else if (*control == 's') --n;
        else if (*control == 'd') n += 10;
        else if (*control == 'a') n -= 10;
    }
    return n;
}

// 전체 코드 줄별 설명
// int solution(int n, const char* control) {  // 수 조작하기 1 풀이 시작
//     for (; *control; ++control) {  // 포인터가 가리키는 문자가 널 문자가 아닐 동안 for로 순회하며 포인터를 이동
//         if (*control == 'w') ++n;  // if와 ==로 w 명령을 검사하고 ++로 현재 수에 1을 더하기
//         else if (*control == 's') --n;  // else if로 s 명령을 검사하고 --로 현재 수에서 1을 빼기
//         else if (*control == 'd') n += 10;  // else if로 d 명령을 검사하고 +=로 현재 수에 10을 더하기
//         else if (*control == 'a') n -= 10;  // else if로 a 명령을 검사하고 -=로 현재 수에서 10을 빼기
//     }  // 블록 끝
//     return n;  // return으로 조작을 모두 적용한 정수를 반환
// }  // 블록 끝

// 풀이 요약
// 조작 문자마다 정해진 증감량을 현재 수에 적용
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:41:15
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181926_%EC%88%98_%EC%A1%B0%EC%9E%91%ED%95%98%EA%B8%B0_1/README.md)
