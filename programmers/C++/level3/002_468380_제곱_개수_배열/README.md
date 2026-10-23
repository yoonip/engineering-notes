# 제곱 개수 배열

[레벨 3 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/468380) · Level 3 · C++

## 풀이

반복 배열의 누적 길이와 합을 구한 뒤 창의 양 끝 구간이 바뀌는 경계 사이에서 합이 등차수열로 변하는 성질로 같은 합의 시작점 세기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <algorithm>
#include <vector>
using namespace std;

vector<long long> solution(vector<int> arr, long long l, long long r) {
    int n = (int)arr.size();
    vector<long long> lengths(n + 1, 0), sums(n + 1, 0);
    for (int i = 0; i < n; ++i) { lengths[i + 1] = lengths[i] + arr[i]; sums[i + 1] = sums[i] + 1LL * arr[i] * arr[i]; }
    auto prefix = [&](long long count) {
        int index = min(n - 1, int(upper_bound(lengths.begin(), lengths.end(), count) - lengths.begin()) - 1);
        return sums[index] + (count - lengths[index]) * arr[index];
    };
    long long target = prefix(r) - prefix(l - 1), window = r - l + 1;
    long long last_start = lengths.back() - window, current = prefix(window), start = 0, answer = 0;
    int left = 0, right = int(upper_bound(lengths.begin(), lengths.end(), window) - lengths.begin()) - 1;
    while (start < last_start) {
        long long span = min({lengths[left + 1] - start, lengths[right + 1] - start - window, last_start - start});
        long long slope = 1LL * arr[right] - arr[left];
        if (slope == 0) { if (current == target) answer += span; }
        else {
            long long difference = target - current;
            if (difference % slope == 0 && difference / slope >= 0 && difference / slope < span) ++answer;
        }
        current += slope * span; start += span;
        if (start == lengths[left + 1]) ++left;
        if (start + window == lengths[right + 1]) ++right;
    }
    answer += current == target;
    return {target, answer};
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// vector<long long> solution(vector<int> arr, long long l, long long r) {  // 지정 구간과 합이 같은 이동 창의 개수 세기
// int n = (int)arr.size();  // 원본 배열의 길이 구하기
// vector<long long> lengths(n + 1, 0), sums(n + 1, 0);  // 반복 배열의 누적 길이와 누적 합 저장
// for (int i = 0; i < n; ++i) { lengths[i + 1] = lengths[i] + arr[i]; sums[i + 1] = sums[i] + 1LL * arr[i] * arr[i]; }  // 값 a가 a번 반복되는 구간의 길이와 합을 더하기
// auto prefix = [&](long long count) {  // 반복 배열의 앞 count개 합 구하기
// int index = min(n - 1, int(upper_bound(lengths.begin(), lengths.end(), count) - lengths.begin()) - 1);  // 마지막으로 걸친 원본 구간을 이분 탐색
// return sums[index] + (count - lengths[index]) * arr[index];  // 완전한 구간 합과 마지막 부분 구간 합을 더하기
// };  // 블록 끝
// long long target = prefix(r) - prefix(l - 1), window = r - l + 1;  // 목표 구간의 합과 길이 구하기
// long long last_start = lengths.back() - window, current = prefix(window), start = 0, answer = 0;  // 이동 창의 마지막 시작점과 첫 합 초기화
// int left = 0, right = int(upper_bound(lengths.begin(), lengths.end(), window) - lengths.begin()) - 1;  // 창의 양 끝이 걸친 원본 구간 찾기
// while (start < last_start) {  // 마지막 창 직전까지 같은 변화율인 구간을 한 번에 처리
// long long span = min({lengths[left + 1] - start, lengths[right + 1] - start - window, last_start - start});  // 양 끝 중 먼저 구간 경계에 닿을 때까지의 이동량 구하기
// long long slope = 1LL * arr[right] - arr[left];  // 창을 한 칸 옮길 때 합의 변화량 구하기
// if (slope == 0) { if (current == target) answer += span; }  // 합이 일정하고 목표와 같으면 모든 시작점 세기
// else {  // 합이 등차수열로 바뀌는 구간
// long long difference = target - current;  // 현재 합에서 목표까지 필요한 변화량 구하기
// if (difference % slope == 0 && difference / slope >= 0 && difference / slope < span) ++answer;  // 구간 안의 정수 이동 위치에서 목표가 되는지 검사
// }  // 블록 끝
// current += slope * span; start += span;  // 현재 합과 시작 위치를 다음 경계로 옮기기
// if (start == lengths[left + 1]) ++left;  // 왼쪽 끝의 원본 구간 경계를 넘겼는지 반영
// if (start + window == lengths[right + 1]) ++right;  // 오른쪽 끝의 원본 구간 경계를 넘겼는지 반영
// }  // 블록 끝
// answer += current == target;  // 마지막 시작점의 창도 따로 세기
// return {target, answer};  // 목표 합과 같은 합을 만드는 구간 수 반환
// }  // 블록 끝

// 풀이 요약
// 반복 배열의 누적 길이와 합을 구한 뒤 창의 양 끝 구간이 바뀌는 경계 사이에서 합이 등차수열로 변하는 성질로 같은 합의 시작점 세기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:41:43
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level3/002_468380_%EC%A0%9C%EA%B3%B1_%EA%B0%9C%EC%88%98_%EB%B0%B0%EC%97%B4/README.md)
