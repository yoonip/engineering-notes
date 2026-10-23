#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <limits.h>

int solution(int n, int m, int section[], size_t section_len) {
    int answer = 0, painted_until = 0;
    for (size_t i = 0; i < section_len; ++i) if (section[i] > painted_until) {
        ++answer; int start = section[i] < n - m + 1 ? section[i] : n - m + 1; painted_until = start + m - 1;
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
// int solution(int n, int m, int section[], size_t section_len) {  // 현재 칠한 마지막 위치보다 뒤에 있는 미도색 구간을 만날 때만 롤러를 한 번 사용; 가능한 오른쪽까지 함께 칠하기
//     int answer = 0, painted_until = 0;  // 롤러를 놓은 횟수 / 마지막으로 칠한 구간의 오른쪽 끝 저장
//     for (size_t i = 0; i < section_len; ++i) if (section[i] > painted_until) {  // 아직 칠하지 않은 구역을 만나면 이 위치부터 롤러 놓기
//         ++answer; int start = section[i] < n - m + 1 ? section[i] : n - m + 1; painted_until = start + m - 1;  // 롤러 횟수를 늘리고 벽을 넘지 않는 시작점에서 칠한 끝점 기록
//     }  // 이 범위 끝
//     return answer;  // 롤러를 놓은 횟수 반환
// }  // 이 범위 끝

// 풀이 요약
// 현재 칠한 마지막 위치보다 뒤에 있는 미도색 구간을 만날 때만 롤러를 한 번 사용; 가능한 오른쪽까지 함께 칠하기
