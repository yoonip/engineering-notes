# 카펫

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/42842) · Level 2 · C++

## 풀이

전체 넓이의 약수 쌍을 가로와 세로 후보로 두고 테두리를 뺀 내부 넓이가 노란 칸 수와 일치하는지 검사

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <vector>
using namespace std;

vector<int> solution(int brown, int yellow) {
    int area = brown + yellow;
    for (int height = 3; height <= area / height; ++height) {
        if (area % height != 0) continue;
        int width = area / height;
        if ((width - 2) * (height - 2) == yellow) return {width, height};
    }
    return {};
}

// 전체 코드 줄별 설명
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// vector<int> solution(int brown, int yellow) {  // 넓이의 약수 쌍 중 갈색 테두리 조건 찾기
// int area = brown + yellow;  // 전체 카펫의 넓이 구하기
// for (int height = 3; height <= area / height; ++height) {  // 가로보다 크지 않은 세로 길이 검사
// if (area % height != 0) continue;  // 넓이를 나눌 수 없는 길이는 제외
// int width = area / height;  // 짝이 되는 가로 길이 구하기
// if ((width - 2) * (height - 2) == yellow) return {width, height};  // 테두리를 뺀 내부가 노란 칸 수와 같으면 반환
// }  // 블록 끝
// return {};  // 유효한 입력에서는 도달하지 않는 기본 반환
// }  // 블록 끝

// 풀이 요약
// 전체 넓이의 약수 쌍을 가로와 세로 후보로 두고 테두리를 뺀 내부 넓이가 노란 칸 수와 일치하는지 검사
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:22:31
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level2/075_42842_%EC%B9%B4%ED%8E%AB/README.md)
