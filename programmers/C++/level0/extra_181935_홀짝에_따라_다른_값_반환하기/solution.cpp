int solution(int n) {
    int answer = 0;
    for (int i = n % 2 ? 1 : 2; i <= n; i += 2) answer += n % 2 ? i : i * i;
    return answer;
}

// 전체 코드 줄별 설명
// int solution(int n) {  // 홀짝에 따라 다른 값 반환하기 풀이 시작
//     int answer = 0;  // int형 합계를 0으로 초기화
//     for (int i = n % 2 ? 1 : 2; i <= n; i += 2) answer += n % 2 ? i : i * i;  // for에서 홀짝에 맞는 시작값부터 2씩 증가시키고 삼항 연산자로 원소 또는 제곱을 더하기
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// n이 홀수이면 홀수의 합을, 짝수이면 짝수 제곱의 합을 구하기
