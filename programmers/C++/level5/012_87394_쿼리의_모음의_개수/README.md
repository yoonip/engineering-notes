# 쿼리의 모음의 개수 — C++

[레벨 5 목록](../README.md) · [언어별 목록](../../README.md) · [문제](https://school.programmers.co.kr/learn/courses/30/lessons/87394?language=cpp)

레벨 5 · C++

## 풀이 요약

목표를 넘지 않는 쿼리만 허용하면, 각 i가 높이 a[i]의 쿼리에 한 번 이상 덮이는 것이 최종 배열과 같아지는 조건.

구간의 최솟값 h 위치들을 나누면 높이 h 쿼리는 이 구간 안에서만 움직이고, 더 높은 쿼리는 최솟값 사이 구간들로 분리됨. 부모 높이와 h 사이 빠진 높이는 무제약 쿼리 종류로 누적.

높이 h의 필수 위치를 못 덮는 사건에 포함배제 적용. 선택한 미덮임 위치 사이 길이가 L이면 허용 부분구간 수는 L(L+1)/2라 그 쿼리들의 지수생성함수는 exp(L(L+1)z/2).

선택한 미덮임 위치들을 왼쪽부터 잇는 DP로 포함배제를 계산. 실제 위치를 선택할 때만 부호를 뒤집고, 가상 오른쪽 경계에서 덮기 조건의 합계를 받음.

독립된 높이별 생성함수와 무제약 exp(Uz)를 곱한 q차 계수에 q!를 곱하면 순서를 구분한 q개 쿼리 수. 같은 쿼리를 여러 번 고르는 경우도 지수함수 계수에 포함.

배열 길이 N, 쿼리 수 Q에서 시간 O(N²Q²), 공간 O(NQ). 모든 계수는 998244353으로 계산.

## 코드와 줄별 설명

[제출 코드](solution.cpp) · [사이트 채점 기록](grading.json) · [별도 로컬 검사](local_checks.json)

~~~cpp
#include <algorithm>
#include <vector>

using namespace std;
static constexpr int MOD = 998244353;
using Polynomial = vector<int>;

static void multiply(Polynomial& product, const Polynomial& factor, int q) {
    Polynomial next(q + 1);
    for (int used = 0; used <= q; ++used) {
        if (product[used] == 0) continue;
        for (int added = 0; used + added <= q; ++added) {
            next[used + added] = static_cast<int>((next[used + added] + 1LL * product[used] * factor[added]) % MOD);
        }
    }
    product.swap(next);
}

int solution(int q, vector<int> a) {
    int n = static_cast<int>(a.size());
    vector<int> inverse(q + 1);
    inverse[1] = 1;
    for (int degree = 2; degree <= q; ++degree) inverse[degree] = static_cast<int>(MOD - 1LL * (MOD / degree) * inverse[MOD % degree] % MOD);
    vector<Polynomial> exponential(n + 1, Polynomial(q + 1));
    for (int length = 0; length <= n; ++length) {
        int intervals = length * (length + 1) / 2;
        exponential[length][0] = 1;
        for (int degree = 1; degree <= q; ++degree) exponential[length][degree] = static_cast<int>(1LL * exponential[length][degree - 1] * intervals % MOD * inverse[degree] % MOD);
    }
    Polynomial product(q + 1);
    product[0] = 1;
    long long unrestricted = 0;
    struct Range { int left, right, floor; };
    vector<Range> stack{{0, n - 1, 0}};
    while (!stack.empty()) {
        Range range = stack.back();
        stack.pop_back();
        int minimum = *min_element(a.begin() + range.left, a.begin() + range.right + 1);
        int length = range.right - range.left + 1;
        unrestricted += 1LL * (minimum - range.floor - 1) * length * (length + 1) / 2;
        vector<int> positions{range.left - 1};
        for (int i = range.left; i <= range.right; ++i) if (a[i] == minimum) positions.push_back(i);
        positions.push_back(range.right + 1);
        int count = static_cast<int>(positions.size());
        vector<Polynomial> paths(count, Polynomial(q + 1));
        paths[0][0] = 1;
        for (int boundary = 1; boundary < count; ++boundary) {
            for (int previous = 0; previous < boundary; ++previous) {
                int gap = positions[boundary] - positions[previous] - 1;
                for (int used = 0; used <= q; ++used) {
                    if (paths[previous][used] == 0) continue;
                    for (int added = 0; used + added <= q; ++added) {
                        int term = static_cast<int>(1LL * paths[previous][used] * exponential[gap][added] % MOD);
                        int& cell = paths[boundary][used + added];
                        if (boundary + 1 == count) {
                            cell += term;
                            if (cell >= MOD) cell -= MOD;
                        } else {
                            cell -= term;
                            if (cell < 0) cell += MOD;
                        }
                    }
                }
            }
        }
        multiply(product, paths.back(), q);
        for (int boundary = 1; boundary < count; ++boundary) {
            int left = positions[boundary - 1] + 1, right = positions[boundary] - 1;
            if (left <= right) stack.push_back({left, right, minimum});
        }
    }
    Polynomial free_queries(q + 1);
    free_queries[0] = 1;
    for (int degree = 1; degree <= q; ++degree) free_queries[degree] = static_cast<int>(1LL * free_queries[degree - 1] * (unrestricted % MOD) % MOD * inverse[degree] % MOD);
    long long coefficient = 0, factorial = 1;
    for (int used = 0; used <= q; ++used) {
        coefficient = (coefficient + 1LL * product[used] * free_queries[q - used]) % MOD;
        if (used > 0) factorial = factorial * used % MOD;
    }
    return static_cast<int>(coefficient * factorial % MOD);
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 현재 연속 구간의 최솟값을 찾을 min_element
// #include <vector>  // 차수별 계수·구간 스택·포함배제 DP
//
// using namespace std;  // 표준 라이브러리 이름 앞의 std:: 생략
// static constexpr int MOD = 998244353;  // 경우의 수를 계산할 소수 나머지
// using Polynomial = vector<int>;  // q차까지만 보관하는 지수생성함수의 계수 배열
//
// static void multiply(Polynomial& product, const Polynomial& factor, int q) {  // 두 지수생성함수를 곱해 q차 이하만 유지
//     Polynomial next(q + 1);  // 곱셈 중 원래 계수를 덮지 않을 새 결과 배열
//     for (int used = 0; used <= q; ++used) {  // 기존 쿼리 종류들이 차지하는 쿼리 수
//         if (product[used] == 0) continue;  // 기여 없는 차수는 생략
//         for (int added = 0; used + added <= q; ++added) {  // 새 쿼리 종류의 개수를 더해 총 q차까지만 계산
//             next[used + added] = static_cast<int>((next[used + added] + 1LL * product[used] * factor[added]) % MOD);  // 같은 총 쿼리 수를 만드는 계수 곱 누적
//         }  // 새 인자의 모든 가능한 차수 조합 끝
//     }  // 잘린 다항식 곱셈 끝
//     product.swap(next);  // 새 결과를 누적 생성함수로 교체
// }  // 생성함수 곱셈 끝
//
// int solution(int q, vector<int> a) {  // 구간 chmax 쿼리 q개로 목표 배열을 만드는 순서열 수 반환
//     int n = static_cast<int>(a.size());  // 목표 배열 길이
//     vector<int> inverse(q + 1);  // 차수 k로 나누는 연산에 필요한 모듈러 역원
//     inverse[1] = 1;  // 1의 역원은 1
//     for (int degree = 2; degree <= q; ++degree) inverse[degree] = static_cast<int>(MOD - 1LL * (MOD / degree) * inverse[MOD % degree] % MOD);  // 더 작은 나머지의 역원으로 2~q의 역원을 준비
//     vector<Polynomial> exponential(n + 1, Polynomial(q + 1));  // 빈 구간 길이에 따른 exp(L(L+1)z/2) 계수
//     for (int length = 0; length <= n; ++length) {  // 포함배제에서 생기는 모든 빈 구간 길이 처리
//         int intervals = length * (length + 1) / 2;  // 이 구간 안에서 고를 수 있는 쿼리 부분구간 수
//         exponential[length][0] = 1;  // 아무 쿼리도 쓰지 않는 0차 계수
//         for (int degree = 1; degree <= q; ++degree) exponential[length][degree] = static_cast<int>(1LL * exponential[length][degree - 1] * intervals % MOD * inverse[degree] % MOD);  // 직전 계수에 intervals/degree를 곱해 intervals^degree/degree! 계산
//     }  // 빈 구간 지수생성함수 준비 끝
//     Polynomial product(q + 1);  // 서로 독립된 높이별 덮기 생성함수를 곱할 배열
//     product[0] = 1;  // 아직 아무 조건도 곱하지 않은 생성함수 1
//     long long unrestricted = 0;  // 어느 정점의 최종 높이도 책임지지 않는 무제약 쿼리 종류 수
//     struct Range { int left, right, floor; };  // 연속 구간의 양끝과 부모 최솟값을 묶은 작업 단위
//     vector<Range> stack{{0, n - 1, 0}};  // 처음에는 전체 구간과 초기 높이 0
//     while (!stack.empty()) {  // 최솟값으로 분리한 모든 높은 구간 처리
//         Range range = stack.back();  // 다음 연속 구간 꺼내기
//         stack.pop_back();  // 처리할 구간은 대기 스택에서 제거
//         int minimum = *min_element(a.begin() + range.left, a.begin() + range.right + 1);  // 이 구간에서 정확히 그 높이의 쿼리로 덮어야 하는 최솟값
//         int length = range.right - range.left + 1;  // 현재 높이 쿼리가 고를 수 있는 연속 구간 길이
//         unrestricted += 1LL * (minimum - range.floor - 1) * length * (length + 1) / 2;  // 부모 높이와 minimum 사이의 빠진 높이들은 모든 부분구간 쿼리가 무제약
//         vector<int> positions{range.left - 1};  // 왼쪽에 실제 정점이 아닌 시작 경계 추가
//         for (int i = range.left; i <= range.right; ++i) if (a[i] == minimum) positions.push_back(i);  // 현재 높이로 반드시 덮어야 하는 모든 최솟값 위치
//         positions.push_back(range.right + 1);  // 포함배제 합계를 받을 오른쪽 가상 경계
//         int count = static_cast<int>(positions.size());  // 실제 필수 위치와 양끝 경계를 합한 개수
//         vector<Polynomial> paths(count, Polynomial(q + 1));  // 선택한 미덮임 위치들을 잇는 포함배제 생성함수 DP
//         paths[0][0] = 1;  // 왼쪽 경계에서 시작하는 빈 선택의 계수
//         for (int boundary = 1; boundary < count; ++boundary) {  // 다음 미덮임 위치 또는 마지막 가상 경계 선택
//             for (int previous = 0; previous < boundary; ++previous) {  // 바로 직전에 고른 경계를 모두 시도
//                 int gap = positions[boundary] - positions[previous] - 1;  // 두 미덮임 위치를 피하는 쿼리들이 들어갈 빈 구간 길이
//                 for (int used = 0; used <= q; ++used) {  // 이전 경계까지의 생성함수 차수
//                     if (paths[previous][used] == 0) continue;  // 기여 없는 차수는 생략
//                     for (int added = 0; used + added <= q; ++added) {  // 새 빈 구간 안 쿼리 수를 기존 계수에 합치기
//                         int term = static_cast<int>(1LL * paths[previous][used] * exponential[gap][added] % MOD);  // 이전 선택과 빈 구간 쿼리들을 함께 쓰는 계수 곱
//                         int& cell = paths[boundary][used + added];  // 총 쿼리 수에 해당하는 다음 경계 계수의 참조
//                         if (boundary + 1 == count) {  // 실제 미덮임 사건이 아닌 가상 끝 경계는 양의 부호
//                             cell += term;  // 해당 포함배제 경로의 기여 더하기
//                             if (cell >= MOD) cell -= MOD;  // 나머지를 범위 안에 유지
//                         } else {  // 실제 최솟값 위치를 미덮임으로 선택하면 부호 반전
//                             cell -= term;  // 미덮임 사건 하나를 추가한 기여 빼기
//                             if (cell < 0) cell += MOD;  // 음수 나머지를 0 이상으로 조정
//                         }  // 다음 경계의 포함배제 부호 반영 끝
//                     }  // 빈 구간 안 쿼리 수 조합 끝
//                 }  // 이전 경계의 모든 차수 처리 끝
//             }  // 직전 경계 후보 처리 끝
//         }  // 현재 높이의 필수 위치들을 모두 덮는 생성함수 완성
//         multiply(product, paths.back(), q);  // 독립된 현재 높이의 쿼리 종류를 전체 생성함수에 곱하기
//         for (int boundary = 1; boundary < count; ++boundary) {  // 최솟값 위치들 사이의 높은 연속 구간 분리
//             int left = positions[boundary - 1] + 1, right = positions[boundary] - 1;  // 다음 높이에서 처리할 실제 정점 구간
//             if (left <= right) stack.push_back({left, right, minimum});  // 비어 있지 않은 높은 구간만 대기 스택에 추가
//         }  // 자식 구간 등록 끝
//     }  // 모든 필수 높이의 덮기 조건 처리 끝
//     Polynomial free_queries(q + 1);  // 무제약 종류들을 세는 exp(unrestricted*z) 계수
//     free_queries[0] = 1;  // 무제약 쿼리를 0개 쓰는 계수
//     for (int degree = 1; degree <= q; ++degree) free_queries[degree] = static_cast<int>(1LL * free_queries[degree - 1] * (unrestricted % MOD) % MOD * inverse[degree] % MOD);  // unrestricted^degree/degree!를 차례대로 계산
//     long long coefficient = 0, factorial = 1;  // 최종 q차 계수와 순서열의 순서를 복원할 q!
//     for (int used = 0; used <= q; ++used) {  // 필수 종류와 무제약 종류가 나눠 차지하는 쿼리 수
//         coefficient = (coefficient + 1LL * product[used] * free_queries[q - used]) % MOD;  // 전체 생성함수 곱의 q차 계수만 합산
//         if (used > 0) factorial = factorial * used % MOD;  // 1~q를 곱해 q! 준비
//     }  // 최종 계수와 팩토리얼 계산 끝
//     return static_cast<int>(coefficient * factorial % MOD);  // q차 계수에 q!를 곱해 반복 쿼리도 포함하는 실제 순서열 수 반환
// }  // 지역 컨테이너는 호출이 끝나면 해제되어 다음 채점에 상태가 남지 않음

// 풀이 요약
// 목표를 넘지 않는 쿼리만 허용하면, 각 i가 높이 a[i]의 쿼리에 한 번 이상 덮이는 것이 최종 배열과 같아지는 조건.
// 구간의 최솟값 h 위치들을 나누면 높이 h 쿼리는 이 구간 안에서만 움직이고, 더 높은 쿼리는 최솟값 사이 구간들로 분리됨. 부모 높이와 h 사이 빠진 높이는 무제약 쿼리 종류로 누적.
// 높이 h의 필수 위치를 못 덮는 사건에 포함배제 적용. 선택한 미덮임 위치 사이 길이가 L이면 허용 부분구간 수는 L(L+1)/2라 그 쿼리들의 지수생성함수는 exp(L(L+1)z/2).
// 선택한 미덮임 위치들을 왼쪽부터 잇는 DP로 포함배제를 계산. 실제 위치를 선택할 때만 부호를 뒤집고, 가상 오른쪽 경계에서 덮기 조건의 합계를 받음.
// 독립된 높이별 생성함수와 무제약 exp(Uz)를 곱한 q차 계수에 q!를 곱하면 순서를 구분한 q개 쿼리 수. 같은 쿼리를 여러 번 고르는 경우도 지수함수 계수에 포함.
// 배열 길이 N, 쿼리 수 Q에서 시간 O(N²Q²), 공간 O(NQ). 모든 계수는 998244353으로 계산.
~~~

## 채점 기록

2026-10-24 사이트 채점: 정답 100/100. 1번째 제출에서 통과. C++ 제출 내역에서도 같은 날짜의 정답 기록 확인.

줄별 설명과 풀이 요약을 포함한 코드를 제출. 로컬 검사 횟수와 실행 시간은 사이트 채점 기록과 별도로 보관.
