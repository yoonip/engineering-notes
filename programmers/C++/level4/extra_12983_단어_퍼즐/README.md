# 단어 퍼즐

[레벨 4 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/12983) · Level 4 · C++

## 풀이

목표 문자열의 앞 end글자를 만드는 최소 조각 수를 DP. 존재하는 조각 길이만 검사하고 마지막 조각이 맞으면 앞 구간 답 + 1로 갱신.

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

int solution(vector<string> strs, string t) {
    unordered_set<string> pieces(strs.begin(), strs.end()); vector<int> lengths; for (const string& piece : pieces) lengths.push_back(piece.size());
    sort(lengths.begin(), lengths.end()); lengths.erase(unique(lengths.begin(), lengths.end()), lengths.end());
    int n = (int)t.size(); vector<int> dp(n + 1, n + 1); dp[0] = 0;
    for (int end = 1; end <= n; ++end) for (int length : lengths) {
        if (length > end) break;
        int start = end - length; if (pieces.count(t.substr(start, length))) dp[end] = min(dp[end], dp[start] + 1);
    }
    return dp[n] <= n ? dp[n] : -1;
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
// int solution(vector<string> strs, string t) {  // 단어 퍼즐 풀이 함수 정의
//     unordered_set<string> pieces(strs.begin(), strs.end()); vector<int> lengths; for (const string& piece : pieces) lengths.push_back(piece.size());  // 단어 조각을 집합으로 중복 제거하고 사용할 조각 길이들을 수집
//     sort(lengths.begin(), lengths.end()); lengths.erase(unique(lengths.begin(), lengths.end()), lengths.end());  // 길이를 정렬하고 중복 제거해 같은 길이의 검사를 한 번만 수행
//     int n = (int)t.size(); vector<int> dp(n + 1, n + 1); dp[0] = 0;  // 목표 길이 n과 불가능 표시 n + 1로 DP 초기화. 빈 문자열은 조각 0개
//     for (int end = 1; end <= n; ++end) for (int length : lengths) {  // 목표 접두사 끝 end와 마지막 조각 길이를 순서대로 검사
//         if (length > end) break;  // 조각이 접두사보다 길면 더 긴 조각도 불가능하므로 중단
//         int start = end - length; if (pieces.count(t.substr(start, length))) dp[end] = min(dp[end], dp[start] + 1);  // 끝부분이 조각 집합에 있으면 그 앞 접두사의 최소 개수 + 1과 비교해 갱신
//     }  // 블록 끝
//     return dp[n] <= n ? dp[n] : -1;  // 목표 전체를 만들 수 있으면 최소 개수, 없으면 -1 반환
// }  // 함수 끝
//

// 풀이 요약
// 목표 문자열의 앞 end글자를 만드는 최소 조각 수를 DP. 존재하는 조각 길이만 검사하고 마지막 조각이 맞으면 앞 구간 답 + 1로 갱신.
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:50:49
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level4/extra_12983_%EB%8B%A8%EC%96%B4_%ED%8D%BC%EC%A6%90/README.md)
