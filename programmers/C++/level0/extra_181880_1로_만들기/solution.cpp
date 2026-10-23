#include <string>
#include <vector>
#include <algorithm>
#include <numeric>
#include <functional>
#include <unordered_set>
#include <sstream>
#include <cctype>
#include <cstdlib>
using namespace std;

int solution(vector<int> num_list) {
    int count = 0;
    for (int value : num_list) while (value > 1) { value /= 2; ++count; }
    return count;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 다룰 string
// #include <vector>  // 길이를 늘릴 수 있는 vector
// #include <algorithm>  // 정렬·검색·뒤집기 알고리즘
// #include <numeric>  // accumulate·iota 등 수치 연산
// #include <functional>  // greater·multiplies 등 함수 객체
// #include <unordered_set>  // 중복을 거를 해시 집합
// #include <sstream>  // 문자열을 항목별로 읽을 스트림
// #include <cctype>  // 문자 검사와 대소문자 변환
// #include <cstdlib>  // 정수 변환과 절댓값 등 표준 함수
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// int solution(vector<int> num_list) {  // 1로 만들기 풀이 시작
//     int count = 0;  // 모든 원소를 1로 만들 때의 총 나눗셈 횟수
//     for (int value : num_list) while (value > 1) { value /= 2; ++count; }  // 각 원소를 정수로 절반씩 줄이며 1이 될 때까지 횟수 추가
//     return count;  // 조건을 만족한 횟수 값을 반환하고 함수를 끝
// }  // 블록 끝

// 풀이 요약
// 양수의 정수 나눗셈은 홀수의 나머지도 버리므로, 짝수·홀수 모두 / 2로 다음 값을 구해 1까지의 횟수 합산
