# 홀짝에 따라 다른 값 반환하기

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181935) · Level 0 · C++

## 풀이

n이 홀수이면 홀수의 합을, 짝수이면 짝수 제곱의 합을 구하기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
int solution(int n) {
    int answer = 0;
    for (int i = n % 2 ? 1 : 2; i <= n; i += 2) answer += n % 2 ? i : i * i;
    return answer;
}

// 전체 코드 줄별 설명
// int solution(int n) {  // 홀짝에 따라 다른 값 반환하기 풀이 시작
//     int answer = 0;  // int형 합계를 0으로 초기화
//     for (int i = n % 2 ? 1 : 2; i <= n; i += 2) answer += n % 2 ? i : i * i;  // for에서 홀짝에 맞는 시작값부터 2씩 증가시키고 삼항 연산자로 원소 또는 제곱을 더하기
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// n이 홀수이면 홀수의 합을, 짝수이면 짝수 제곱의 합을 구하기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:34:17
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_181935_%ED%99%80%EC%A7%9D%EC%97%90_%EB%94%B0%EB%9D%BC_%EB%8B%A4%EB%A5%B8_%EA%B0%92_%EB%B0%98%ED%99%98%ED%95%98%EA%B8%B0/README.md)
