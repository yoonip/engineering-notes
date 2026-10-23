#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <limits.h>

int solution(int schedules[], size_t schedules_len, int** timelogs, size_t timelogs_rows, size_t timelogs_cols, int startday) {
    int answer = 0;
    for (size_t i = 0; i < schedules_len; ++i) {
        int limit = schedules[i] / 100 * 60 + schedules[i] % 100 + 10;
        bool eligible = true;
        for (int day = 0; day < 7; ++day) {
            if ((startday + day - 1) % 7 >= 5) continue;
            int arrival = timelogs[i][day] / 100 * 60 + timelogs[i][day] % 100;
            if (arrival > limit) { eligible = false; break; }
        }
        if (eligible) ++answer;
    }
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
// int solution(int schedules[], size_t schedules_len, int** timelogs, size_t timelogs_rows, size_t timelogs_cols, int startday) {  // 시각을 분으로 바꾸고 출근 희망 시각에 10분을 더하기; 주말을 제외한 모든 출근 기록이 제한 이내인 직원 수를 세기
//     int answer = 0;  // 이벤트 대상 직원 수 저장
//     for (size_t i = 0; i < schedules_len; ++i) {  // 검사할 직원 번호 순서대로 확인
//         int limit = schedules[i] / 100 * 60 + schedules[i] % 100 + 10;  // 희망 출근 시각에 10분 더한 기준 저장
//         bool eligible = true;  // 평일을 모두 지킨 직원인지 여부 저장
//         for (int day = 0; day < 7; ++day) {  // 일주일 중 날짜 위치 순서대로 확인
//             if ((startday + day - 1) % 7 >= 5) continue;  // 토요일과 일요일은 출근 시각 검사에서 제외
//             int arrival = timelogs[i][day] / 100 * 60 + timelogs[i][day] % 100;  // 현재 날짜의 출근 시각 저장
//             if (arrival > limit) { eligible = false; break; }  // 평일 출근이 허용 시각을 넘으면 대상에서 제외하고 이 직원 확인 종료
//         }  // 이 범위 끝
//         if (eligible) ++answer;  // 평일을 모두 지킨 직원인지 여부가 남아 있으면 이벤트 대상 직원 수 갱신
//     }  // 이 범위 끝
//     return answer;  // 이벤트 대상 직원 수 반환
// }  // 이 범위 끝

// 풀이 요약
// 시각을 분으로 바꾸고 출근 희망 시각에 10분을 더하기; 주말을 제외한 모든 출근 기록이 제한 이내인 직원 수를 세기
