int solution(int n) {
    int previous = 0, current = 1;
    for (int i = 0; i < n; ++i) {
        int next = (previous + current) % 1234567;
        previous = current; current = next;
    }
    return previous;
}

// 전체 코드 줄별 설명
// int solution(int n) {  // 이전 두 피보나치 값만 남기며 다음 항 계산
// int previous = 0, current = 1;  // F(0)과 F(1)을 초기값으로 두기
// for (int i = 0; i < n; ++i) {  // 피보나치 항을 n번 앞으로 이동
// int next = (previous + current) % 1234567;  // 두 항의 합을 나머지로 줄여 다음 항 구하기
// previous = current; current = next;  // 연속한 두 항을 다음 위치로 갱신
// }  // 블록 끝
// return previous;  // F(n)의 나머지 반환
// }  // 블록 끝

// 풀이 요약
// 연속한 두 피보나치 항만 유지하며 합의 나머지를 다음 항으로 계산
