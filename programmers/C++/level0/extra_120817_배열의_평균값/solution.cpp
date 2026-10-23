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

double solution(vector<int> numbers) {
    return accumulate(numbers.begin(), numbers.end(), 0.0) / numbers.size();
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
// double solution(vector<int> numbers) {  // 배열의 평균값 풀이 시작
//     return accumulate(numbers.begin(), numbers.end(), 0.0) / numbers.size();  // 합을 실수로 누적한 뒤 원소 수로 나눠 평균 계산
// }  // 블록 끝

// 풀이 요약
// 평균은 전체 합을 원소 개수로 나눈 값임
