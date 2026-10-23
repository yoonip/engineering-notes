# 예산

[레벨 1 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/12982) · Level 1 · C++

## 풀이

요청 금액이 작은 부서부터 지원. 남은 예산으로 다음 금액을 낼 수 없으면 종료.

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

int solution(vector<int> d, int budget) {
    sort(d.begin(), d.end());
    int answer = 0;
    for (int cost : d) { if (cost > budget) break; budget -= cost; ++answer; }
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
// int solution(vector<int> d, int budget) {  // 예산 풀이 함수 정의
//     sort(d.begin(), d.end());  // 적은 금액부터 지원하도록 오름차순 정렬
//     int answer = 0;  // 지원한 부서 수 answer를 0으로 시작
//     for (int cost : d) { if (cost > budget) break; budget -= cost; ++answer; }  // 예산을 넘는 금액이면 중단하고, 지불 가능하면 예산 차감 후 부서 수 증가
//     return answer;  // 예산 안에서 지원한 최대 부서 수 반환
// }  // 함수 끝
//

// 풀이 요약
// 요청 금액이 작은 부서부터 지원. 남은 예산으로 다음 금액을 낼 수 없으면 종료.
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:18:21
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level1/extra_12982_%EC%98%88%EC%82%B0/README.md)
