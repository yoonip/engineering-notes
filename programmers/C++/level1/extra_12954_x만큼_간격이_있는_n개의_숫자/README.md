# x만큼 간격이 있는 n개의 숫자

[레벨 1 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/12954) · Level 1 · C++

## 풀이

x부터 x × n까지의 배수를 차례로 추가. 곱셈 시작부터 long long을 사용해 큰 결과도 저장.

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

vector<long long> solution(int x, int n) {
    vector<long long> answer;
    for (int i = 1; i <= n; ++i) answer.push_back(1LL * x * i);
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
// vector<long long> solution(int x, int n) {  // x만큼 간격이 있는 n개의 숫자 풀이 함수 정의
//     vector<long long> answer;  // x의 배수들을 저장할 long long 배열 준비
//     for (int i = 1; i <= n; ++i) answer.push_back(1LL * x * i);  // 1부터 n까지 곱하며 1LL로 정수 곱을 long long으로 계산해 결과에 추가
//     return answer;  // x 간격의 n개 수를 순서대로 반환
// }  // 함수 끝
//

// 풀이 요약
// x부터 x × n까지의 배수를 차례로 추가. 곱셈 시작부터 long long을 사용해 큰 결과도 저장.
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:19:11
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level1/extra_12954_x%EB%A7%8C%ED%81%BC_%EA%B0%84%EA%B2%A9%EC%9D%B4_%EC%9E%88%EB%8A%94_n%EA%B0%9C%EC%9D%98_%EC%88%AB%EC%9E%90/README.md)
