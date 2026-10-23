int solution(int n) {
    if (n % 2) return 0;
    const long long MOD = 1000000007;
    long long previous = 1, current = 3;
    for (int width = 4; width <= n; width += 2) {
        long long next = (4 * current - previous + MOD) % MOD;
        previous = current; current = next;
    }
    return (int)current;
}

// 전체 코드 줄별 설명
// int solution(int n) {  // 짝수 너비의 3행 타일링 점화식 계산
// if (n % 2) return 0;  // 너비가 홀수이면 3×n 영역을 채울 수 없음
// const long long MOD = 1000000007;  // 결과의 나머지 기준 선언
// long long previous = 1, current = 3;  // 너비 0과 2의 타일링 수 초기화
// for (int width = 4; width <= n; width += 2) {  // 짝수 너비의 점화식을 순서대로 적용
// long long next = (4 * current - previous + MOD) % MOD;  // 이전 두 짝수 너비로 다음 경우의 수 계산
// previous = current; current = next;  // 다음 너비 계산에 쓸 두 값 갱신
// }  // 블록 끝
// return (int)current;  // 3×n 타일링 수의 나머지 반환
// }  // 블록 끝

// 풀이 요약
// 짝수 너비에서 앞선 두 짝수 너비의 경우의 수를 4배와 뺄셈으로 연결하는 점화식 적용
