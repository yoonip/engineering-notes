#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>
#include <math.h>

int* solution(int n, int info[], size_t info_len) {
    (void)info_len;
    int* answer = calloc(11, sizeof(*answer)); int best = 0;
    for (unsigned mask = 0; mask < (1u << 10); ++mask) {
        int shots[11] = {0}, remaining = n, difference = 0;
        for (int i = 0; i < 10; ++i) if (mask & (1u << i)) { shots[i] = info[i] + 1; remaining -= shots[i]; }
        if (remaining < 0) continue;
        shots[10] = remaining;
        for (int i = 0; i < 10; ++i) {
            if (shots[i] > info[i]) difference += 10 - i;
            else if (info[i]) difference -= 10 - i;
        }
        bool better = difference > best;
        if (difference > 0 && difference == best)
            for (int i = 10; i >= 0; --i) if (shots[i] != answer[i]) { better = shots[i] > answer[i]; break; }
        if (better) { best = difference; memcpy(answer, shots, sizeof(shots)); }
    }
    if (!best) answer[0] = -1;
    return answer;
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
// int* solution(int n, int info[], size_t info_len) {  // 각 점수에서 이기려면 어피치보다 한 발 더 쏘고, 포기하면 0발로 두기; 모든 점수 선택을 검사하고 남은 화살은 0점에 두기
//     (void)info_len;  // 입력 형식에만 필요한 길이 값은 계산에서 생략
//     int* answer = calloc(11, sizeof(*answer)); int best = 0;  // 가장 유리한 라이언 화살 배분 / 현재 최대 점수 차 공간 확보하고 0으로 시작
//     for (unsigned mask = 0; mask < (1u << 10); ++mask) {  // 남은 후보를 순서대로 확인
//         int shots[11] = {0}, remaining = n, difference = 0;  // 현재 선택의 화살 배분 / 아직 배분하지 않은 화살 / 라이언 점수에서 어피치 점수를 뺀 값 저장
//         for (int i = 0; i < 10; ++i) if (mask & (1u << i)) { shots[i] = info[i] + 1; remaining -= shots[i]; }  // 선택한 점수에는 어피치보다 한 발 더 쏘고 남은 화살에서 차감
//         if (remaining < 0) continue;  // 아직 배분하지 않은 화살가 0보다 작으면 다음 후보로 넘어가기
//         shots[10] = remaining;  // 현재 선택의 화살 배분 갱신
//         for (int i = 0; i < 10; ++i) {  // 점수 칸 번호 순서대로 확인
//             if (shots[i] > info[i]) difference += 10 - i;  // 라이언이 더 많이 맞힌 점수는 점수 차이에 더하기
//             else if (info[i]) difference -= 10 - i;  // 라이언이 이기지 못하고 어피치 화살이 있으면 어피치 점수 차감
//         }  // 이 범위 끝
//         bool better = difference > best;  // 현재 배분이 더 나은지 여부 저장
//         if (difference > 0 && difference == best)  // 양수 점수 차이가 기존 최고와 같으면 낮은 점수의 화살 수로 우선순위 비교
//             for (int i = 10; i >= 0; --i) if (shots[i] != answer[i]) { better = shots[i] > answer[i]; break; }  // 낮은 점수부터 처음 다른 칸을 찾아 화살이 더 많은 배분 우선
//         if (better) { best = difference; memcpy(answer, shots, sizeof(shots)); }  // 현재 배분이 더 나은지 여부가 남아 있으면 현재 최대 점수 차 복사
//     }  // 이 범위 끝
//     if (!best) answer[0] = -1;  // 현재 최대 점수 차가 없으면 가장 유리한 라이언 화살 배분 갱신
//     return answer;  // 가장 유리한 라이언 화살 배분 반환
// }  // 이 범위 끝

// 풀이 요약
// 각 점수에서 이기려면 어피치보다 한 발 더 쏘고, 포기하면 0발로 두기; 모든 점수 선택을 검사하고 남은 화살은 0점에 두기
// 예: 첫 예제의 최적 배치는 [0,2,2,0,1,0,0,0,0,0,0].; 동률은 낮은 점수부터 비교.; 시간 O(2^10*11), 공간 O(11)
