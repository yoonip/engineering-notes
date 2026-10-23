#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int* solution(int** score, size_t score_rows, size_t score_cols) {
    (void)score_cols;
    int* answer = malloc(score_rows * sizeof(*answer));
    for (size_t i = 0; i < score_rows; ++i) {
        answer[i] = 1;
        for (size_t j = 0; j < score_rows; ++j)
            answer[i] += score[j][0] + score[j][1] > score[i][0] + score[i][1];
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <ctype.h>  // 문자 검사와 대소문자 변환
// #include <limits.h>  // 정수형 최솟값·최댓값 상수
//
// int* solution(int** score, size_t score_rows, size_t score_cols) {  // 등수 매기기 풀이 시작
//     (void)score_cols;  // 각 행에서 두 과목 점수를 고정된 인덱스 0과 1로 읽으므로 열 개수 score_cols를 별도 계산에 사용하지 않음을 표시
//     int* answer = malloc(score_rows * sizeof(*answer));  // malloc으로 학생 수 score_rows만큼 등수를 담을 정수 배열 공간을 확보
//     for (size_t i = 0; i < score_rows; ++i) {  // 바깥 for로 등수를 구할 학생의 인덱스 i를 순서대로 선택
//         answer[i] = 1;  // 현재 학생의 등수를 1로 시작하여 자신보다 점수가 높은 학생 수를 더할 준비
//         for (size_t j = 0; j < score_rows; ++j)  // 안쪽 for로 비교 대상 학생의 인덱스 j를 전체 학생 범위에서 순회
//             answer[i] += score[j][0] + score[j][1] > score[i][0] + score[i][1];  // 학생 j의 두 과목 합이 학생 i의 합보다 큰 경우에만 등수에 1을 더하기. 합이 같으면 더하지 않아 공동 등수가 되며, 평균 대신 합을 비교해도 대소 관계가 같음
//     }  // 블록 끝
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 각 학생보다 두 과목 점수 합이 큰 학생 수에 1을 더해 등수를 구하기. 합이 같은 학생은 더하지 않아 공동 등수가 되며, 평균 대신 합을 비교해도 순서는 같음
