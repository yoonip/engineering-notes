# 수열과 구간 쿼리 2

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181923) · Level 0 · C++

## 풀이

각 구간에서 k보다 큰 값 중 최솟값을 찾고, 없으면 -1을 기록

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <vector>
using namespace std;

vector<int> solution(vector<int> arr, vector<vector<int>> queries) {
    vector<int> answer;
    for (const auto& query : queries) {
        int best = -1;
        for (int i = query[0]; i <= query[1]; ++i) {
            if (arr[i] > query[2] && (best == -1 || arr[i] < best)) best = arr[i];
        }
        answer.push_back(best);
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <vector>  // 길이를 늘릴 수 있는 vector
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// vector<int> solution(vector<int> arr, vector<vector<int>> queries) {  // 수열과 구간 쿼리 2 풀이 시작
//     vector<int> answer;  // 쿼리마다 구한 최솟값 또는 -1
//     for (const auto& query : queries) {  // 범위 for와 const auto 참조로 각 쿼리를 복사 없이 읽기
//         int best = -1;  // 조건을 만족하는 값이 없음을 나타내는 -1로 최솟값 후보를 초기화
//         for (int i = query[0]; i <= query[1]; ++i) {  // for에서 <=를 사용해 쿼리의 시작 인덱스부터 끝 인덱스까지 포함해 검사
//             if (arr[i] > query[2] && (best == -1 || arr[i] < best)) best = arr[i];  // &&와 ||로 기준보다 크고 기존 후보보다 작은 값을 골라 최솟값 후보를 갱신
//         }  // 블록 끝
//         answer.push_back(best);  // push_back으로 현재 쿼리의 결과를 vector 끝에 추가
//     }  // 블록 끝
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 각 구간에서 k보다 큰 값 중 최솟값을 찾고, 없으면 -1을 기록
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:42:51
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181923_%EC%88%98%EC%97%B4%EA%B3%BC_%EA%B5%AC%EA%B0%84_%EC%BF%BC%EB%A6%AC_2/README.md)
