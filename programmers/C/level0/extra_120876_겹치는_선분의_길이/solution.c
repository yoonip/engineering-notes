#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int solution(int** lines, size_t lines_rows, size_t lines_cols) {
    (void)lines_cols;
    int covered[200] = {0}, answer = 0;
    for (size_t i = 0; i < lines_rows; ++i)
        for (int x = lines[i][0]; x < lines[i][1]; ++x) ++covered[x + 100];
    for (int i = 0; i < 200; ++i) answer += covered[i] >= 2;
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
// int solution(int** lines, size_t lines_rows, size_t lines_cols) {  // 겹치는 선분의 길이 풀이 시작
//     (void)lines_cols;  // 각 선분의 시작·끝 좌표를 인덱스 0과 1로 읽으므로 열 개수 lines_cols를 별도 계산에 사용하지 않음을 표시
//     int covered[200] = {0}, answer = 0;  // covered의 200개 값을 0으로 초기화하여 -100부터 99까지에서 시작하는 길이 1 구간의 덮인 횟수를 저장. answer는 겹친 구간의 총길이임
//     for (size_t i = 0; i < lines_rows; ++i)  // 바깥 for로 각 선분의 인덱스 i를 순회
//         for (int x = lines[i][0]; x < lines[i][1]; ++x) ++covered[x + 100];  // 선분의 시작 x부터 끝 좌표 직전까지 순회하며 단위 구간 [x, x + 1)의 덮인 횟수를 늘림. x + 100은 음수 좌표를 배열 인덱스로 옮기기
//     for (int i = 0; i < 200; ++i) answer += covered[i] >= 2;  // 모든 단위 구간을 확인하여 덮인 횟수가 2 이상인 구간마다 길이 1을 answer에 더하기
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 각 선분이 덮는 길이 1 구간의 횟수를 세고, 두 번 이상 덮인 구간의 개수를 더하기. 끝점만 맞닿은 경우에는 겹친 길이가 추가되지 않음
