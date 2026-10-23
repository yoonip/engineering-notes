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

int solution(vector<int> array) {
    int answer = 0;
    for (int value : array)
        for (char digit : to_string(value)) answer += digit == '7';
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
// int solution(vector<int> array) {  // 7의 개수 풀이 시작
//     int answer = 0;  // 모든 정수의 자릿수에 나타난 7의 개수
//     for (int value : array)  // 배열의 정수를 하나씩 숫자 문자열로 바꾸기
//         for (char digit : to_string(value)) answer += digit == '7';  // 숫자 문자가 7일 때마다 하나씩 세기
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 각 정수를 문자열로 바꿔 숫자 문자 7의 출현 횟수를 세기
