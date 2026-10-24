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

int solution(string A, string B) {
    for (size_t shift = 0; shift < A.size(); ++shift) {
        if (A == B) return static_cast<int>(shift);
        rotate(A.begin(), A.end() - 1, A.end());
    }
    return -1;
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
// int solution(string A, string B) {  // 문자열 밀기 풀이 시작
//     for (size_t shift = 0; shift < A.size(); ++shift) {  // 오른쪽 이동 횟수를 0부터 작은 순서로 시도
//         if (A == B) return static_cast<int>(shift);  // A가 B와 같아진 첫 순간의 오른쪽 회전 횟수를 int로 반환
//         rotate(A.begin(), A.end() - 1, A.end());  // rotate는 지정한 중간 위치의 원소가 맨 앞에 오도록 구간을 회전
//     }  // 블록 끝
//     return -1;  // 모든 회전에서도 목표 문자열을 만들 수 없음
// }  // 블록 끝

// 풀이 요약
// 오른쪽으로 한 칸씩 회전해 목표 문자열과 처음 같아지는 횟수를 찾기
