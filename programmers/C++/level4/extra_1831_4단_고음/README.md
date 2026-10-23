# 4단 고음

[레벨 4 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/1831) · Level 4 · C++

## 풀이

최종 두 번의 덧셈을 먼저 되돌린 뒤 역순 탐색. 남은 값과 짝이 안 맞은 덧셈 수를 상태로 메모하고 필요한 3의 거듭제곱보다 작으면 가지치기.

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

int solution(int n) {
    vector<long long> powers(1, 1); while (powers.back() <= n) powers.push_back(powers.back() * 3);
    unordered_map<long long, int> cache;
    function<int(long long, int)> search = [&](long long value, int pending) {
        if (value < 3) return 0;
        if (value == 3) return pending == 2 ? 1 : 0;
        int required = (pending + 1) / 2; if (required >= (int)powers.size() || value < powers[required]) return 0;
        long long key = value * 128 + pending; auto found = cache.find(key); if (found != cache.end()) return found->second;
        int answer = search(value - 1, pending + 1);
        if (pending >= 2 && value % 3 == 0) answer += search(value / 3, pending - 2);
        return cache[key] = answer;
    };
    return search((long long)n - 2, 2);
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
// int solution(int n) {  // 4단 고음 풀이 함수 정의
//     vector<long long> powers(1, 1); while (powers.back() <= n) powers.push_back(powers.back() * 3);  // 가지치기에 사용할 3의 거듭제곱 표를 n보다 큰 값까지 준비
//     unordered_map<long long, int> cache;  // 남은 값과 미처리 덧셈 수 상태별 경우의 수를 저장할 캐시 준비
//     function<int(long long, int)> search = [&](long long value, int pending) {  // 남은 값 value와 앞으로 3배 연산에 짝지을 덧셈 수 pending을 받는 재귀 람다
//         if (value < 3) return 0;  // 3보다 작아지면 올바른 시작 형태가 아니므로 0
//         if (value == 3) return pending == 2 ? 1 : 0;  // 3에 도달했을 때 덧셈 두 개가 맞물리는 상태만 성공 1로 처리
//         int required = (pending + 1) / 2; if (required >= (int)powers.size() || value < powers[required]) return 0;  // 남은 덧셈에 필요한 최소 3배 횟수를 계산하고, 값이 필요한 3의 거듭제곱보다 작으면 중단
//         long long key = value * 128 + pending; auto found = cache.find(key); if (found != cache.end()) return found->second;  // 두 상태를 정수 키로 묶고 이미 계산한 경우의 수면 캐시 반환
//         int answer = search(value - 1, pending + 1);  // 끝의 +1을 되돌려 값은 1 줄이고 미처리 덧셈 수는 1 늘려 탐색
//         if (pending >= 2 && value % 3 == 0) answer += search(value / 3, pending - 2);  // 덧셈 두 개가 있고 3으로 나누어떨어지면 3배 연산도 되돌려 경우의 수 추가
//         return cache[key] = answer;  // value·pending 조합의 경우의 수를 캐시에 저장하면서 반환
//     };  // 블록 끝
//     return search((long long)n - 2, 2);  // 마지막 +1 두 번을 미리 되돌린 상태에서 역순 탐색 시작
// }  // 함수 끝
//

// 풀이 요약
// 최종 두 번의 덧셈을 먼저 되돌린 뒤 역순 탐색. 남은 값과 짝이 안 맞은 덧셈 수를 상태로 메모하고 필요한 3의 거듭제곱보다 작으면 가지치기.
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:51:55
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level4/extra_1831_4%EB%8B%A8_%EA%B3%A0%EC%9D%8C/README.md)
