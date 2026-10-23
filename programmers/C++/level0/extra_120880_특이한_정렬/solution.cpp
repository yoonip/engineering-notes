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

vector<int> solution(vector<int> numlist, int n) {
    sort(numlist.begin(), numlist.end(), [n](int a, int b) {
        if (abs(a - n) != abs(b - n)) return abs(a - n) < abs(b - n);
        return a > b;
    });
    return numlist;
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
// vector<int> solution(vector<int> numlist, int n) {  // 특이한 정렬 풀이 시작
//     sort(numlist.begin(), numlist.end(), [n](int a, int b) {  // 람다 함수에 기준값 n을 캡처하여 거리와 동률 조건에 따라 정렬
//         if (abs(a - n) != abs(b - n)) return abs(a - n) < abs(b - n);  // if 조건이 참이면 지정한 결과를 즉시 반환하여 함수 실행을 끝
//         return a > b;  // n과의 거리가 같으면 더 큰 수를 먼저 배치
//     });  // 비교 함수와 호출 끝
//     return numlist;  // 거리 우선, 동률이면 큰 값 우선으로 정렬한 배열
// }  // 블록 끝

// 풀이 요약
// 비교 함수에서 n과의 거리가 작은 수를 앞에 두고, 거리가 같으면 큰 수를 앞에 두기
