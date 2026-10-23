#include <string>
using namespace std;

string solution(int q, int r, string code) {
    string answer;
    for (size_t i = r; i < code.size(); i += q) answer += code[i];
    return answer;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 다룰 string
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// string solution(int q, int r, string code) {  // qr code 풀이 시작
//     string answer;  // 인덱스를 q로 나눈 나머지가 r인 문자
//     for (size_t i = r; i < code.size(); i += q) answer += code[i];  // for에서 r부터 q칸씩 이동하며 조건에 맞는 문자를 +=로 연결
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 인덱스를 q로 나눈 나머지가 r인 위치의 문자만 연결
