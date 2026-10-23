#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <limits.h>
#include <stdint.h>

static int position(const char* r, const char* c) { return (atoi(r) - 1) * 50 + atoi(c) - 1; }
char** solution(const char* commands[], size_t commands_len) {
    int groups[2500]; char (*values)[51] = calloc(2500, sizeof(*values));
    for (int i = 0; i < 2500; ++i) groups[i] = i;
    char** answer = malloc(commands_len * sizeof(*answer)); size_t count = 0;
    for (size_t index = 0; index < commands_len; ++index) {
        char operation[16], a[51], b[51], c[51], d[51];
        int fields = sscanf(commands[index], "%15s %50s %50s %50s %50s", operation, a, b, c, d);
        if (!strcmp(operation, "UPDATE") && fields == 4) strcpy(values[groups[position(a,b)]], c);
        else if (!strcmp(operation, "UPDATE")) { for (int i = 0; i < 2500; ++i) if (!strcmp(values[i], a)) strcpy(values[i], b); }
        else if (!strcmp(operation, "MERGE")) {
            int first = groups[position(a,b)], second = groups[position(c,d)]; if (first == second) continue;
            if (!values[first][0]) strcpy(values[first], values[second]);
            for (int i = 0; i < 2500; ++i) if (groups[i] == second) groups[i] = first;
            values[second][0] = '\0';
        } else if (!strcmp(operation, "UNMERGE")) {
            int cell = position(a,b), group = groups[cell]; char kept[51]; strcpy(kept, values[group]);
            for (int i = 0; i < 2500; ++i) if (groups[i] == group) { groups[i] = i; values[i][0] = '\0'; }
            strcpy(values[cell], kept);
        } else {
            const char* value = values[groups[position(a,b)]]; if (!value[0]) value = "EMPTY";
            answer[count] = malloc(strlen(value) + 1); strcpy(answer[count++], value);
        }
    }
    free(values);
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
// static int position(const char* r, const char* c) { return (atoi(r) - 1) * 50 + atoi(c) - 1; }  // 행·열을 0부터 시작하는 50열 셀 번호로 변환
// char** solution(const char* commands[], size_t commands_len) {  // 2500칸뿐이므로 각 셀에 그룹 번호를 직접 저장하고 병합·해제 때 전체를 순회; 값은 그룹 대표 한 곳에만 두기
//     int groups[2500]; char (*values)[51] = calloc(2500, sizeof(*values));  // 각 셀의 그룹 번호와 대표 셀의 문자열 공간 만들기
//     for (int i = 0; i < 2500; ++i) groups[i] = i;  // 처음에는 각 셀이 자기 자신만 속한 그룹
//     char** answer = malloc(commands_len * sizeof(*answer)); size_t count = 0;  // PRINT 결과를 담을 포인터 배열과 출력 개수 초기화
//     for (size_t index = 0; index < commands_len; ++index) {  // 처리할 명령 위치 순서대로 확인
//         char operation[16], a[51], b[51], c[51], d[51];  // 명령 이름과 최대 네 인수를 읽을 버퍼
//         int fields = sscanf(commands[index], "%15s %50s %50s %50s %50s", operation, a, b, c, d);  // 명령과 인수를 나누고 읽은 항목 수로 UPDATE 두 형식 구분
//         if (!strcmp(operation, "UPDATE") && fields == 4) strcpy(values[groups[position(a,b)]], c);  // 좌표 UPDATE는 그 셀이 속한 그룹 대표의 값 변경
//         else if (!strcmp(operation, "UPDATE")) { for (int i = 0; i < 2500; ++i) if (!strcmp(values[i], a)) strcpy(values[i], b); }  // 값 UPDATE는 기존 값과 같은 모든 그룹 대표의 문자열 변경
//         else if (!strcmp(operation, "MERGE")) {  // 두 셀의 그룹을 하나로 합치기
//             int first = groups[position(a,b)], second = groups[position(c,d)]; if (first == second) continue;  // 두 셀의 대표를 찾고 이미 같은 그룹이면 건너뛰기
//             if (!values[first][0]) strcpy(values[first], values[second]);  // 첫 셀 그룹에 값이 없을 때만 둘째 그룹의 값 가져오기
//             for (int i = 0; i < 2500; ++i) if (groups[i] == second) groups[i] = first;  // 둘째 그룹의 모든 셀을 첫 그룹으로 옮기기
//             values[second][0] = '\0';  // 흡수된 둘째 대표에 남은 문자열 비우기
//         } else if (!strcmp(operation, "UNMERGE")) {  // 그 외에는 UNMERGE 명령이면 처리
//             int cell = position(a,b), group = groups[cell]; char kept[51]; strcpy(kept, values[group]);  // 해제할 셀의 값은 그룹을 풀기 전에 따로 보관
//             for (int i = 0; i < 2500; ++i) if (groups[i] == group) { groups[i] = i; values[i][0] = '\0'; }  // 해제할 그룹의 셀을 각각 자기 그룹으로 돌리고 값 비우기
//             strcpy(values[cell], kept);  // 해제 후 지정한 셀 하나에만 원래 그룹 값 복원
//         } else {  // PRINT는 지정 셀의 그룹 값 출력
//             const char* value = values[groups[position(a,b)]]; if (!value[0]) value = "EMPTY";  // 출력할 그룹 값을 찾고 빈 값이면 EMPTY 선택
//             answer[count] = malloc(strlen(value) + 1); strcpy(answer[count++], value);  // PRINT 문자열을 별도 메모리에 복사하고 출력 개수 늘리기
//         }  // 이 범위 끝
//     }  // 이 범위 끝
//     free(values);  // 그룹 대표에 저장한 문자열 임시 공간 정리
//     return answer;  // PRINT 출력 목록 반환
// }  // 이 범위 끝

// 풀이 요약
// 2500칸뿐이므로 각 셀에 그룹 번호를 직접 저장하고 병합·해제 때 전체를 순회; 값은 그룹 대표 한 곳에만 두기
// MERGE는 첫 셀 값이 있으면 우선하기; UNMERGE는 모든 소속 셀을 초기화한 후 지정 셀 하나만 값을 남기기; 명령 Q개에 대해 시간 O(2500Q), 공간 O(2500+출력 수)
// 예: a와 b가 있는 두 셀을 첫 셀 우선으로 병합하면 모두 a.; 둘째 셀에서 해제하면 첫 셀은 EMPTY, 둘째 셀만 a
