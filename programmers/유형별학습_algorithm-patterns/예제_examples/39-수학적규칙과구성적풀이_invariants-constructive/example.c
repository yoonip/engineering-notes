#include <stdio.h>  // 표준 입력과 숫자·문자열 출력 함수
#include <stdlib.h>  // qsort와 정수 절댓값 함수
static int read_int(void) {  // 다음 정수 하나를 읽는 공통 함수
    int value = 0;  // 입력값을 받을 정수
    scanf("%d", &value);  // 공백을 건너뛰고 정수 읽기
    return value;  // 읽은 값 전달
}  // 정수 입력 함수 끝
static void write_number(int value) {  // 정수 한 개를 출력하는 공통 함수
    printf("%d", value);  // 불필요한 공백 없이 정수 출력
}  // 정수 출력 함수 끝
static void write_text(const char *text) {  // 구분자나 결과 문구 출력
    fputs(text, stdout);  // 문자열을 표준 출력에 그대로 쓰기
}  // 문자열 출력 함수 끝


int main(void) {  // 불변량 검사 후 실제 증가 연산 구성
    int n = read_int(), initial[6], deficit[6];  // 배열 길이·초기값·남은 부족량
    for (int i = 0; i < n; ++i) initial[i] = read_int();  // 초기 배열 입력
    int total = 0, largest = 0, possible = 1;  // 부족량 합·최댓값·가능 여부
    for (int i = 0; i < n; ++i) {  // 목표와의 차이 계산
        deficit[i] = read_int() - initial[i];  // 이 위치에서 더해야 할 양
        if (deficit[i] < 0) possible = 0;  // 감소 연산이 없으므로 음수 차이는 불가능
        total += deficit[i];  // 한 연산이 2 줄일 총부족량
        if (deficit[i] > largest) largest = deficit[i];  // 한 위치의 최대 부족량
    }  // 부족량 집계 끝
    if (!possible || total % 2 || 2 * largest > total) { write_text("IMPOSSIBLE\n"); return 0; }  // 다른 위치와 짝지을 수 있는 조건 검사
    int steps = total / 2;  // 모든 연산은 합을 정확히 2 올림
    write_text("POSSIBLE "); write_number(steps); write_text("\n");  // 구성할 연산 수 먼저 출력
    for (int step = 0; step < steps; ++step) {  // 부족량이 모두 0이 될 때까지 구성
        int first = -1, second = -1;  // 가장 큰 두 부족량의 위치
        for (int i = 0; i < n; ++i) {  // 작은 인덱스부터 동률 처리
            if (first == -1 || deficit[i] > deficit[first]) { second = first; first = i; }  // 새 최댓값을 첫 후보로
            else if (second == -1 || deficit[i] > deficit[second]) second = i;  // 나머지 중 두 번째 후보
        }  // 서로 다른 두 위치 선택 끝
        --deficit[first]; --deficit[second];  // 선택한 두 위치의 목표 부족량을 1씩 줄이기
        write_number(first); write_text(" "); write_number(second); write_text("\n");  // 실제 증가 연산 출력
    }  // 목표까지의 구성 끝
    return 0;  // 정상 종료
}  // 불변량·구성 예제 끝
