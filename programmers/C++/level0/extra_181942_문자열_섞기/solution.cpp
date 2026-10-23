#include <string>
using namespace std;

string solution(string str1, string str2) {
    string answer;
    for (size_t i = 0; i < str1.size(); ++i) { answer += str1[i]; answer += str2[i]; }
    return answer;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 다룰 string
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// string solution(string str1, string str2) {  // 문자열 섞기 풀이 시작
//     string answer;  // 두 문자열의 문자를 번갈아 모을 결과
//     for (size_t i = 0; i < str1.size(); ++i) { answer += str1[i]; answer += str2[i]; }  // size_t 인덱스를 for로 순회하며 []로 두 문자열의 문자를 번갈아 붙이기
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 두 문자열에서 같은 위치의 문자를 번갈아 연결
