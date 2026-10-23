# 테이블 해시 함수

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/147354) · Level 2 · C++

## 풀이

지정 열과 첫 열의 정렬 규칙을 적용한 뒤 각 행의 나머지 합을 XOR로 누적

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <algorithm>
#include <vector>
using namespace std;

int solution(vector<vector<int>> data, int col, int row_begin, int row_end) {
    sort(data.begin(), data.end(), [&](const auto& a, const auto& b) { return a[col - 1] != b[col - 1] ? a[col - 1] < b[col - 1] : a[0] > b[0]; });
    int answer = 0;
    for (int row = row_begin; row <= row_end; ++row) {
        int value = 0;
        for (int number : data[row - 1]) value += number % row;
        answer ^= value;
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(vector<vector<int>> data, int col, int row_begin, int row_end) {  // 정렬한 행의 나머지 합을 XOR로 결합
// sort(data.begin(), data.end(), [&](const auto& a, const auto& b) { return a[col - 1] != b[col - 1] ? a[col - 1] < b[col - 1] : a[0] > b[0]; });  // 지정 열은 오름차순, 동률이면 첫 열은 내림차순으로 정렬
// int answer = 0;  // XOR 누적값의 시작값을 0으로 두기
// for (int row = row_begin; row <= row_end; ++row) {  // 1부터 시작하는 지정 행 범위를 순회
// int value = 0;  // 현재 행의 나머지 합 초기화
// for (int number : data[row - 1]) value += number % row;  // 실제 배열 인덱스로 바꾸고 각 값을 행 번호로 나눈 나머지를 더하기
// answer ^= value;  // 복합 XOR 대입 연산자로 행의 값 누적
// }  // 블록 끝
// return answer;  // 테이블 해시 값 반환
// }  // 블록 끝

// 풀이 요약
// 지정 열과 첫 열의 정렬 규칙을 적용한 뒤 각 행의 나머지 합을 XOR로 누적
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:33:43
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level2/032_147354_%ED%85%8C%EC%9D%B4%EB%B8%94_%ED%95%B4%EC%8B%9C_%ED%95%A8%EC%88%98/README.md)
