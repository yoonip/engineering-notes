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

string solution(string bin1, string bin2) {
    int i = static_cast<int>(bin1.size()) - 1, j = static_cast<int>(bin2.size()) - 1, carry = 0;
    string answer;
    while (i >= 0 || j >= 0 || carry) {
        int sum = carry;
        if (i >= 0) sum += bin1[i--] - '0';
        if (j >= 0) sum += bin2[j--] - '0';
        answer += char('0' + sum % 2);
        carry = sum / 2;
    }
    reverse(answer.begin(), answer.end());
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
// string solution(string bin1, string bin2) {  // 이진수 더하기 풀이 시작
//     int i = static_cast<int>(bin1.size()) - 1, j = static_cast<int>(bin2.size()) - 1, carry = 0;  // 두 문자열의 마지막 비트 위치와 이전 자리에서 넘어온 올림
//     string answer;  // 낮은 비트부터 역순으로 모을 덧셈 결과
//     while (i >= 0 || j >= 0 || carry) {  // 남은 비트나 마지막 올림이 있는 동안 덧셈
//         int sum = carry;  // 이번 자리의 합에 이전 자리 올림부터 반영
//         if (i >= 0) sum += bin1[i--] - '0';  // i >= 0이면 sum에 bin1[i--] - '0' 더하기
//         if (j >= 0) sum += bin2[j--] - '0';  // j >= 0이면 sum에 bin2[j--] - '0' 더하기
//         answer += char('0' + sum % 2);  // 합의 나머지를 이번 결과 비트로 추가
//         carry = sum / 2;  // 2 이상인 부분을 다음 높은 자리의 올림으로 전달
//     }  // 블록 끝
//     reverse(answer.begin(), answer.end());  // reverse는 지정한 시작·끝 반복자 구간의 원소 순서를 뒤집기
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 뒤쪽 비트부터 두 값과 올림을 더하기. 나머지는 결과 비트로 쓰고 몫은 다음 올림으로 넘긴 뒤, 역순으로 쌓은 결과를 뒤집기
