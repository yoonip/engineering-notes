#include <algorithm>
using namespace std;

int solution(int h1, int m1, int s1, int h2, int m2, int s2) {
    long long start = h1 * 3600 + m1 * 60 + s1, end = h2 * 3600 + m2 * 60 + s2;
    auto count = [](long long t) { return t * 719 / 43200 + t * 59 / 3600 - t / 43200 + 1; };
    bool at_start = start * 719 % 43200 == 0 || start * 59 % 3600 == 0;
    return (int)(count(end) - count(start) + at_start);
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// using namespace std;  // std:: 접두사 생략
// int solution(int h1, int m1, int s1, int h2, int m2, int s2) {  // 초침이 다른 바늘과 겹치는 횟수 계산
// long long start = h1 * 3600 + m1 * 60 + s1, end = h2 * 3600 + m2 * 60 + s2;  // 시작과 끝을 자정 이후의 초로 바꾸기
// auto count = [](long long t) { return t * 719 / 43200 + t * 59 / 3600 - t / 43200 + 1; };  // 초침과 시침 및 분침의 누적 만남에서 동시 만남 중복 빼기
// bool at_start = start * 719 % 43200 == 0 || start * 59 % 3600 == 0;  // 시작 시각 자체가 겹침인지 정수 나머지로 확인
// return (int)(count(end) - count(start) + at_start);  // 누적 횟수의 차이에 시작 시각 포함 여부를 더하기
// }  // 블록 끝

// 풀이 요약
// 초침과 시침 및 분침의 상대 속도로 누적 겹침 횟수를 구하고 시작 시각 포함 여부와 동시 겹침 중복 처리
