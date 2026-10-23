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
    for (int r = 1; r <= n / r; ++r) if (r * r == n) return 1;
    return 2;
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
// int solution(int n) {  // 제곱수 판별하기 풀이 시작
//     for (int r = 1; r <= n / r; ++r) if (r * r == n) return 1;  // 제곱근 이하의 양의 정수를 검사해 제곱이 n이면 성공
//     return 2;  // 제곱해서 n이 되는 양의 정수가 없음
// }  // 블록 끝

// 풀이 요약
// 1부터 제곱근 이하까지 후보를 검사. 후보의 제곱이 n인 경우 1, 끝까지 없으면 2
