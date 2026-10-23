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

vector<int> solution(vector<int> num_list) {
    vector<int> answer(2);
    for (int value : num_list) ++answer[value % 2];
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
// vector<int> solution(vector<int> num_list) {  // 짝수 홀수 개수 풀이 시작
//     vector<int> answer(2);  // 인덱스 0은 짝수 개수, 1은 홀수 개수
//     for (int value : num_list) ++answer[value % 2];  // 2로 나눈 나머지를 이용해 짝수·홀수 개수를 나눠 증가
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 각 값을 2로 나눈 나머지로 짝수와 홀수를 구분. 결과의 첫 칸은 짝수 개수, 둘째 칸은 홀수 개수
