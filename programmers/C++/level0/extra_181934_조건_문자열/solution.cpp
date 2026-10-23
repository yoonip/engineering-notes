#include <string>
using namespace std;

int solution(string ineq, string eq, int n, int m) {
    if (n == m) return eq == "=";
    return ineq == ">" ? n > m : n < m;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 다룰 string
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// int solution(string ineq, string eq, int n, int m) {  // 조건 문자열 풀이 시작
//     if (n == m) return eq == "=";  // if로 두 수가 같은지 검사하고 eq가 등호 문자열인지 반환
//     return ineq == ">" ? n > m : n < m;  // 삼항 연산자 ?:로 부등호 방향에 맞는 대소 비교 결과를 반환
// }  // 블록 끝

// 풀이 요약
// 같은 값일 때 등호 허용 여부를 확인하고, 다른 값은 부등호 방향에 맞게 비교
