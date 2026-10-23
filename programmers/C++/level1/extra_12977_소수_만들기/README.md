# 소수 만들기

[레벨 1 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/12977) · Level 1 · C++

## 풀이

i < j < k인 세 수의 합을 검사. 합의 제곱근 이하에서 약수를 찾지 못하면 소수 조합으로 셈.

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

int solution(vector<int> nums) {
    int answer = 0, n = (int)nums.size();
    for (int i = 0; i < n; ++i) for (int j = i + 1; j < n; ++j) for (int k = j + 1; k < n; ++k) {
        int sum = nums[i] + nums[j] + nums[k]; bool prime = true;
        for (int divisor = 2; divisor * divisor <= sum; ++divisor) if (sum % divisor == 0) { prime = false; break; }
        if (prime) ++answer;
    }
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
// int solution(vector<int> nums) {  // 소수 만들기 풀이 함수 정의
//     int answer = 0, n = (int)nums.size();  // 소수가 되는 조합 수 answer와 원소 수 n 저장
//     for (int i = 0; i < n; ++i) for (int j = i + 1; j < n; ++j) for (int k = j + 1; k < n; ++k) {  // 중복 없이 증가하는 세 인덱스 조합 선택
//         int sum = nums[i] + nums[j] + nums[k]; bool prime = true;  // 선택한 세 수의 합 sum을 구하고 소수라고 가정
//         for (int divisor = 2; divisor * divisor <= sum; ++divisor) if (sum % divisor == 0) { prime = false; break; }  // 2부터 제곱근 이하의 약수가 하나라도 있으면 소수가 아니므로 검사 중단
//         if (prime) ++answer;  // 약수가 발견되지 않은 조합만 하나 셈
//     }  // 블록 끝
//     return answer;  // 합이 소수인 세 수 조합의 개수 반환
// }  // 함수 끝
//

// 풀이 요약
// i < j < k인 세 수의 합을 검사. 합의 제곱근 이하에서 약수를 찾지 못하면 소수 조합으로 셈.
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:18:39
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level1/extra_12977_%EC%86%8C%EC%88%98_%EB%A7%8C%EB%93%A4%EA%B8%B0/README.md)
