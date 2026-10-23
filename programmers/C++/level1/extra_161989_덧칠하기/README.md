# 덧칠하기

[레벨 1 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/161989) · Level 1 · C++

## 풀이

왼쪽부터 아직 칠하지 않은 구역을 만나면 롤러를 한 번 사용. 그 롤러가 덮는 오른쪽 끝을 기록해 중복 작업 생략.

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

int solution(int n, int m, vector<int> section) {
    int answer = 0, painted_until = 0;
    for (int position : section) if (position > painted_until) { ++answer; painted_until = min(position, n - m + 1) + m - 1; }
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
// int solution(int n, int m, vector<int> section) {  // 덧칠하기 풀이 함수 정의
//     int answer = 0, painted_until = 0;  // 롤러 사용 수 answer와 칠한 오른쪽 끝 painted_until을 0으로 시작
//     for (int position : section) if (position > painted_until) { ++answer; painted_until = min(position, n - m + 1) + m - 1; }  // 칠할 위치가 기존 범위 밖이면 롤러 횟수 증가. 벽을 넘지 않는 시작점을 잡아 새 오른쪽 끝 계산
//     return answer;  // 필요한 롤러 사용 횟수 반환
// }  // 함수 끝
//

// 풀이 요약
// 왼쪽부터 아직 칠하지 않은 구역을 만나면 롤러를 한 번 사용. 그 롤러가 덮는 오른쪽 끝을 기록해 중복 작업 생략.
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:06:36
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level1/extra_161989_%EB%8D%A7%EC%B9%A0%ED%95%98%EA%B8%B0/README.md)
