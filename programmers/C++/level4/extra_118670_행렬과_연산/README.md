# 행렬과 연산

[레벨 4 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/118670) · Level 4 · C++

## 풀이

왼쪽 열·오른쪽 열·가운데 행들을 각각 deque로 분리. ShiftRow는 행 덱 회전, Rotate는 테두리 네 부분 사이의 앞뒤 원소 이동으로 처리.

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

vector<vector<int>> solution(vector<vector<int>> rc, vector<string> operations) {
    int rows = (int)rc.size(), cols = (int)rc[0].size();
    deque<int> left, right; deque<deque<int>> middle;
    for (const auto& row : rc) { left.push_back(row.front()); right.push_back(row.back()); middle.emplace_back(row.begin() + 1, row.end() - 1); }
    for (const string& operation : operations) {
        if (operation == "ShiftRow") {
            left.push_front(left.back()); left.pop_back(); right.push_front(right.back()); right.pop_back();
            middle.push_front(move(middle.back())); middle.pop_back();
        } else {
            middle.front().push_front(left.front()); left.pop_front();
            right.push_front(middle.front().back()); middle.front().pop_back();
            middle.back().push_back(right.back()); right.pop_back();
            left.push_back(middle.back().front()); middle.back().pop_front();
        }
    }
    vector<vector<int>> answer(rows, vector<int>(cols));
    for (int r = 0; r < rows; ++r) { answer[r][0] = left[r]; answer[r][cols - 1] = right[r]; for (int c = 1; c < cols - 1; ++c) answer[r][c] = middle[r][c - 1]; }
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
// vector<vector<int>> solution(vector<vector<int>> rc, vector<string> operations) {  // 행렬과 연산 풀이 함수 정의
//     int rows = (int)rc.size(), cols = (int)rc[0].size();  // 원래 행렬의 행 수 rows와 열 수 cols 저장
//     deque<int> left, right; deque<deque<int>> middle;  // 양 끝 열은 정수 deque, 가운데 부분은 행별 deque로 분리
//     for (const auto& row : rc) { left.push_back(row.front()); right.push_back(row.back()); middle.emplace_back(row.begin() + 1, row.end() - 1); }  // 각 행의 첫·끝 원소와 중간 구간을 해당 덱에 저장
//     for (const string& operation : operations) {  // 주어진 행렬 연산을 순서대로 처리
//         if (operation == "ShiftRow") {  // ShiftRow이면 마지막 행을 맨 앞으로 이동
//             left.push_front(left.back()); left.pop_back(); right.push_front(right.back()); right.pop_back();  // 양쪽 열의 마지막 원소를 앞으로 보내 행 이동 반영
//             middle.push_front(move(middle.back())); middle.pop_back();  // 가운데의 마지막 행 덱도 앞으로 이동. move로 내부 원소 복사 줄임
//         } else {  // Rotate이면 테두리 네 구간 사이 원소 이동
//             middle.front().push_front(left.front()); left.pop_front();  // 왼쪽 위 원소를 윗행 가운데의 앞에 전달
//             right.push_front(middle.front().back()); middle.front().pop_back();  // 윗행 가운데의 끝 원소를 오른쪽 열 앞에 전달
//             middle.back().push_back(right.back()); right.pop_back();  // 오른쪽 아래 원소를 아랫행 가운데의 뒤에 전달
//             left.push_back(middle.back().front()); middle.back().pop_front();  // 아랫행 가운데의 앞 원소를 왼쪽 열 뒤에 전달
//         }  // 블록 끝
//     }  // 블록 끝
//     vector<vector<int>> answer(rows, vector<int>(cols));  // 덱에서 최종 값을 꺼내 담을 결과 행렬 준비
//     for (int r = 0; r < rows; ++r) { answer[r][0] = left[r]; answer[r][cols - 1] = right[r]; for (int c = 1; c < cols - 1; ++c) answer[r][c] = middle[r][c - 1]; }  // 각 행의 양 끝 열과 가운데 부분을 원래 행렬 모양으로 복원
//     return answer;  // 모든 연산을 반영한 행렬 반환
// }  // 함수 끝
//

// 풀이 요약
// 왼쪽 열·오른쪽 열·가운데 행들을 각각 deque로 분리. ShiftRow는 행 덱 회전, Rotate는 테두리 네 부분 사이의 앞뒤 원소 이동으로 처리.
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:43:36
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level4/extra_118670_%ED%96%89%EB%A0%AC%EA%B3%BC_%EC%97%B0%EC%82%B0/README.md)
