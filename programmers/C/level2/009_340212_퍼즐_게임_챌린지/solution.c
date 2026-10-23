#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>
#include <math.h>

int solution(int diffs[], size_t diffs_len, int times[], size_t times_len, long long limit) {
    (void)times_len;
    int low = 1, high = 1;
    for (size_t i = 0; i < diffs_len; ++i) if (diffs[i] > high) high = diffs[i];
    while (low < high) {
        int level = low + (high - low) / 2, previous = 0; long long elapsed = 0;
        for (size_t i = 0; i < diffs_len; ++i) {
            elapsed += times[i];
            if (diffs[i] > level) elapsed += (long long)(diffs[i] - level) * (times[i] + previous);
            if (elapsed > limit) break;
            previous = times[i];
        }
        if (elapsed <= limit) high = level; else low = level + 1;
    }
    return low;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // 문자열 형식 읽기·쓰기용 표준 입출력 선언
// #include <stdlib.h>  // 동적 메모리, 정수 변환, 정렬 함수 선언
// #include <string.h>  // 문자열 길이·비교·복사와 메모리 함수 선언
// #include <stdbool.h>  // 참·거짓 표시용 bool, true, false
// #include <ctype.h>  // 문자 종류 확인과 대소문자 변환
// #include <limits.h>  // 최솟값·최댓값 초기화에 쓸 정수 범위 상수
// #include <math.h>  // 정수 제곱근 계산 등에 쓸 수학 함수
//
// int solution(int diffs[], size_t diffs_len, int times[], size_t times_len, long long limit) {  // 퍼즐 시간은 current+max(0,diff-level)*(current+previous); 숙련도가 높아질수록 시간은 줄거나 같음
//     (void)times_len;  // 입력 형식에만 필요한 길이 값은 계산에서 생략
//     int low = 1, high = 1;  // 가능한 숙련도 하한 / 숙련도 상한 저장
//     for (size_t i = 0; i < diffs_len; ++i) if (diffs[i] > high) high = diffs[i];  // 가장 높은 난도를 숙련도 이분 탐색의 상한으로 사용
//     while (low < high) {  // 이분 탐색 범위가 한 값으로 좁혀질 때까지 중간값의 가능 여부를 확인
//         int level = low + (high - low) / 2, previous = 0; long long elapsed = 0;  // 시험할 중간 숙련도 / 직전 퍼즐 소요 시간 / 현재 숙련도의 총소요 시간 저장
//         for (size_t i = 0; i < diffs_len; ++i) {  // 계산할 퍼즐 번호 순서대로 확인
//             elapsed += times[i];  // 현재 숙련도의 총소요 시간 / 계산할 퍼즐 번호 더해 누적
//             if (diffs[i] > level) elapsed += (long long)(diffs[i] - level) * (times[i] + previous);  // 숙련도보다 어려운 만큼 현재와 이전 퍼즐 시간을 반복 실패 비용으로 추가
//             if (elapsed > limit) break;  // 제한 시간을 이미 넘었으면 남은 퍼즐 계산 중단
//             previous = times[i];  // 직전 퍼즐 소요 시간 갱신
//         }  // 이 범위 끝
//         if (elapsed <= limit) high = level; else low = level + 1;  // 제한 시간 안이면 숙련도를 낮추고, 넘었으면 숙련도를 높이기
//     }  // 이 범위 끝
//     return low;  // 가능한 숙련도 하한 반환
// }  // 이 범위 끝

// 풀이 요약
// 퍼즐 시간은 current+max(0,diff-level)*(current+previous); 숙련도가 높아질수록 시간은 줄거나 같음
// 이 단조성을 이용해 제한 시간 안에 가능한 최소 숙련도를 이진 탐색; 시간 O(n log 최대 난이도), 추가 공간 O(1)
// 예: [1,5,3], [2,4,7], 제한30에서 숙련도2는42, 3은25이므로 최소3
