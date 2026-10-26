#include <iostream>  // cin과 cout으로 표준 입력·출력 처리
#include <cstdlib>  // qsort와 정수 절댓값 함수
using namespace std;  // 작은 예제에서 표준 라이브러리 이름을 짧게 사용
static int read_int(void) {  // 다음 정수 하나를 읽는 공통 함수
    int value = 0;  // 입력값을 받을 정수
    cin >> value;  // 스트림에서 정수 읽기
    return value;  // 읽은 값 전달
}  // 정수 입력 함수 끝
static void write_number(int value) {  // 정수 한 개를 출력하는 공통 함수
    cout << value;  // 불필요한 공백 없이 정수 출력
}  // 정수 출력 함수 끝
static void write_text(const char *text) {  // 구분자나 결과 문구 출력
    cout << text;  // 문자열을 스트림에 그대로 쓰기
}  // 문자열 출력 함수 끝


int main(void) {  // 서로 다른 두 구조로 최대 부분합 비교
    int n = read_int(), values[10];  // 배열 길이와 작은 검산 입력
    for (int i = 0; i < n; ++i) values[i] = read_int();  // 정수 배열 입력
    int slow = -1000000000;  // 모든 허용 합보다 작은 초기값
    for (int left = 0; left < n; ++left) {  // 부분배열 시작점 열거
        for (int right = left; right < n; ++right) {  // 비어 있지 않은 끝점 열거
            int total = 0;  // 매 구간을 처음부터 독립 계산
            for (int i = left; i <= right; ++i) total += values[i];  // 정의대로 모든 원소를 직접 합산
            if (total > slow) slow = total;  // 느린 기준의 최대합 갱신
        }  // 현재 시작점의 구간 비교 끝
    }  // 모든 비어 있지 않은 구간 검사 끝
    int current = values[0], fast = values[0];  // 첫 원소로 끝나는 최적합과 전체 최적합
    for (int i = 1; i < n; ++i) {  // 이후 원소를 한 번씩 추가
        current = current + values[i] > values[i] ? current + values[i] : values[i];  // 이전 구간을 잇거나 현재 값에서 새로 시작
        if (current > fast) fast = current;  // 전체 최적합 갱신
    }  // Kadane 단일 순회 끝
    write_number(slow); write_text(" "); write_number(fast); write_text("\n");  // 독립 결과를 나란히 출력
    return 0;  // 정상 종료
}  // 차등 비교 예제 끝
