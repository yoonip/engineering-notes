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

int solution(vector<vector<int>> board, int k) {
    int sum = 0;
    for (int i = 0; i < (int)board.size(); ++i)
        for (int j = 0; j < (int)board[i].size(); ++j) if (i + j <= k) sum += board[i][j];
    return sum;
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
// int solution(vector<vector<int>> board, int k) {  // 이차원 배열 대각선 순회하기 풀이 시작
//     int sum = 0;  // 행·열 인덱스 합 조건에 맞는 원소의 합
//     for (int i = 0; i < (int)board.size(); ++i)  // 행을 하나씩 확인
//         for (int j = 0; j < (int)board[i].size(); ++j) if (i + j <= k) sum += board[i][j];  // 행 번호와 열 번호의 합이 k 이하인 칸만 더하기
//     return sum;  // 누적 합계 값을 반환하고 함수를 끝
// }  // 블록 끝

// 풀이 요약
// 행과 열의 인덱스 합이 기준 이하인 위치만 더하기
