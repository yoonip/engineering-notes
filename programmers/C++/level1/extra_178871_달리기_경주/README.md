# 달리기 경주

[레벨 1 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/178871) · Level 1 · C++

## 풀이

선수 배열과 이름별 현재 위치를 함께 관리. 호명될 때 앞 선수와 교환하고 두 사람의 위치도 갱신.

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

vector<string> solution(vector<string> players, vector<string> callings) {
    unordered_map<string, int> position;
    for (int i = 0; i < (int)players.size(); ++i) position[players[i]] = i;
    for (const string& name : callings) {
        int i = position[name];
        string front = players[i - 1];
        swap(players[i - 1], players[i]);
        position[name] = i - 1; position[front] = i;
    }
    return players;
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
// vector<string> solution(vector<string> players, vector<string> callings) {  // 달리기 경주 풀이 함수 정의
//     unordered_map<string, int> position;  // 이름으로 현재 순위를 바로 찾을 해시 맵 준비
//     for (int i = 0; i < (int)players.size(); ++i) position[players[i]] = i;  // 초기 선수 배열의 인덱스를 이름별 위치로 기록
//     for (const string& name : callings) {  // 호명된 이름을 순서대로 처리
//         int i = position[name];  // 호명된 선수의 현재 위치 i 조회
//         string front = players[i - 1];  // 바로 앞에 있는 선수 이름을 저장
//         swap(players[i - 1], players[i]);  // 배열에서 앞 선수와 호명된 선수의 위치 교환
//         position[name] = i - 1; position[front] = i;  // 교환된 두 선수의 위치를 해시 맵에도 반영
//     }  // 블록 끝
//     return players;  // 모든 추월을 반영한 최종 선수 순서 반환
// }  // 함수 끝
//

// 풀이 요약
// 선수 배열과 이름별 현재 위치를 함께 관리. 호명될 때 앞 선수와 교환하고 두 사람의 위치도 갱신.
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:05:32
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level1/extra_178871_%EB%8B%AC%EB%A6%AC%EA%B8%B0_%EA%B2%BD%EC%A3%BC/README.md)
