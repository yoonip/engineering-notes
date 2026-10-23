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

string solution(string cipher, int code) {
    string answer;
    for (size_t i = code - 1; i < cipher.size(); i += code) answer += cipher[i];
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
// string solution(string cipher, int code) {  // 암호 해독 풀이 시작
//     string answer;  // string 변수 answer를 빈 문자열로 초기화하여 code의 배수 번째 문자들을 순서대로 붙이기
//     for (size_t i = code - 1; i < cipher.size(); i += code) answer += cipher[i];  // for의 첫 인덱스를 code - 1로 정. i를 code씩 늘리며 문자열 범위 안의 cipher[i]를 붙여, 1부터 센 위치 code, 2 * code, 3 * code의 문자들을 선택
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 0부터 시작하는 인덱스 code - 1에서 출발해 code씩 증가. 1부터 센 위치가 code의 배수인 문자들을 순서대로 모읍니다
