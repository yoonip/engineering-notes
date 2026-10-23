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

int solution(vector<int> common) {
    if (common[1] - common[0] == common[2] - common[1]) return common.back() + common[1] - common[0];
    return common.back() * (common[1] / common[0]);
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
// int solution(vector<int> common) {  // 다음에 올 숫자 풀이 시작
//     if (common[1] - common[0] == common[2] - common[1]) return common.back() + common[1] - common[0];  // if 조건이 참이면 지정한 결과를 즉시 반환하여 함수 실행을 끝
//     return common.back() * (common[1] / common[0]);  // 등비수열이면 마지막 항에 공비를 곱한 다음 항
// }  // 블록 끝

// 풀이 요약
// 앞 세 항의 차이가 같으면 등차수열이고, 아니면 등비수열임
