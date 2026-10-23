#include <stddef.h>

int solution(int num_list[], size_t num_list_len) {
    long long product = 1, sum = 0;
    for (size_t i = 0; i < num_list_len; ++i) {
        product *= num_list[i]; sum += num_list[i];
    }
    return product < sum * sum;
}

// 전체 코드 줄별 설명
// #include <stddef.h>  // 배열 길이와 인덱스에 쓰는 size_t
//
// int solution(int num_list[], size_t num_list_len) {  // 원소들의 곱과 합 풀이 시작
//     long long product = 1, sum = 0;  // 정수 곱과 합을 각각 1과 0으로 초기화하고 long long형으로 계산 범위를 확보
//     for (size_t i = 0; i < num_list_len; ++i) {  // for로 정수 목록의 인덱스를 처음부터 끝까지 순회
//         product *= num_list[i]; sum += num_list[i];  // *=로 현재 원소를 누적 곱에 곱하고 +=로 누적 합에 더하기
//     }  // 블록 끝
//     return product < sum * sum;  // <로 전체 곱과 합의 제곱을 비교해 1 또는 0을 반환
// }  // 블록 끝

// 풀이 요약
// 모든 원소의 곱과 합의 제곱을 계산해 비교
