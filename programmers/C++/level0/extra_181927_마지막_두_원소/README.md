# 마지막 두 원소

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181927) · Level 0 · C++

## 풀이

마지막 값이 직전 값보다 크면 차이를, 아니면 마지막 값의 두 배를 추가

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <vector>
using namespace std;

vector<int> solution(vector<int> num_list) {
    int last = num_list.back(), previous = num_list[num_list.size() - 2];
    num_list.push_back(last > previous ? last - previous : last * 2);
    return num_list;
}

// 전체 코드 줄별 설명
// #include <vector>  // 길이를 늘릴 수 있는 vector
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// vector<int> solution(vector<int> num_list) {  // 마지막 두 원소 풀이 시작
//     int last = num_list.back(), previous = num_list[num_list.size() - 2];  // back과 []로 마지막 원소와 직전 원소를 각각 저장
//     num_list.push_back(last > previous ? last - previous : last * 2);  // 삼항 연산자로 추가할 값을 고르고 push_back으로 배열 끝에 넣기
//     return num_list;  // return으로 새 원소를 추가한 배열을 반환
// }  // 블록 끝

// 풀이 요약
// 마지막 값이 직전 값보다 크면 차이를, 아니면 마지막 값의 두 배를 추가
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:40:17
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_181927_%EB%A7%88%EC%A7%80%EB%A7%89_%EB%91%90_%EC%9B%90%EC%86%8C/README.md)
