# 하샤드 수

[레벨 1 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/12947) · Level 1 · C++

## 풀이

10으로 나눈 나머지로 자릿수를 더한 뒤, 원래 수가 자릿수 합으로 나누어떨어지는지 확인.

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

bool solution(int x) {
    int sum = 0;
    for (int n = x; n; n /= 10) sum += n % 10;
    return x % sum == 0;
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
// bool solution(int x) {  // 하샤드 수 풀이 함수 정의
//     int sum = 0;  // 자릿수 합 sum을 0으로 시작
//     for (int n = x; n; n /= 10) sum += n % 10;  // x의 복사본 n에서 끝자리를 더하고 10으로 나눠 다음 자리 이동
//     return x % sum == 0;  // 원래 x를 자릿수 합으로 나눈 나머지가 0인지 반환
// }  // 함수 끝
//

// 풀이 요약
// 10으로 나눈 나머지로 자릿수를 더한 뒤, 원래 수가 자릿수 합으로 나누어떨어지는지 확인.
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:19:58
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level1/extra_12947_%ED%95%98%EC%83%A4%EB%93%9C_%EC%88%98/README.md)
