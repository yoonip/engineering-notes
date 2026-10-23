# [1차] 캐시

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/17680) · Level 2 · C++

## 풀이

도시 이름을 소문자로 통일하고 사용한 도시를 가장 최근 위치로 옮기며 캐시 적중과 실패 비용을 더하기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <algorithm>
#include <cctype>
#include <list>
#include <string>
#include <vector>
using namespace std;

int solution(int cacheSize, vector<string> cities) {
    list<string> cache; int time = 0;
    for (string city : cities) {
        for (char& c : city) c = (char)tolower((unsigned char)c);
        auto found = find(cache.begin(), cache.end(), city);
        if (found != cache.end()) { time += 1; cache.erase(found); }
        else time += 5;
        if (cacheSize > 0) {
            cache.push_back(city);
            if ((int)cache.size() > cacheSize) cache.pop_front();
        }
    }
    return time;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <cctype>  // 문자 분류와 대소문자 변환
// #include <list>  // 원소를 연결하고 옮길 수 있는 list
// #include <string>  // 문자열을 담는 string
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(int cacheSize, vector<string> cities) {  // 대소문자 구분 없이 LRU 캐시 갱신
// list<string> cache; int time = 0;  // 최근 사용 순서의 캐시와 총 실행 시간 초기화
// for (string city : cities) {  // 도시 이름을 요청 순서대로 처리
// for (char& c : city) c = (char)tolower((unsigned char)c);  // 도시 이름의 대소문자를 통일
// auto found = find(cache.begin(), cache.end(), city);  // 현재 도시가 캐시에 있는지 찾기
// if (found != cache.end()) { time += 1; cache.erase(found); }  // 캐시 적중이면 비용 1을 더하고 기존 위치 지우기
// else time += 5;  // 캐시 실패이면 비용 5를 더하기
// if (cacheSize > 0) {  // 캐시 용량이 있을 때만 도시 저장
// cache.push_back(city);  // 현재 도시를 가장 최근 위치에 두기
// if ((int)cache.size() > cacheSize) cache.pop_front();  // 용량을 넘으면 가장 오래 사용하지 않은 도시 빼기
// }  // 블록 끝
// }  // 블록 끝
// return time;  // LRU 규칙의 총 실행 시간 반환
// }  // 블록 끝

// 풀이 요약
// 도시 이름을 소문자로 통일하고 사용한 도시를 가장 최근 위치로 옮기며 캐시 적중과 실패 비용을 더하기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:29:36
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level2/090_17680_%EC%BA%90%EC%8B%9C/README.md)
