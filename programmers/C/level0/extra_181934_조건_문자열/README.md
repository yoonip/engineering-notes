# 조건 문자열

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181934) · Level 0 · C

## 풀이

같은 값일 때 등호 허용 여부를 확인하고, 다른 값은 부등호 방향에 맞게 비교

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
int solution(const char* ineq, const char* eq, int n, int m) {
    if (n == m) return eq[0] == '=';
    return ineq[0] == '>' ? n > m : n < m;
}

// 전체 코드 줄별 설명
// int solution(const char* ineq, const char* eq, int n, int m) {  // 조건 문자열 풀이 시작
//     if (n == m) return eq[0] == '=';  // if로 두 수가 같은지 검사하고 eq의 첫 문자가 등호인지 반환
//     return ineq[0] == '>' ? n > m : n < m;  // 삼항 연산자 ?:로 부등호 방향에 맞는 대소 비교 결과를 반환
// }  // 블록 끝

// 풀이 요약
// 같은 값일 때 등호 허용 여부를 확인하고, 다른 값은 부등호 방향에 맞게 비교
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:30:35
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_181934_%EC%A1%B0%EA%B1%B4_%EB%AC%B8%EC%9E%90%EC%97%B4/README.md)
