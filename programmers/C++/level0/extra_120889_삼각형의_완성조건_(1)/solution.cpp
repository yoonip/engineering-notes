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

int solution(vector<int> sides) {
    int total = accumulate(sides.begin(), sides.end(), 0);
    return total > 2 * *max_element(sides.begin(), sides.end()) ? 1 : 2;
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
// int solution(vector<int> sides) {  // 삼각형의 완성조건 (1) 풀이 시작
//     int total = accumulate(sides.begin(), sides.end(), 0);  // accumulate로 sides의 모든 원소를 초기값 0에 더하여 세 변의 합 total을 구하기
//     return total > 2 * *max_element(sides.begin(), sides.end()) ? 1 : 2;  // max_element의 반복자를 *로 역참조하여 가장 긴 변을 읽기. 전체 합이 최장 변의 2배보다 커야 나머지 두 변의 합이 최장 변보다 크므로, 삼항 연산자로 1 또는 2를 반환
// }  // 블록 끝

// 풀이 요약
// 세 변의 합이 가장 긴 변의 두 배보다 큰지 확인. 이는 나머지 두 변의 합이 가장 긴 변보다 커야 한다는 삼각형 조건과 같음
