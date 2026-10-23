#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <limits.h>

int solution(int n, int w, int num) {
    int row = (num - 1) / w, col = (num - 1) % w, answer = 0;
    if (row % 2) col = w - 1 - col;
    for (int r = row; r < (n + w - 1) / w; ++r) {
        int box = r % 2 == 0 ? r * w + col + 1 : (r + 1) * w - col;
        if (box <= n) ++answer;
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
// int solution(int n, int w, int num) {  // 상자가 놓인 행의 홀짝으로 실제 열을 계산; 같은 열의 위쪽 행에서 존재하는 상자 수를 세기
//     int row = (num - 1) / w, col = (num - 1) % w, answer = 0;  // 꺼낼 상자의 층 / 꺼낼 상자의 실제 열 / 위에서 꺼내야 할 상자 수 저장
//     if (row % 2) col = w - 1 - col;  // 홀수 층은 적재 방향이 반대이므로 실제 열 좌표 뒤집기
//     for (int r = row; r < (n + w - 1) / w; ++r) {  // 같은 열에서 확인할 층 순서대로 확인
//         int box = r % 2 == 0 ? r * w + col + 1 : (r + 1) * w - col;  // 현재 층 같은 열의 상자 번호 저장
//         if (box <= n) ++answer;  // 그 위치의 상자 번호가 n 이하이면 실제 상자가 있으므로 개수에 추가
//     }  // 이 범위 끝
//     return answer;  // 위에서 꺼내야 할 상자 수 반환
// }  // 이 범위 끝

// 풀이 요약
// 상자가 놓인 행의 홀짝으로 실제 열을 계산; 같은 열의 위쪽 행에서 존재하는 상자 수를 세기
