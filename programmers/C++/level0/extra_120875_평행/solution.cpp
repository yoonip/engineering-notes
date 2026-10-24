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

int solution(vector<vector<int>> dots) {
    int pairs[3][4] = {{0,1,2,3}, {0,2,1,3}, {0,3,1,2}};
    for (const auto& p : pairs) {
        long long dx1 = dots[p[1]][0] - dots[p[0]][0], dy1 = dots[p[1]][1] - dots[p[0]][1];
        long long dx2 = dots[p[3]][0] - dots[p[2]][0], dy2 = dots[p[3]][1] - dots[p[2]][1];
        if (dy1 * dx2 == dy2 * dx1) return 1;
    }
    return 0;
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
// int solution(vector<vector<int>> dots) {  // 평행 풀이 시작
//     int pairs[3][4] = {{0,1,2,3}, {0,2,1,3}, {0,3,1,2}};  // 네 점을 겹치지 않는 두 직선으로 나누는 세 쌍의 인덱스 목록
//     for (const auto& p : pairs) {  // 네 점을 서로 다른 두 쌍으로 나누는 세 경우
//         long long dx1 = dots[p[1]][0] - dots[p[0]][0], dy1 = dots[p[1]][1] - dots[p[0]][1];  // 첫 직선의 가로·세로 변화량
//         long long dx2 = dots[p[3]][0] - dots[p[2]][0], dy2 = dots[p[3]][1] - dots[p[2]][1];  // 두 번째 직선의 가로·세로 변화량
//         if (dy1 * dx2 == dy2 * dx1) return 1;  // 기울기의 교차 곱이 같으면 두 직선이 평행하므로 1 반환
//     }  // 블록 끝
//     return 0;  // 조건에 맞는 경우가 없으면 0 반환
// }  // 블록 끝

// 풀이 요약
// 기울기의 분자·분모를 교차 곱해 비교하고 네 점을 두 쌍으로 나누는 모든 경우를 검사
