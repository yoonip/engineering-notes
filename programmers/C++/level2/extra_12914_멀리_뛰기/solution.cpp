long long solution(int n) {
    long long previous = 1, current = 1;
    for (int i = 2; i <= n; ++i) {
        long long next = (previous + current) % 1234567;
        previous = current; current = next;
    }
    return current;
}

// 전체 코드 줄별 설명
// long long solution(int n) {  // 마지막 한 칸·두 칸 점프의 경우의 수 합치기
// long long previous = 1, current = 1;  // 길이 0과 1을 이동하는 방법 수 초기화
// for (int i = 2; i <= n; ++i) {  // 마지막에 한 칸 또는 두 칸 뛰는 두 경우 합치기
// long long next = (previous + current) % 1234567;  // 이전 두 길이의 방법 수를 더해 나머지 구하기
// previous = current; current = next;  // 연속한 두 길이의 방법 수 갱신
// }  // 블록 끝
// return current;  // n칸을 이동하는 방법 수의 나머지 반환
// }  // 블록 끝

// 풀이 요약
// 마지막에 한 칸 또는 두 칸 뛰는 두 경우의 수를 이전 두 길이의 점화식으로 더하기
