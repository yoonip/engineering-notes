# 정수를 나선형으로 배치하기

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181832) · Level 0 · C++

## 풀이

현재 방향으로 채우다가 벽이나 이미 채운 칸을 만나면 시계방향으로 회전

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <string>
#include <vector>
#include <algorithm>
#include <numeric>
#include <functional>
#include <unordered_set>
#include <sstream>
#include <cctype>
#include <cstdlib>
using namespace std;

vector<vector<int>> solution(int n) {
    vector<vector<int>> answer(n, vector<int>(n, 0));
    int dr[4] = {0, 1, 0, -1}, dc[4] = {1, 0, -1, 0};
    int row = 0, col = 0, direction = 0;
    for (int value = 1; value <= n * n; ++value) {
        answer[row][col] = value;
        if (value == n * n) break;
        int nr = row + dr[direction], nc = col + dc[direction];
        if (nr < 0 || nr >= n || nc < 0 || nc >= n || answer[nr][nc]) direction = (direction + 1) % 4;
        row += dr[direction]; col += dc[direction];
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 다룰 string
// #include <vector>  // 길이를 늘릴 수 있는 vector
// #include <algorithm>  // 정렬·검색·뒤집기 알고리즘
// #include <numeric>  // accumulate·iota 등 수치 연산
// #include <functional>  // greater·multiplies 등 함수 객체
// #include <unordered_set>  // 중복을 거를 해시 집합
// #include <sstream>  // 문자열을 항목별로 읽을 스트림
// #include <cctype>  // 문자 검사와 대소문자 변환
// #include <cstdlib>  // 정수 변환과 절댓값 등 표준 함수
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// vector<vector<int>> solution(int n) {  // 정수를 나선형으로 배치하기 풀이 시작
//     vector<vector<int>> answer(n, vector<int>(n, 0));  // 아직 채우지 않은 칸을 0으로 표시한 n×n 격자
//     int dr[4] = {0, 1, 0, -1}, dc[4] = {1, 0, -1, 0};  // 오른쪽·아래·왼쪽·위 순서의 행·열 이동량
//     int row = 0, col = 0, direction = 0;  // 왼쪽 위 칸에서 오른쪽 방향으로 출발
//     for (int value = 1; value <= n * n; ++value) {  // 1부터 n²까지 하나씩 배치
//         answer[row][col] = value;  // 현재 칸에 다음 숫자 기록
//         if (value == n * n) break;  // 마지막 숫자를 썼으면 더 이동하지 않고 종료
//         int nr = row + dr[direction], nc = col + dc[direction];  // 현재 방향으로 직진했을 때의 다음 칸
//         if (nr < 0 || nr >= n || nc < 0 || nc >= n || answer[nr][nc]) direction = (direction + 1) % 4;  // nr < 0 || nr >= n || nc < 0 || nc >= n || answer[nr][nc]이면 direction에 (direction + 1) % 4 저장
//         row += dr[direction]; col += dc[direction];  // 확정한 방향으로 한 칸 이동
//     }  // 블록 끝
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 현재 방향으로 채우다가 벽이나 이미 채운 칸을 만나면 시계방향으로 회전
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:27:56
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181832_%EC%A0%95%EC%88%98%EB%A5%BC_%EB%82%98%EC%84%A0%ED%98%95%EC%9C%BC%EB%A1%9C_%EB%B0%B0%EC%B9%98%ED%95%98%EA%B8%B0/README.md)
