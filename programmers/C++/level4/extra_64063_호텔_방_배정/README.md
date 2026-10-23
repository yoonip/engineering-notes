# 호텔 방 배정

[레벨 4 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/64063) · Level 4 · C++

## 풀이

사용된 방은 다음 후보를 가리키도록 연결. 빈 방을 찾는 동안 지나간 방들을 최종 빈 방 다음 위치로 압축해 재탐색을 줄임.

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

vector<long long> solution(long long k, vector<long long> room_number) {
    unordered_map<long long, long long> next; next.reserve(room_number.size() * 2);
    vector<long long> answer;
    for (long long wanted : room_number) {
        long long room = wanted; vector<long long> trail;
        while (next.count(room)) { trail.push_back(room); room = next[room]; }
        answer.push_back(room); next[room] = room + 1;
        for (long long previous : trail) next[previous] = room + 1;
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
// vector<long long> solution(long long k, vector<long long> room_number) {  // 호텔 방 배정 풀이 함수 정의
//     unordered_map<long long, long long> next; next.reserve(room_number.size() * 2);  // 사용한 방에서 다음 후보 방으로 이어지는 해시 맵 준비
//     vector<long long> answer;  // 손님 순서대로 배정한 방을 담을 배열 준비
//     for (long long wanted : room_number) {  // 각 손님의 희망 방부터 배정 탐색
//         long long room = wanted; vector<long long> trail;  // 후보 room과 지나간 방 목록 trail 준비
//         while (next.count(room)) { trail.push_back(room); room = next[room]; }  // 이미 배정된 방이면 경로에 기록하고 다음 후보 연결을 따라 이동
//         answer.push_back(room); next[room] = room + 1;  // 찾은 빈 방을 배정하고 그 방의 다음 후보를 room + 1로 연결
//         for (long long previous : trail) next[previous] = room + 1;  // 지나온 모든 방도 새 빈 방 다음 위치로 연결해 경로 압축
//     }  // 블록 끝
//     return answer;  // 요청 순서의 배정 방 번호 반환
// }  // 함수 끝
//

// 풀이 요약
// 사용된 방은 다음 후보를 가리키도록 연결. 빈 방을 찾는 동안 지나간 방들을 최종 빈 방 다음 위치로 압축해 재탐색을 줄임.
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:46:34
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level4/extra_64063_%ED%98%B8%ED%85%94_%EB%B0%A9_%EB%B0%B0%EC%A0%95/README.md)
