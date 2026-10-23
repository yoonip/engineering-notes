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

vector<int> solution(vector<int> numbers, string direction) {
    if (direction == "right") rotate(numbers.begin(), numbers.end() - 1, numbers.end());
    else rotate(numbers.begin(), numbers.begin() + 1, numbers.end());
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
// vector<int> solution(vector<int> numbers, string direction) {  // 배열 회전시키기 풀이 시작
//     if (direction == "right") rotate(numbers.begin(), numbers.end() - 1, numbers.end());  // rotate는 지정한 중간 위치의 원소가 맨 앞에 오도록 구간을 회전
//     else rotate(numbers.begin(), numbers.begin() + 1, numbers.end());  // rotate는 지정한 중간 위치의 원소가 맨 앞에 오도록 구간을 회전
//     return numbers;  // 지정된 방향으로 한 칸 회전한 배열
// }  // 블록 끝

// 풀이 요약
// 회전 방향에 따라 끝 원소를 앞으로 또는 첫 원소를 뒤로 옮기기
