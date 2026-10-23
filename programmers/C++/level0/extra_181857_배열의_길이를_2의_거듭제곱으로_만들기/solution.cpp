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

vector<int> solution(vector<int> arr) {
    size_t length = 1;
    while (length < arr.size()) length *= 2;
    arr.resize(length, 0);
    return arr;
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
// vector<int> solution(vector<int> arr) {  // 배열의 길이를 2의 거듭제곱으로 만들기 풀이 시작
//     size_t length = 1;  // 늘릴 길이의 후보인 가장 작은 2의 거듭제곱
//     while (length < arr.size()) length *= 2;  // 원래 길이 이상이 될 때까지 후보 길이를 두 배씩 증가
//     arr.resize(length, 0);  // 원소는 유지하고 새로 늘어난 뒷부분만 0으로 채우기
//     return arr;  // 길이가 2의 거듭제곱이 된 배열
// }  // 블록 끝

// 풀이 요약
// 현재 길이 이상인 가장 작은 2의 거듭제곱을 찾고 그 차이만큼 0을 추가
