#include <stdlib.h>

int* solution(int start_num, int end_num) {
    int count = end_num - start_num + 1;
    int* answer = malloc(count * sizeof(int));
    for (int i = 0; i < count; ++i) answer[i] = start_num + i;
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
//
// int* solution(int start_num, int end_num) {  // 카운트 업 풀이 시작
//     int count = end_num - start_num + 1;  // 양 끝을 포함한 정수 개수를 뺄셈과 덧셈으로 구하기
//     int* answer = malloc(count * sizeof(int));  // malloc으로 결과 정수 배열을 할당하며 sizeof(int)로 한 원소의 바이트 수를 구하기
//     for (int i = 0; i < count; ++i) answer[i] = start_num + i;  // for로 결과 인덱스를 순회하며 시작값에 인덱스를 더한 수를 저장
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 시작값부터 끝값까지 1씩 증가하는 정수를 저장
