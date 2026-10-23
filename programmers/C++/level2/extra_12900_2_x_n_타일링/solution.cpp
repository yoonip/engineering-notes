int solution(int n) {
    const int MOD = 1000000007;
    int previous = 1, current = 1;
    for (int width = 2; width <= n; ++width) {
        int next = (previous + current) % MOD;
        previous = current; current = next;
    }
    return current;
}

// 전체 코드 줄별 설명
// int solution(int n) {  // 마지막 배치 두 경우로 2행 타일링 수 계산
// const int MOD = 1000000007;  // 결과의 나머지 기준 선언
// int previous = 1, current = 1;  // 너비 0과 1의 타일링 수 초기화
// for (int width = 2; width <= n; ++width) {  // 마지막에 세로 한 개 또는 가로 두 개를 두는 경우 합치기
// int next = (previous + current) % MOD;  // 이전 두 너비의 경우의 수를 더하기
// previous = current; current = next;  // 연속한 두 너비의 값 갱신
// }  // 블록 끝
// return current;  // 2×n 타일링 수의 나머지 반환
// }  // 블록 끝

// 풀이 요약
// 마지막 타일 배치에 따라 이전 두 너비의 타일링 수를 더하는 점화식 적용
