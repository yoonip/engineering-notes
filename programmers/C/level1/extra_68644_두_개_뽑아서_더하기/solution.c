#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <limits.h>

int* solution(int numbers[], size_t numbers_len) {
    bool sums[201] = {false};
    for (size_t i = 0; i < numbers_len; ++i) for (size_t j = i + 1; j < numbers_len; ++j) sums[numbers[i] + numbers[j]] = true;
    size_t length = 0; for (int sum = 0; sum <= 200; ++sum) if (sums[sum]) ++length;
    int* answer = malloc(length * sizeof(int)); size_t out = 0;
    for (int sum = 0; sum <= 200; ++sum) if (sums[sum]) answer[out++] = sum;
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // 문자열 형식 읽기·쓰기용 표준 입출력 선언
// #include <stdlib.h>  // 동적 메모리, 정수 변환, 정렬 함수 선언
// #include <stdbool.h>  // 참·거짓 표시용 bool, true, false
// #include <string.h>  // 문자열 길이·비교·복사와 메모리 함수 선언
// #include <ctype.h>  // 문자 종류 확인과 대소문자 변환
// #include <math.h>  // 정수 제곱근 계산 등에 쓸 수학 함수
// #include <limits.h>  // 최솟값·최댓값 초기화에 쓸 정수 범위 상수
//
// int* solution(int numbers[], size_t numbers_len) {  // 서로 다른 두 인덱스의 합을 모두 기록; 중복을 제거하고 오름차순으로 반환
//     bool sums[201] = {false};  // 두 수의 합이 나왔는지 표시한 표 저장
//     for (size_t i = 0; i < numbers_len; ++i) for (size_t j = i + 1; j < numbers_len; ++j) sums[numbers[i] + numbers[j]] = true;  // 서로 다른 두 위치만 골라 합이 나왔는지 표시
//     size_t length = 0; for (int sum = 0; sum <= 200; ++sum) if (sums[sum]) ++length;  // 서로 다른 합의 개수 / 결과로 꺼낼 합 후보 저장
//     int* answer = malloc(length * sizeof(int)); size_t out = 0;  // 중복 없는 두 수의 합 / 오름차순 결과의 다음 위치 공간 확보
//     for (int sum = 0; sum <= 200; ++sum) if (sums[sum]) answer[out++] = sum;  // 나온 적 있는 합만 작은 값부터 결과에 추가
//     return answer;  // 중복 없는 두 수의 합 반환
// }  // 이 범위 끝

// 풀이 요약
// 서로 다른 두 인덱스의 합을 모두 기록; 중복을 제거하고 오름차순으로 반환
