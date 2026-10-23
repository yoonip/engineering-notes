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

int solution(vector<vector<int>> arr) {
    for (int i = 0; i < (int)arr.size(); ++i)
        for (int j = i + 1; j < (int)arr.size(); ++j) if (arr[i][j] != arr[j][i]) return 0;
    return 1;
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
// int solution(vector<vector<int>> arr) {  // 특별한 이차원 배열 2 풀이 시작
//     for (int i = 0; i < (int)arr.size(); ++i)  // 각 행에서 주대각선 위쪽의 칸 검사
//         for (int j = i + 1; j < (int)arr.size(); ++j) if (arr[i][j] != arr[j][i]) return 0;  // 대각선 양쪽의 대칭 위치가 다르면 즉시 실패
//     return 1;  // 조건의 판정 결과로 1을 반환
// }  // 블록 끝

// 풀이 요약
// 주대각선을 기준으로 서로 마주 보는 두 칸의 값이 모두 같은지 검사
