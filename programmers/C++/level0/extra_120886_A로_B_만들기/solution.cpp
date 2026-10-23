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

int solution(string before, string after) {
    sort(before.begin(), before.end());
    sort(after.begin(), after.end());
    return before == after ? 1 : 0;
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
// int solution(string before, string after) {  // A로 B 만들기 풀이 시작
//     sort(before.begin(), before.end());  // before를 오름차순 정렬
//     sort(after.begin(), after.end());  // after를 오름차순 정렬
//     return before == after ? 1 : 0;  // 정렬한 문자 목록이 같으면 재배열 가능하므로 1, 아니면 0
// }  // 블록 끝

// 풀이 요약
// 두 문자열을 정렬하면 같은 문자가 같은 횟수만큼 있는지 비교할 수 있음. 정렬 결과가 같아야 재배열 가능
