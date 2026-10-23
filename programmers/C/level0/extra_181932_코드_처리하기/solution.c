#include <stdlib.h>
#include <string.h>

char* solution(const char* code) {
    size_t n = strlen(code), used = 0;
    char* answer = malloc((n > 5 ? n : 5) + 1);
    int mode = 0;
    for (size_t i = 0; i < n; ++i) {
        if (code[i] == '1') mode = 1 - mode;
        else if ((int)(i % 2) == mode) answer[used++] = code[i];
    }
    answer[used] = '\0';
    if (!used) strcpy(answer, "EMPTY");
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
//
// char* solution(const char* code) {  // 코드 처리하기 풀이 시작
//     size_t n = strlen(code), used = 0;  // strlen으로 입력 길이를 구하고 결과에 저장한 문자 개수를 0으로 초기화
//     char* answer = malloc((n > 5 ? n : 5) + 1);  // malloc으로 입력 길이와 EMPTY 길이 중 큰 값에 맞춰 종료 문자까지 저장할 공간을 할당
//     int mode = 0;  // 문자 선택 규칙을 나타내는 모드를 0으로 초기화
//     for (size_t i = 0; i < n; ++i) {  // size_t형 인덱스를 for로 증가시키며 각 위치를 차례로 처리
//         if (code[i] == '1') mode = 1 - mode;  // if로 모드 변경 문자를 검사하고 1에서 현재 값을 빼 0과 1을 전환
//         else if ((int)(i % 2) == mode) answer[used++] = code[i];  // %로 인덱스의 홀짝을 구해 모드와 같으면 문자를 저장하고 개수를 늘림
//     }  // 블록 끝
//     answer[used] = '\0';  // 결과의 마지막 위치에 널 문자를 넣어 C 문자열을 종료
//     if (!used) strcpy(answer, "EMPTY");  // !로 빈 결과를 검사하고 strcpy로 EMPTY와 종료 문자를 복사
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 문자 1은 모드를 바꾸고, 나머지는 모드와 인덱스 홀짝이 같을 때만 연결
