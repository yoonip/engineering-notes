# 수식 최대화

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/67257) · Level 2 · C++

## 풀이

수식의 숫자와 연산자를 분리하고 여섯 가지 우선순위마다 높은 연산부터 계산해 최종 절댓값의 최댓값 구하기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <algorithm>
#include <cstdlib>
#include <string>
#include <vector>
using namespace std;

long long solution(string expression) {
    vector<long long> original; vector<char> original_ops;
    long long value = 0;
    for (char c : expression) {
        if (c >= '0' && c <= '9') value = value * 10 + c - '0';
        else { original.push_back(value); original_ops.push_back(c); value = 0; }
    }
    original.push_back(value);
    string order = "*+-"; long long answer = 0;
    do {
        vector<long long> numbers = original; vector<char> ops = original_ops;
        for (char operation : order) {
            for (int i = 0; i < (int)ops.size();) {
                if (ops[i] != operation) { ++i; continue; }
                long long result = operation == '+' ? numbers[i] + numbers[i + 1] : operation == '-' ? numbers[i] - numbers[i + 1] : numbers[i] * numbers[i + 1];
                numbers[i] = result; numbers.erase(numbers.begin() + i + 1); ops.erase(ops.begin() + i);
            }
        }
        answer = max(answer, llabs(numbers[0]));
    } while (next_permutation(order.begin(), order.end()));
    return answer;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <cstdlib>  // 정수 절댓값 같은 기본 유틸리티
// #include <string>  // 문자열을 담는 string
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// long long solution(string expression) {  // 연산자 우선순위를 바꿔 결과 절댓값 최대화
// vector<long long> original; vector<char> original_ops;  // 원래 피연산자와 연산자를 분리해 저장
// long long value = 0;  // 현재 숫자 토큰 누적
// for (char c : expression) {  // 수식의 각 문자 읽기
// if (c >= '0' && c <= '9') value = value * 10 + c - '0';  // 연속한 숫자를 하나의 정수로 만들기
// else { original.push_back(value); original_ops.push_back(c); value = 0; }  // 연산자를 만나면 숫자와 연산자를 각각 저장
// }  // 블록 끝
// original.push_back(value);  // 마지막 숫자도 저장
// string order = "*+-"; long long answer = 0;  // 사전순 첫 우선순위와 최대 절댓값 초기화
// do {  // 연산자 우선순위의 여섯 순열 검사
// vector<long long> numbers = original; vector<char> ops = original_ops;  // 현재 우선순위에서 사용할 수식을 복사
// for (char operation : order) {  // 높은 우선순위부터 계산
// for (int i = 0; i < (int)ops.size();) {  // 현재 종류의 연산자를 왼쪽부터 찾기
// if (ops[i] != operation) { ++i; continue; }  // 다른 연산자이면 다음 위치로 이동
// long long result = operation == '+' ? numbers[i] + numbers[i + 1] : operation == '-' ? numbers[i] - numbers[i + 1] : numbers[i] * numbers[i + 1];  // 연산자 종류에 맞게 인접한 두 값 계산
// numbers[i] = result; numbers.erase(numbers.begin() + i + 1); ops.erase(ops.begin() + i);  // 세 토큰을 계산 결과 하나로 바꾸기
// }  // 블록 끝
// }  // 블록 끝
// answer = max(answer, llabs(numbers[0]));  // 최종 값의 절댓값으로 최댓값 갱신
// } while (next_permutation(order.begin(), order.end()));  // 다음 연산자 우선순위를 생성
// return answer;  // 가능한 최대 절댓값 반환
// }  // 블록 끝

// 풀이 요약
// 수식의 숫자와 연산자를 분리하고 여섯 가지 우선순위마다 높은 연산부터 계산해 최종 절댓값의 최댓값 구하기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:16:03
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level2/062_67257_%EC%88%98%EC%8B%9D_%EC%B5%9C%EB%8C%80%ED%99%94/README.md)
