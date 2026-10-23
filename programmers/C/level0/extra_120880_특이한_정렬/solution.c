#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int* solution(int numlist[], size_t numlist_len, int n) {
    int* answer = malloc(numlist_len * sizeof(*answer));
    memcpy(answer, numlist, numlist_len * sizeof(*answer));
    for (size_t i = 1; i < numlist_len; ++i) {
        int value = answer[i];
        size_t j = i;
        while (j > 0 && (abs(answer[j - 1] - n) > abs(value - n) ||
            (abs(answer[j - 1] - n) == abs(value - n) && answer[j - 1] < value))) {
            answer[j] = answer[j - 1]; --j;
        }
        answer[j] = value;
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
// int* solution(int numlist[], size_t numlist_len, int n) {  // 특이한 정렬 풀이 시작
//     int* answer = malloc(numlist_len * sizeof(*answer));  // answer를 저장할 메모리 확보
//     memcpy(answer, numlist, numlist_len * sizeof(*answer));  // memcpy는 지정한 바이트 수만큼 원본 배열·문자열을 결과 공간으로 복사
//     for (size_t i = 1; i < numlist_len; ++i) {  // 정렬된 앞부분에 다음 원소를 하나씩 끼워 넣음
//         int value = answer[i];  // 이번에 정렬된 앞부분에 끼워 넣을 값
//         size_t j = i;  // 삽입할 위치를 현재 인덱스부터 앞으로 탐색
//         while (j > 0 && (abs(answer[j - 1] - n) > abs(value - n) ||  // 삽입할 값보다 기준 n에서 멀리 있는 앞 원소는 오른쪽으로 이동할 대상
//             (abs(answer[j - 1] - n) == abs(value - n) && answer[j - 1] < value))) {  // 거리가 같을 때는 값이 더 작은 앞 원소도 뒤로 밀어 큰 값이 먼저 오도록 처리
//             answer[j] = answer[j - 1]; --j;  // 앞 원소를 한 칸 뒤로 밀고 삽입할 위치 j를 왼쪽으로 이동
//         }  // 블록 끝
//         answer[j] = value;  // 앞 원소를 밀어 만든 빈자리에 현재 값 삽입
//     }  // 블록 끝
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 기준 n까지의 거리가 작은 값부터 삽입 정렬. 거리가 같으면 더 큰 수가 앞에 오도록 앞 원소를 밀고 삽입.
