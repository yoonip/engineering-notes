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

int solution(vector<int> numbers) {
    sort(numbers.begin(), numbers.end());
    size_t n = numbers.size();
    return max(numbers[0] * numbers[1], numbers[n - 1] * numbers[n - 2]);
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
// int solution(vector<int> numbers) {  // 최댓값 만들기 (2) 풀이 시작
//     sort(numbers.begin(), numbers.end());  // numbers를 오름차순 정렬
//     size_t n = numbers.size();  // n에 numbers의 길이 저장
//     return max(numbers[0] * numbers[1], numbers[n - 1] * numbers[n - 2]);  // 가장 작은 두 수의 곱과 가장 큰 두 수의 곱 중 큰 값
// }  // 블록 끝

// 풀이 요약
// 큰 양수 두 개 또는 절댓값이 큰 음수 두 개의 곱이 최대 후보임
