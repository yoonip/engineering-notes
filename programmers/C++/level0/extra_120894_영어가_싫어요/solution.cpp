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

long long solution(string numbers) {
    vector<string> words = {"zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"};
    long long answer = 0;
    size_t pos = 0;
    while (pos < numbers.size()) {
        for (int d = 0; d < 10; ++d)
            if (numbers.compare(pos, words[d].size(), words[d]) == 0) {
                answer = answer * 10 + d; pos += words[d].size(); break;
            }
    }
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
// long long solution(string numbers) {  // 영어가 싫어요 풀이 시작
//     vector<string> words = {"zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"};  // 0부터 9까지 숫자와 영어 이름을 대응시키는 목록
//     long long answer = 0;  // 영어 숫자를 읽으며 십진수로 쌓을 값
//     size_t pos = 0;  // 아직 해석하지 않은 영어 숫자의 시작 위치
//     while (pos < numbers.size()) {  // 모든 영어 숫자를 읽을 때까지 반복
//         for (int d = 0; d < 10; ++d)  // 현재 부분과 일치하는 zero~nine 찾기
//             if (numbers.compare(pos, words[d].size(), words[d]) == 0) {  // 현재 위치에 해당 숫자의 영어 이름이 맞는 경우
//                 answer = answer * 10 + d; pos += words[d].size(); break;  // 읽은 숫자를 십진수 뒤에 붙이고 단어 길이만큼 이동한 뒤 숫자 검색 종료
//             }  // 블록 끝
//     }  // 블록 끝
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 현재 위치에서 일치하는 영어 숫자를 찾기. 기존 값에 10을 곱하고 그 숫자를 더한 뒤, 읽은 단어 길이만큼 다음 위치로 이동
