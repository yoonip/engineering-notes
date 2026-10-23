# [3차] 자동완성

[레벨 4 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/17685) · Level 4 · C++

## 풀이

단어를 정렬하면 접두사를 가장 많이 공유하는 단어가 이웃에 있음. 인접 단어의 공통 접두사 + 1을 필요한 입력 길이에 반영하고 자기 길이로 제한.

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

int solution(vector<string> words) {
    sort(words.begin(), words.end()); vector<int> needed(words.size(), 1);
    for (int i = 0; i + 1 < (int)words.size(); ++i) {
        int common = 0; while (common < (int)min(words[i].size(), words[i + 1].size()) && words[i][common] == words[i + 1][common]) ++common;
        needed[i] = max(needed[i], common + 1); needed[i + 1] = max(needed[i + 1], common + 1);
    }
    int answer = 0; for (int i = 0; i < (int)words.size(); ++i) answer += min((int)words[i].size(), needed[i]);
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
// int solution(vector<string> words) {  // [3차] 자동완성 풀이 함수 정의
//     sort(words.begin(), words.end()); vector<int> needed(words.size(), 1);  // 단어를 사전순 정렬하고 각 단어의 필요 입력 길이를 1로 시작
//     for (int i = 0; i + 1 < (int)words.size(); ++i) {  // 사전순으로 붙어 있는 단어 쌍 검사
//         int common = 0; while (common < (int)min(words[i].size(), words[i + 1].size()) && words[i][common] == words[i + 1][common]) ++common;  // 둘 중 짧은 길이 안에서 같은 문자가 이어지는 공통 접두사 길이 계산
//         needed[i] = max(needed[i], common + 1); needed[i + 1] = max(needed[i + 1], common + 1);  // 두 단어 모두 구분하려면 공통 접두사보다 한 글자 더 필요하므로 최대 필요 길이 갱신
//     }  // 블록 끝
//     int answer = 0; for (int i = 0; i < (int)words.size(); ++i) answer += min((int)words[i].size(), needed[i]);  // 필요 길이를 단어 자체 길이 이하로 제한해 전체 입력 수 합산
//     return answer;  // 모든 단어를 찾는 데 필요한 입력 수 합 반환
// }  // 함수 끝
//

// 풀이 요약
// 단어를 정렬하면 접두사를 가장 많이 공유하는 단어가 이웃에 있음. 인접 단어의 공통 접두사 + 1을 필요한 입력 길이에 반영하고 자기 길이로 제한.
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:49:55
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level4/extra_17685_%5B3%EC%B0%A8%5D_%EC%9E%90%EB%8F%99%EC%99%84%EC%84%B1/README.md)
