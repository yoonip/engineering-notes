# 쿼드압축 후 개수 세기

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/68936) · Level 2 · C++

## 풀이

영역이 모두 같은 값이면 하나로 세고 그렇지 않으면 네 부분으로 나누어 재귀 압축

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <functional>
#include <vector>
using namespace std;

vector<int> solution(vector<vector<int>> arr) {
    vector<int> answer(2, 0);
    function<void(int, int, int)> compress = [&](int row, int column, int size) {
        int value = arr[row][column]; bool same = true;
        for (int r = row; r < row + size; ++r) for (int c = column; c < column + size; ++c) if (arr[r][c] != value) same = false;
        if (same) { ++answer[value]; return; }
        int half = size / 2;
        compress(row, column, half); compress(row, column + half, half);
        compress(row + half, column, half); compress(row + half, column + half, half);
    };
    compress(0, 0, (int)arr.size());
    return answer;
}

// 전체 코드 줄별 설명
// #include <functional>  // 재귀 람다를 담는 function과 함수 객체
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// vector<int> solution(vector<vector<int>> arr) {  // 같은 값인 구역은 압축하고 나머지는 네 조각 탐색
// vector<int> answer(2, 0);  // 압축 후 남는 0과 1 영역 수 저장
// function<void(int, int, int)> compress = [&](int row, int column, int size) {  // 정사각형의 시작점과 크기로 재귀 압축
// int value = arr[row][column]; bool same = true;  // 영역의 기준값과 균일 여부 초기화
// for (int r = row; r < row + size; ++r) for (int c = column; c < column + size; ++c) if (arr[r][c] != value) same = false;  // 영역의 모든 값이 같은지 검사
// if (same) { ++answer[value]; return; }  // 균일하면 하나의 영역으로 세고 종료
// int half = size / 2;  // 네 부분 영역의 한 변 길이 구하기
// compress(row, column, half); compress(row, column + half, half);  // 위쪽 두 영역을 압축
// compress(row + half, column, half); compress(row + half, column + half, half);  // 아래쪽 두 영역을 압축
// };  // 블록 끝
// compress(0, 0, (int)arr.size());  // 전체 정사각형부터 압축을 시작
// return answer;  // 남은 0과 1의 영역 수 반환
// }  // 블록 끝

// 풀이 요약
// 영역이 모두 같은 값이면 하나로 세고 그렇지 않으면 네 부분으로 나누어 재귀 압축
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:15:20
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level2/060_68936_%EC%BF%BC%EB%93%9C%EC%95%95%EC%B6%95_%ED%9B%84_%EA%B0%9C%EC%88%98_%EC%84%B8%EA%B8%B0/README.md)
