#include <string>
#include <vector>
#include <algorithm>
#include <numeric>
#include <functional>
#include <unordered_set>
#include <sstream>
#include <cctype>
#include <cstdlib>
using namespace std;

string solution(string rny_string) {
    string answer;
    for (char c : rny_string) {
        if (c == 'm') answer += "rn";
        else answer += c;
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 다룰 string
// #include <vector>  // 길이를 늘릴 수 있는 vector
// #include <algorithm>  // 정렬·검색·뒤집기 알고리즘
// #include <numeric>  // accumulate·iota 등 수치 연산
// #include <functional>  // greater·multiplies 등 함수 객체
// #include <unordered_set>  // 중복을 거를 해시 집합
// #include <sstream>  // 문자열을 항목별로 읽을 스트림
// #include <cctype>  // 문자 검사와 대소문자 변환
// #include <cstdlib>  // 정수 변환과 절댓값 등 표준 함수
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// string solution(string rny_string) {  // rny_string 풀이 시작
//     string answer;  // m을 rn으로 바꿔 이어 붙일 결과
//     for (char c : rny_string) {  // 문자 하나씩 읽어 m의 치환 여부 확인
//         if (c == 'm') answer += "rn";  // c == 'm'이면 answer에 "rn" 더하기
//         else answer += c;  // m이 아닌 문자는 그대로 추가
//     }  // 블록 끝
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 한 문자 m을 두 문자 rn으로 모두 치환
