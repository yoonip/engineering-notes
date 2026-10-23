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

int solution(int price) {
    int percent = price >= 500000 ? 80 : price >= 300000 ? 90 : price >= 100000 ? 95 : 100;
    return price * percent / 100;
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
// int solution(int price) {  // 옷가게 할인 받기 풀이 시작
//     int percent = price >= 500000 ? 80 : price >= 300000 ? 90 : price >= 100000 ? 95 : 100;  // 큰 금액 구간부터 검사해 할인 후 지불 비율 선택
//     return price * percent / 100;  // 정수 나눗셈으로 할인 후 금액의 소수 부분 버리기
// }  // 블록 끝

// 풀이 요약
// 50만·30만·10만 원 구간에 맞는 지불 비율을 고른 뒤 정수 연산으로 최종 금액 계산
