int solution(int a, int b, int c) {
    int answer = a + b + c;
    if (a == b || b == c || a == c) answer *= a * a + b * b + c * c;
    if (a == b && b == c) answer *= a * a * a + b * b * b + c * c * c;
    return answer;
}

// 전체 코드 줄별 설명
// int solution(int a, int b, int c) {  // 주사위 게임 2 풀이 시작
//     int answer = a + b + c;  // 세 주사위 눈의 합으로 기본 점수를 초기화
//     if (a == b || b == c || a == c) answer *= a * a + b * b + c * c;  // ||로 같은 눈이 있는지 검사하고 *=로 제곱의 합을 점수에 곱하기
//     if (a == b && b == c) answer *= a * a * a + b * b * b + c * c * c;  // &&로 세 눈이 모두 같은지 검사하고 *=로 세제곱의 합을 점수에 곱하기
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 같은 눈의 수에 따라 1차 합에 제곱 합과 세제곱 합을 차례대로 곱하기
