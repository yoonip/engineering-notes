int solution(int number, int n, int m) {
    return number % n == 0 && number % m == 0;
}

// 전체 코드 줄별 설명
// int solution(int number, int n, int m) {  // 공배수 풀이 시작
//     return number % n == 0 && number % m == 0;  // %와 ==로 두 배수 조건을 검사하고 &&로 모두 참인지 확인
// }  // 블록 끝

// 풀이 요약
// number가 n과 m 모두로 나누어떨어지는지 확인
