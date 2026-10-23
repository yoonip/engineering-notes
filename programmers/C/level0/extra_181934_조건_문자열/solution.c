int solution(const char* ineq, const char* eq, int n, int m) {
    if (n == m) return eq[0] == '=';
    return ineq[0] == '>' ? n > m : n < m;
}

// 전체 코드 줄별 설명
// int solution(const char* ineq, const char* eq, int n, int m) {  // 조건 문자열 풀이 시작
//     if (n == m) return eq[0] == '=';  // if로 두 수가 같은지 검사하고 eq의 첫 문자가 등호인지 반환
//     return ineq[0] == '>' ? n > m : n < m;  // 삼항 연산자 ?:로 부등호 방향에 맞는 대소 비교 결과를 반환
// }  // 블록 끝

// 풀이 요약
// 같은 값일 때 등호 허용 여부를 확인하고, 다른 값은 부등호 방향에 맞게 비교
