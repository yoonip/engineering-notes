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

vector<int> solution(vector<int> array) {
    auto position = max_element(array.begin(), array.end());
    return {*position, static_cast<int>(position - array.begin())};
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
// vector<int> solution(vector<int> array) {  // 가장 큰 수 찾기 풀이 시작
//     auto position = max_element(array.begin(), array.end());  // max_element로 배열 전체에서 최댓값이 있는 위치를 찾기. auto는 반환된 반복자의 자료형을 추론하여 position에 저장
//     return {*position, static_cast<int>(position - array.begin())};  // 찾은 최댓값과 시작 반복자부터의 거리인 인덱스를 함께 반환
// }  // 블록 끝

// 풀이 요약
// max_element로 최댓값의 반복자를 구하기. 반복자의 값과 배열 시작으로부터의 거리를 각각 최댓값과 0부터 시작하는 인덱스로 반환
