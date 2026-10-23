#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <limits.h>
#include <stdint.h>

int solution(int cookie[], size_t cookie_len) {
    int n = (int)cookie_len, answer = 0;
    for (int middle = 0; middle + 1 < n; ++middle) {
        int left = middle, right = middle + 1, left_sum = cookie[left], right_sum = cookie[right];
        for (;;) {
            if (left_sum == right_sum && left_sum > answer) answer = left_sum;
            if (left_sum <= right_sum) { if (!left) break; left_sum += cookie[--left]; }
            else { if (right == n - 1) break; right_sum += cookie[++right]; }
        }
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // 문자열 형식 읽기·쓰기용 표준 입출력 선언
// #include <stdlib.h>  // 동적 메모리, 정수 변환, 정렬 함수 선언
// #include <string.h>  // 문자열 길이·비교·복사와 메모리 함수 선언
// #include <stdbool.h>  // 참·거짓 표시용 bool, true, false
// #include <limits.h>  // 최솟값·최댓값 초기화에 쓸 정수 범위 상수
// #include <stdint.h>  // 비트 마스크와 해시 키에 쓸 고정 폭 정수
//
// int solution(int cookie[], size_t cookie_len) {  // 두 아들의 구간은 붙어 있어야 하므로 경계 m을 고정하고 양쪽 포인터를 바깥으로 확장하기; 양수 배열이라 합이 작은 쪽만 늘리면 됨
//     int n = (int)cookie_len, answer = 0;  // 봉지 개수 / 똑같이 줄 수 있는 최대 쿠키 수 저장
//     for (int middle = 0; middle + 1 < n; ++middle) {  // 두 자식 봉지 사이의 경계 순서대로 확인
//         int left = middle, right = middle + 1, left_sum = cookie[left], right_sum = cookie[right];  // 왼쪽 자식의 첫 봉지 / 오른쪽 자식의 마지막 봉지 / 왼쪽 자식에게 준 쿠키 합 / 오른쪽 자식에게 준 쿠키 합 저장
//         for (;;) {  // 남은 후보를 순서대로 확인
//             if (left_sum == right_sum && left_sum > answer) answer = left_sum;  // 양쪽 연속 구간의 쿠키 합이 같고 더 크면 답 갱신
//             if (left_sum <= right_sum) { if (!left) break; left_sum += cookie[--left]; }  // 왼쪽 합이 더 작거나 같으면 왼쪽 봉지를 확장하고 더 없으면 중단
//             else { if (right == n - 1) break; right_sum += cookie[++right]; }  // 앞 조건이 아니면 오른쪽 자식의 마지막 봉지 갱신
//         }  // 이 범위 끝
//     }  // 이 범위 끝
//     return answer;  // 똑같이 줄 수 있는 최대 쿠키 수 반환
// }  // 이 범위 끝

// 풀이 요약
// 두 아들의 구간은 붙어 있어야 하므로 경계 m을 고정하고 양쪽 포인터를 바깥으로 확장하기; 양수 배열이라 합이 작은 쪽만 늘리면 됨
// 예: [1,1,2,3]에서 왼쪽 [1,2], 오른쪽 [3]을 선택하면 한 사람당 3개
// 각 경계에서 포인터가 최대 n번 움직; 시간 O(n^2), 추가 공간 O(1)
