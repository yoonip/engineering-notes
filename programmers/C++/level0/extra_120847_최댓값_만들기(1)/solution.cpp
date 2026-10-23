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
    sort(numbers.begin(), numbers.end(), greater<int>());
    return numbers[0] * numbers[1];
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
// int solution(vector<int> numbers) {  // 최댓값 만들기(1) 풀이 시작
//     sort(numbers.begin(), numbers.end(), greater<int>());  // 정렬 함수와 greater 비교자로 배열을 내림차순으로 정렬
//     return numbers[0] * numbers[1];  // 내림차순으로 정렬한 가장 큰 두 원소의 곱
// }  // 블록 끝

// 풀이 요약
// 모든 수가 0 이상이므로 가장 큰 두 원소의 곱이 최대임
