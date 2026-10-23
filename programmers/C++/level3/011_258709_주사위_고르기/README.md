# 주사위 고르기

[레벨 3 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/258709) · Level 3 · C++

## 풀이

주사위 절반의 모든 조합에서 양쪽 주사위 합 분포를 만들고 정렬한 상대 합을 이분 탐색해 승리 수 비교

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <algorithm>
#include <functional>
#include <numeric>
#include <vector>
using namespace std;

vector<int> solution(vector<vector<int>> dice) {
    int n = (int)dice.size(); vector<int> selected, answer; long long best = -1;
    auto distribution = [&](const vector<int>& indices) {
        vector<int> sums{0};
        for (int index : indices) {
            vector<int> next; next.reserve(sums.size() * 6);
            for (int total : sums) for (int face : dice[index]) next.push_back(total + face);
            sums = move(next);
        }
        return sums;
    };
    function<void(int)> choose = [&](int start) {
        if ((int)selected.size() == n / 2) {
            vector<int> other;
            for (int i = 0; i < n; ++i) if (!binary_search(selected.begin(), selected.end(), i)) other.push_back(i);
            vector<int> left = distribution(selected), right = distribution(other);
            sort(right.begin(), right.end());
            long long wins = 0;
            for (int value : left) wins += lower_bound(right.begin(), right.end(), value) - right.begin();
            if (wins > best) { best = wins; answer = selected; }
            return;
        }
        for (int i = start; i <= n - (n / 2 - (int)selected.size()); ++i) { selected.push_back(i); choose(i + 1); selected.pop_back(); }
    };
    choose(0);
    for (int& index : answer) ++index;
    return answer;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <functional>  // 재귀 람다를 담는 function과 함수 객체
// #include <numeric>  // 누적합·최대공약수 같은 수치 알고리즘
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// vector<int> solution(vector<vector<int>> dice) {  // 절반의 주사위를 골라 승리 횟수 최대화
// int n = (int)dice.size(); vector<int> selected, answer; long long best = -1;  // 선택 주사위와 최선 승리 수 초기화
// auto distribution = [&](const vector<int>& indices) {  // 선택한 주사위의 모든 합을 중복을 유지해 생성
// vector<int> sums{0};  // 빈 선택의 합 0에서 시작
// for (int index : indices) {  // 주사위를 하나씩 추가
// vector<int> next; next.reserve(sums.size() * 6);  // 새 합을 저장할 공간을 확보
// for (int total : sums) for (int face : dice[index]) next.push_back(total + face);  // 모든 기존 합과 여섯 면을 조합
// sums = move(next);  // 새 분포를 다음 단계에 사용
// }  // 블록 끝
// return sums;  // 각 경우의 합 목록 반환
// };  // 블록 끝
// function<void(int)> choose = [&](int start) {  // 절반의 주사위 조합을 오름차순으로 생성
// if ((int)selected.size() == n / 2) {  // A의 주사위를 모두 선택하면 승리 수 계산
// vector<int> other;  // B가 가져갈 나머지 주사위 저장
// for (int i = 0; i < n; ++i) if (!binary_search(selected.begin(), selected.end(), i)) other.push_back(i);  // 선택되지 않은 주사위 모으기
// vector<int> left = distribution(selected), right = distribution(other);  // 양쪽의 모든 합을 생성
// sort(right.begin(), right.end());  // B의 합을 이분 탐색할 수 있게 정렬
// long long wins = 0;  // A의 승리 경우 수 누적
// for (int value : left) wins += lower_bound(right.begin(), right.end(), value) - right.begin();  // 각 A의 합보다 작은 B의 합 수를 더하기
// if (wins > best) { best = wins; answer = selected; }  // 더 많이 이기는 조합 선택
// return;  // 완성한 조합의 탐색을 끝
// }  // 블록 끝
// for (int i = start; i <= n - (n / 2 - (int)selected.size()); ++i) { selected.push_back(i); choose(i + 1); selected.pop_back(); }  // 필요한 수를 채울 수 있는 주사위만 이어 고르기
// };  // 블록 끝
// choose(0);  // 첫 주사위부터 절반 조합 탐색
// for (int& index : answer) ++index;  // 주사위 번호를 1부터 시작하도록 바꾸기
// return answer;  // 가장 유리한 주사위 번호 반환
// }  // 블록 끝

// 풀이 요약
// 주사위 절반의 모든 조합에서 양쪽 주사위 합 분포를 만들고 정렬한 상대 합을 이분 탐색해 승리 수 비교
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:46:17
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level3/011_258709_%EC%A3%BC%EC%82%AC%EC%9C%84_%EA%B3%A0%EB%A5%B4%EA%B8%B0/README.md)
