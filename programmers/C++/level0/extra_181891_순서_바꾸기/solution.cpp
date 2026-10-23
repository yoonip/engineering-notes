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

vector<int> solution(vector<int> num_list, int n) {
    rotate(num_list.begin(), num_list.begin() + n, num_list.end());
    return num_list;
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
// vector<int> solution(vector<int> num_list, int n) {  // 순서 바꾸기 풀이 시작
//     rotate(num_list.begin(), num_list.begin() + n, num_list.end());  // rotate로 앞 n개 원소를 뒤로 옮기고 나머지를 앞으로 이동
//     return num_list;  // 앞 n개를 뒤로 옮긴 배열 반환
// }  // 블록 끝

// 풀이 요약
// 앞 n개와 나머지로 나누고 두 묶음의 순서를 바꾸기
