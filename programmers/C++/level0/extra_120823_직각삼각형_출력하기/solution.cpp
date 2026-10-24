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

int main() {
    int n;
    cin >> n;
    for (int i = 1; i <= n; ++i) cout << string(i, '*') << '\n';
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
// int main() {  // 입력을 읽고 답을 출력할 시작점
//     int n;  // 삼각형의 줄 수이자 마지막 줄에 출력할 별 개수
//     cin >> n;  // 입력 연산자 >>로 표준 입력에서 정수를 읽어 n에 저장
//     for (int i = 1; i <= n; ++i) cout << string(i, '*') << '\n';  // string으로 해당 행의 별표를 만들고 <<로 별표와 줄바꿈을 출력
//     return 0;  // 0으로 정상 종료
// }  // 블록 끝

// 풀이 요약
// 첫 행부터 별을 1개,2개 순서로 늘려 n개까지 출력
