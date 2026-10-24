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

int solution(int n) {
    int count = 0;
    for (int value = 4; value <= n; ++value)
        for (int d = 2; d <= value / d; ++d)
            if (value % d == 0) { ++count; break; }
    return count;
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
// int solution(int n) {  // 합성수 찾기 풀이 시작
//     int count = 0;  // 1과 자기 자신 외의 약수를 찾은 합성수 개수
//     for (int value = 4; value <= n; ++value)  // 가장 작은 합성수 4부터 n까지 확인
//         for (int d = 2; d <= value / d; ++d)  // 제곱근 이하에서 1이 아닌 약수 찾기
//             if (value % d == 0) { ++count; break; }  // 1과 자기 자신 외의 약수를 찾으면 합성수로 한 번 세고 약수 탐색 종료
//     return count;  // 범위 안의 합성수 총개수
// }  // 블록 끝

// 풀이 요약
// 4부터 n까지 각 수에 대해 제곱근 이하의 약수를 찾기. 하나라도 있으면 합성수로 한 번만 세기
