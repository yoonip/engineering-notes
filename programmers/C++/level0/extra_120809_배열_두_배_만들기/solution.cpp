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

vector<int> solution(vector<int> numbers) {
    for (int& value : numbers) value *= 2;
    return numbers;
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
// vector<int> solution(vector<int> numbers) {  // 배열 두 배 만들기 풀이 시작
//     for (int& value : numbers) value *= 2;  // 범위 기반 for문으로 numbers의 원소를 int& 참조 value에 연결. 복합 대입 연산자 *=로 각 원소 자체를 두 배로 바꾸기
//     return numbers;  // 모든 원소가 두 배로 바뀐 numbers를 반환
// }  // 블록 끝

// 풀이 요약
// 범위 기반 for문으로 입력 vector의 각 원소를 참조하여 두 배로 바꾼 뒤 그 vector를 반환
