# 연속 펄스 부분 수열의 합

[레벨 3 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/161988) · Level 3 · C++

## 풀이

한 가지 교대 부호를 적용한 누적합의 최댓값과 최솟값 차이로 두 시작 부호를 모두 포함한 최대 부분합 구하기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <algorithm>
#include <vector>
using namespace std;

long long solution(vector<int> sequence) {
    long long prefix = 0, lowest = 0, highest = 0;
    for (int i = 0; i < (int)sequence.size(); ++i) {
        prefix += i % 2 == 0 ? sequence[i] : -1LL * sequence[i];
        lowest = min(lowest, prefix); highest = max(highest, prefix);
    }
    return highest - lowest;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// long long solution(vector<int> sequence) {  // 교대 부호 누적합으로 최대 펄스 부분합 계산
// long long prefix = 0, lowest = 0, highest = 0;  // 교대 부호 누적합의 현재 값과 최저 및 최고 저장
// for (int i = 0; i < (int)sequence.size(); ++i) {  // 수열의 각 위치에 고정된 교대 부호 적용
// prefix += i % 2 == 0 ? sequence[i] : -1LL * sequence[i];  // 짝수 위치는 더하고 홀수 위치는 빼기
// lowest = min(lowest, prefix); highest = max(highest, prefix);  // 누적합의 두 경계 갱신
// }  // 블록 끝
// return highest - lowest;  // 두 펄스 시작 부호를 모두 포함하는 최대 부분합 반환
// }  // 블록 끝

// 풀이 요약
// 한 가지 교대 부호를 적용한 누적합의 최댓값과 최솟값 차이로 두 시작 부호를 모두 포함한 최대 부분합 구하기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:48:20
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level3/018_161988_%EC%97%B0%EC%86%8D_%ED%8E%84%EC%8A%A4_%EB%B6%80%EB%B6%84_%EC%88%98%EC%97%B4%EC%9D%98_%ED%95%A9/README.md)
