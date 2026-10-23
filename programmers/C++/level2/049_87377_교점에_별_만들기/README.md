# 교점에 별 만들기

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/87377) · Level 2 · C++

## 풀이

직선 쌍의 교점을 정수 연산으로 구해 정수 좌표만 남기고 최소 경계 상자에 별을 표시

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <algorithm>
#include <climits>
#include <set>
#include <string>
#include <utility>
#include <vector>
using namespace std;

vector<string> solution(vector<vector<int>> line) {
    set<pair<long long, long long>> points;
    for (int i = 0; i < (int)line.size(); ++i) for (int j = i + 1; j < (int)line.size(); ++j) {
        long long a = line[i][0], b = line[i][1], e = line[i][2], c = line[j][0], d = line[j][1], f = line[j][2];
        long long denominator = a * d - b * c;
        if (denominator == 0) continue;
        long long nx = b * f - e * d, ny = e * c - a * f;
        if (nx % denominator == 0 && ny % denominator == 0) points.insert({nx / denominator, ny / denominator});
    }
    long long min_x = LLONG_MAX, max_x = LLONG_MIN, min_y = LLONG_MAX, max_y = LLONG_MIN;
    for (auto [x, y] : points) { min_x = min(min_x, x); max_x = max(max_x, x); min_y = min(min_y, y); max_y = max(max_y, y); }
    vector<string> answer((size_t)(max_y - min_y + 1), string((size_t)(max_x - min_x + 1), '.'));
    for (auto [x, y] : points) answer[(size_t)(max_y - y)][(size_t)(x - min_x)] = '*';
    return answer;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <climits>  // 정수 자료형의 최솟값·최댓값
// #include <set>  // 정렬된 집합과 중복을 허용하는 multiset
// #include <string>  // 문자열을 담는 string
// #include <utility>  // 두 값을 묶는 pair와 이동 유틸리티
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// vector<string> solution(vector<vector<int>> line) {  // 정수 교점만 모아 경계 상자 안에 별 표시
// set<pair<long long, long long>> points;  // 정수 좌표의 교점을 중복 없이 저장
// for (int i = 0; i < (int)line.size(); ++i) for (int j = i + 1; j < (int)line.size(); ++j) {  // 서로 다른 두 직선의 모든 조합 검사
// long long a = line[i][0], b = line[i][1], e = line[i][2], c = line[j][0], d = line[j][1], f = line[j][2];  // 계수를 넓은 정수형으로 옮기기
// long long denominator = a * d - b * c;  // 연립방정식의 분모 계산
// if (denominator == 0) continue;  // 평행하거나 같은 직선이면 교점 계산을 건너뛰기
// long long nx = b * f - e * d, ny = e * c - a * f;  // x좌표와 y좌표의 분자 구하기
// if (nx % denominator == 0 && ny % denominator == 0) points.insert({nx / denominator, ny / denominator});  // 두 좌표가 모두 정수인 교점만 저장
// }  // 블록 끝
// long long min_x = LLONG_MAX, max_x = LLONG_MIN, min_y = LLONG_MAX, max_y = LLONG_MIN;  // 교점을 담을 최소 경계 상자 초기화
// for (auto [x, y] : points) { min_x = min(min_x, x); max_x = max(max_x, x); min_y = min(min_y, y); max_y = max(max_y, y); }  // 모든 교점을 포함하는 좌표 경계 구하기
// vector<string> answer((size_t)(max_y - min_y + 1), string((size_t)(max_x - min_x + 1), '.'));  // 경계 상자 크기의 점 그림 만들기
// for (auto [x, y] : points) answer[(size_t)(max_y - y)][(size_t)(x - min_x)] = '*';  // 큰 y가 위로 오도록 행 좌표를 바꾸어 별을 찍기
// return answer;  // 별이 표시된 최소 크기의 문자열 그림 반환
// }  // 블록 끝

// 풀이 요약
// 직선 쌍의 교점을 정수 연산으로 구해 정수 좌표만 남기고 최소 경계 상자에 별을 표시
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:38:09
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level2/049_87377_%EA%B5%90%EC%A0%90%EC%97%90_%EB%B3%84_%EB%A7%8C%EB%93%A4%EA%B8%B0/README.md)
