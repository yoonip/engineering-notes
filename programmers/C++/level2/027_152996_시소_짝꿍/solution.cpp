#include <array>
#include <utility>
#include <vector>
using namespace std;

long long solution(vector<int> weights) {
    vector<long long> counts(4001, 0);
    for (int weight : weights) ++counts[weight];
    long long answer = 0;
    array<pair<int, int>, 3> ratios{{{2, 1}, {3, 2}, {4, 3}}};
    for (int weight = 100; weight <= 1000; ++weight) {
        long long count = counts[weight];
        answer += count * (count - 1) / 2;
        for (auto [numerator, denominator] : ratios) {
            if (weight * numerator % denominator == 0) answer += count * counts[weight * numerator / denominator];
        }
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <array>  // 크기가 고정된 array
// #include <utility>  // 두 값을 묶는 pair와 이동 유틸리티
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// long long solution(vector<int> weights) {  // 거리 비율에 맞는 몸무게 쌍의 수 계산
// vector<long long> counts(4001, 0);  // 가능한 짝의 무게까지 조회할 수 있도록 빈도 배열 만들기
// for (int weight : weights) ++counts[weight];  // 각 몸무게의 사람 수 세기
// long long answer = 0;  // 시소 짝의 수를 넓은 정수형으로 누적
// array<pair<int, int>, 3> ratios{{{2, 1}, {3, 2}, {4, 3}}};  // 서로 다른 몸무게에서 가능한 큰 쪽과 작은 쪽의 비율
// for (int weight = 100; weight <= 1000; ++weight) {  // 가능한 몸무게를 작은 쪽 기준으로 순회
// long long count = counts[weight];  // 현재 몸무게의 사람 수 읽기
// answer += count * (count - 1) / 2;  // 몸무게가 같은 두 사람의 조합 수를 더하기
// for (auto [numerator, denominator] : ratios) {  // 거리 2, 3, 4에서 나오는 세 비율 검사
// if (weight * numerator % denominator == 0) answer += count * counts[weight * numerator / denominator];  // 짝의 몸무게가 정수이면 두 빈도의 곱을 더하기
// }  // 블록 끝
// }  // 블록 끝
// return answer;  // 중복 없이 센 시소 짝 수 반환
// }  // 블록 끝

// 풀이 요약
// 같은 몸무게의 조합 수와 서로 다른 몸무게의 비율 2:1, 3:2, 4:3에 맞는 두 빈도의 곱을 더하기
