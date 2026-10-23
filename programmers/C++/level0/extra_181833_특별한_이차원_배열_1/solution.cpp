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

vector<vector<int>> solution(int n) {
    vector<vector<int>> answer(n, vector<int>(n, 0));
    for (int i = 0; i < n; ++i) answer[i][i] = 1;
    return answer;
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
// vector<vector<int>> solution(int n) {  // 특별한 이차원 배열 1 풀이 시작
//     vector<vector<int>> answer(n, vector<int>(n, 0));  // 모든 칸이 0인 n×n 배열
//     for (int i = 0; i < n; ++i) answer[i][i] = 1;  // 행과 열 번호가 같은 주대각선만 1
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 0으로 채운 n×n 배열에서 주대각선만 1로 바꾸기
