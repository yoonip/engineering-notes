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

vector<vector<int>> solution(vector<vector<int>> arr) {
    size_t n = max(arr.size(), arr[0].size());
    for (auto& row : arr) row.resize(n, 0);
    arr.resize(n, vector<int>(n, 0));
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
// vector<vector<int>> solution(vector<vector<int>> arr) {  // 정사각형으로 만들기 풀이 시작
//     size_t n = max(arr.size(), arr[0].size());  // 행 수와 열 수 중 큰 쪽을 정사각형의 한 변으로 선택
//     for (auto& row : arr) row.resize(n, 0);  // 각 행의 부족한 열을 0으로 채우기
//     arr.resize(n, vector<int>(n, 0));  // 행이 부족하면 전부 0인 새 행 추가
//     return arr;  // 원래 원소를 유지한 n×n 정사각형
// }  // 블록 끝

// 풀이 요약
// 행 수와 열 수 중 큰 길이에 맞춰 부족한 열과 행만 0으로 채우기
