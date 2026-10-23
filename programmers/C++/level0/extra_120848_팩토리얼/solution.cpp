#include <string>
#include <vector>
#include <algorithm>
#include <numeric>
#include <cmath>
#include <sstream>
#include <climits>
#include <cctype>
#include <iostream>
#include <functional>

using namespace std;

int solution(int n) {
    int factorial = 1, answer = 1;
    while (factorial <= n / (answer + 1)) factorial *= ++answer;
    return answer;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 다룰 string
// #include <vector>  // 길이를 늘릴 수 있는 vector
// #include <algorithm>  // 정렬·검색·뒤집기 알고리즘
// #include <numeric>  // accumulate·iota 등 수치 연산
// #include <cmath>  // 제곱근 등 수학 함수
// #include <sstream>  // 문자열을 항목별로 읽을 스트림
// #include <climits>  // INT_MIN·INT_MAX 등 정수 범위 상수
// #include <cctype>  // 문자 검사와 대소문자 변환
// #include <iostream>  // cin·cout 표준 입출력
// #include <functional>  // greater·multiplies 등 함수 객체
//
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// int solution(int n) {  // 팩토리얼 풀이 시작
//     int factorial = 1, answer = 1;  // 현재 팩토리얼 값과 그 값에 해당하는 정수 i
//     while (factorial <= n / (answer + 1)) factorial *= ++answer;  // 다음 팩토리얼이 n을 넘지 않는 동안 반복하며 정수 나눗셈으로 곱셈 오버플로를 피
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 다음 팩토리얼이 n을 넘지 않을 때만 정수 i를 증가
