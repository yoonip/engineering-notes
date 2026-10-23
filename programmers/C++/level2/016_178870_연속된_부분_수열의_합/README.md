# 연속된 부분 수열의 합

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/178870) · Level 2 · C++

## 풀이

양의 원소로 이루어진 수열에서 오른쪽 끝을 늘리고 합이 크면 왼쪽 끝을 줄이며 합이 k인 최단 구간 찾기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <vector>
using namespace std;

vector<int> solution(vector<int> sequence, int k) {
    int left = 0;
    long long total = 0;
    vector<int> answer{0, (int)sequence.size()};
    for (int right = 0; right < (int)sequence.size(); ++right) {
        total += sequence[right];
        while (total > k) total -= sequence[left++];
        if (total == k && right - left < answer[1] - answer[0]) answer = {left, right};
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// vector<int> solution(vector<int> sequence, int k) {  // 합이 k인 구간 중 가장 짧고 앞선 구간 찾기
// int left = 0;  // 현재 부분 수열의 왼쪽 끝 초기화
// long long total = 0;  // 현재 구간의 합 초기화
// vector<int> answer{0, (int)sequence.size()};  // 아직 찾지 않은 구간의 길이를 전체보다 크게 두기
// for (int right = 0; right < (int)sequence.size(); ++right) {  // 오른쪽 끝을 한 칸씩 늘리기
// total += sequence[right];  // 새 원소를 구간 합에 더하기
// while (total > k) total -= sequence[left++];  // 합이 크면 왼쪽 원소를 제거해 구간 줄이기
// if (total == k && right - left < answer[1] - answer[0]) answer = {left, right};  // 합이 같고 더 짧은 구간만 갱신
// }  // 블록 끝
// return answer;  // 길이가 가장 짧고 시작 위치가 가장 이른 구간 반환
// }  // 블록 끝

// 풀이 요약
// 양의 원소로 이루어진 수열에서 오른쪽 끝을 늘리고 합이 크면 왼쪽 끝을 줄이며 합이 k인 최단 구간 찾기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:28:25
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level2/016_178870_%EC%97%B0%EC%86%8D%EB%90%9C_%EB%B6%80%EB%B6%84_%EC%88%98%EC%97%B4%EC%9D%98_%ED%95%A9/README.md)
