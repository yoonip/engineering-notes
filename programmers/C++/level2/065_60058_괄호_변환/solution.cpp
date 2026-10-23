#include <functional>
#include <string>
using namespace std;

string solution(string p) {
    function<string(const string&)> convert = [&](const string& text) -> string {
        if (text.empty()) return "";
        int balance = 0; bool correct = true;
        for (int i = 0; i < (int)text.size(); ++i) {
            balance += text[i] == '(' ? 1 : -1;
            if (balance < 0) correct = false;
            if (balance == 0) {
                string u = text.substr(0, i + 1), v = text.substr(i + 1);
                if (correct) return u + convert(v);
                string flipped;
                for (int j = 1; j + 1 < (int)u.size(); ++j) flipped += u[j] == '(' ? ')' : '(';
                return "(" + convert(v) + ")" + flipped;
            }
        }
        return "";
    };
    return convert(p);
}

// 전체 코드 줄별 설명
// #include <functional>  // 재귀 람다를 담는 function과 함수 객체
// #include <string>  // 문자열을 담는 string
// using namespace std;  // std:: 접두사 생략
// string solution(string p) {  // 균형 접두사와 나머지를 재귀적으로 변환
// function<string(const string&)> convert = [&](const string& text) -> string {  // 균형잡힌 문자열을 올바른 문자열로 바꾸는 재귀 람다
// if (text.empty()) return "";  // 빈 문자열은 그대로 반환
// int balance = 0; bool correct = true;  // 괄호 차이와 앞부분의 올바름 초기화
// for (int i = 0; i < (int)text.size(); ++i) {  // 가장 짧은 균형잡힌 접두사 찾기
// balance += text[i] == '(' ? 1 : -1;  // 여는 괄호와 닫는 괄호의 차이 갱신
// if (balance < 0) correct = false;  // 도중에 닫는 괄호가 많으면 올바르지 않음
// if (balance == 0) {  // 처음 균형이 맞는 위치에서 u와 v 나누기
// string u = text.substr(0, i + 1), v = text.substr(i + 1);  // 접두사와 남은 부분을 분리
// if (correct) return u + convert(v);  // u가 올바르면 v만 재귀 변환해 연결
// string flipped;  // u의 양 끝을 제외하고 뒤집을 괄호 저장
// for (int j = 1; j + 1 < (int)u.size(); ++j) flipped += u[j] == '(' ? ')' : '(';  // 내부 괄호 방향을 반대로 바꾸기
// return "(" + convert(v) + ")" + flipped;  // 문제의 변환 규칙대로 새 문자열 만들기
// }  // 블록 끝
// }  // 블록 끝
// return "";  // 균형잡힌 입력에서는 도달하지 않는 기본 반환
// };  // 블록 끝
// return convert(p);  // 전체 문자열을 재귀적으로 변환
// }  // 블록 끝

// 풀이 요약
// 가장 짧은 균형잡힌 접두사와 나머지로 분리하고 접두사의 올바름에 따라 연결하거나 괄호를 뒤집는 규칙을 재귀 적용
