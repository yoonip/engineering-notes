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

vector<int> solution(vector<int> arr, int n) {
    for (size_t i = arr.size() % 2 ? 0 : 1; i < arr.size(); i += 2) arr[i] += n;
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
// vector<int> solution(vector<int> arr, int n) {  // 배열의 길이에 따라 다른 연산하기 풀이 시작
//     for (size_t i = arr.size() % 2 ? 0 : 1; i < arr.size(); i += 2) arr[i] += n;  // 길이가 홀수면 짝수 인덱스, 짝수면 홀수 인덱스에 n 추가
//     return arr;  // 길이의 홀짝에 맞는 위치만 바꾼 배열
// }  // 블록 끝

// 풀이 요약
// 길이의 홀짝에 맞는 시작 인덱스를 정하고 두 칸씩 이동
