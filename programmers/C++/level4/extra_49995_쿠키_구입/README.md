# 쿠키 구입

[레벨 4 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/49995) · Level 4 · C++

## 풀이

두 아들의 구간 사이 경계를 하나씩 고정. 양쪽 합 중 작은 쪽을 바깥으로 늘려 같아지는 합의 최댓값을 찾음.

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <string>
#include <vector>
#include <array>
#include <algorithm>
#include <numeric>
#include <functional>
#include <unordered_set>
#include <unordered_map>
#include <map>
#include <set>
#include <queue>
#include <deque>
#include <tuple>
#include <utility>
#include <climits>
#include <cstdlib>
using namespace std;

int solution(vector<int> cookie) {
    int n = (int)cookie.size(), answer = 0;
    for (int middle = 0; middle < n - 1; ++middle) {
        int left = middle, right = middle + 1, a = cookie[left], b = cookie[right];
        while (true) {
            if (a == b) answer = max(answer, a);
            if (a <= b) { if (left == 0) break; a += cookie[--left]; }
            else { if (right == n - 1) break; b += cookie[++right]; }
        }
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열 string 사용 준비
// #include <vector>  // 가변 길이 배열 vector 사용 준비
// #include <array>  // 고정 크기 배열 array 사용 준비
// #include <algorithm>  // 정렬·탐색·최솟값 등 표준 알고리즘 사용 준비
// #include <numeric>  // gcd·accumulate 등 수치 알고리즘 사용 준비
// #include <functional>  // 함수 래퍼와 greater 등 비교 함수 객체 사용 준비
// #include <unordered_set>  // 중복 없는 원소를 저장하는 해시 집합 사용 준비
// #include <unordered_map>  // 키로 값을 찾는 해시 맵 사용 준비
// #include <map>  // 키 순서가 유지되는 맵 사용 준비
// #include <set>  // 중복 제거와 정렬을 함께 하는 집합 사용 준비
// #include <queue>  // FIFO 큐와 우선순위 큐 사용 준비
// #include <deque>  // 양 끝 삽입·삭제를 지원하는 덱 사용 준비
// #include <tuple>  // 여러 상태 값을 묶는 tuple 사용 준비
// #include <utility>  // pair·move 등 유틸리티 사용 준비
// #include <climits>  // 정수 범위 상수 사용 준비
// #include <cstdlib>  // 정수 절댓값 등 표준 유틸리티 함수 사용 준비
// using namespace std;  // 표준 이름의 std:: 접두사 생략
//
// int solution(vector<int> cookie) {  // 쿠키 구입 풀이 함수 정의
//     int n = (int)cookie.size(), answer = 0;  // 쿠키 묶음 수 n과 한 아들에게 줄 최대 합 answer 저장
//     for (int middle = 0; middle < n - 1; ++middle) {  // 두 연속 구간을 나누는 모든 경계 middle 검사
//         int left = middle, right = middle + 1, a = cookie[left], b = cookie[right];  // 경계 양옆에서 시작해 왼쪽·오른쪽 합 a·b 준비
//         while (true) {  // 한쪽 구간을 더 늘릴 수 없을 때까지 비교
//             if (a == b) answer = max(answer, a);  // 양쪽 합이 같으면 한 아들이 받는 쿠키 수의 최댓값 갱신
//             if (a <= b) { if (left == 0) break; a += cookie[--left]; }  // 왼쪽 합이 작거나 같으면 왼쪽으로 확장. 더 갈 수 없으면 종료
//             else { if (right == n - 1) break; b += cookie[++right]; }  // 오른쪽 합이 작으면 오른쪽으로 확장. 더 갈 수 없으면 종료
//         }  // 블록 끝
//     }  // 블록 끝
//     return answer;  // 두 아들이 똑같이 받을 수 있는 최대 쿠키 수 반환
// }  // 함수 끝
//

// 풀이 요약
// 두 아들의 구간 사이 경계를 하나씩 고정. 양쪽 합 중 작은 쪽을 바깥으로 늘려 같아지는 합의 최댓값을 찾음.
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:47:48
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level4/extra_49995_%EC%BF%A0%ED%82%A4_%EA%B5%AC%EC%9E%85/README.md)
