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

string solution(string my_string) {
    bool seen[256] = {};
    string answer;
    for (unsigned char c : my_string)
        if (!seen[c]) { seen[c] = true; answer += c; }
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
// string solution(string my_string) {  // 중복된 문자 제거 풀이 시작
//     bool seen[256] = {};  // 참·거짓 또는 비트 표시로 현재 위치의 안전 여부·일치 여부·사용한 발음을 관리
//     string answer;  // 처음 등장한 문자만 모을 결과
//     for (unsigned char c : my_string)  // 입력 순서대로 각 문자의 첫 등장 여부 확인
//         if (!seen[c]) { seen[c] = true; answer += c; }  // 처음 본 문자만 결과에 넣고 이미 보았다고 표시
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 문자별 등장 여부를 배열에 기록. 처음 나온 문자만 결과에 붙여 원래 순서를 유지
