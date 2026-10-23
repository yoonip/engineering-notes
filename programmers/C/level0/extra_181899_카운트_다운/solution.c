#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

int* solution(int start_num, int end_num) {
    int n = start_num - end_num + 1;
    int* answer = malloc(n * sizeof(int));
    for (int i = 0; i < n; ++i) answer[i] = start_num - i;
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <ctype.h>  // 문자 검사와 대소문자 변환
//
// int* solution(int start_num, int end_num) {  // 카운트 다운 풀이 시작
//     int n = start_num - end_num + 1;  // 시작값과 끝값을 모두 포함하는 감소 수열의 길이 계산
//     int* answer = malloc(n * sizeof(int));  // answer를 저장할 메모리 확보
//     for (int i = 0; i < n; ++i) answer[i] = start_num - i;  // 시작값에서 인덱스만큼 빼서 끝값까지 1씩 감소하는 수열 저장
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 시작값에서 1씩 뺀 값을 차례로 저장해 끝값까지 포함하는 감소 수열 생성.
