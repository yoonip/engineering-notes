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

vector<int> solution(vector<int> arr, vector<vector<int>> queries) {
    for (const auto& q : queries)
        for (int i = q[0]; i <= q[1]; ++i) ++arr[i];
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
// vector<int> solution(vector<int> arr, vector<vector<int>> queries) {  // 수열과 구간 쿼리 1 풀이 시작
//     for (const auto& q : queries)  // 입력된 구간 쿼리를 순서대로 적용
//         for (int i = q[0]; i <= q[1]; ++i) ++arr[i];  // 쿼리의 양 끝을 포함한 모든 원소를 1 증가
//     return arr;  // 모든 구간의 증가를 반영한 배열 반환
// }  // 블록 끝

// 풀이 요약
// 각 닫힌 구간에 속한 원소를 모두 1씩 증가
