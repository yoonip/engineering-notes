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

vector<int> solution(int n) {
    vector<int> answer;
    for (int d = 2; d <= n / d; ++d)
        if (n % d == 0) {
            answer.push_back(d);
            while (n % d == 0) n /= d;
        }
    if (n > 1) answer.push_back(n);
    return answer;
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
// vector<int> solution(int n) {  // 소인수분해 풀이 시작
//     vector<int> answer;  // 중복 없이 모을 소인수
//     for (int d = 2; d <= n / d; ++d)  // 남은 n의 제곱근 이하에서 작은 약수부터 검사
//         if (n % d == 0) {  // n % d == 0이면 이 분기에서 처리
//             answer.push_back(d);  // answer 끝에 d 추가
//             while (n % d == 0) n /= d;  // 같은 소인수는 n에서 모두 나눠 없애기
//         }  // 블록 끝
//     if (n > 1) answer.push_back(n);  // n > 1이면 answer 끝에 n 추가
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 작은 인수부터 나누되 같은 인수는 모두 제거한 후 한 번만 기록
