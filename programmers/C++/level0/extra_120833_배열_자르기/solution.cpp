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

vector<int> solution(vector<int> numbers, int num1, int num2) {
    return vector<int>(numbers.begin() + num1, numbers.begin() + num2 + 1);
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
// vector<int> solution(vector<int> numbers, int num1, int num2) {  // 배열 자르기 풀이 시작
//     return vector<int>(numbers.begin() + num1, numbers.begin() + num2 + 1);  // 구간 생성자는 시작 반복자를 포함하고 끝 반복자는 제외하므로, begin() + num1부터 begin() + num2 + 1까지의 원소로 새 vector를 만들어 반환
// }  // 블록 끝

// 풀이 요약
// vector의 구간 생성자에 num1 위치부터 num2 바로 다음 위치까지를 전달하여, 양 끝 인덱스가 모두 포함된 새 배열을 만들기
