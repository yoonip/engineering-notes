#include <string>
#include <vector>

using namespace std;

string solution(string nickname) {
    string answer = "";
    for(int i=0; i<nickname.size(); i++){
        if(nickname[i] == 'l'){
            answer += "I";
        }
        else if(nickname[i] == 'w'){
            answer += "vv";
        }
        else if(nickname[i] == 'W'){
            answer += "VV";
        }
        else if(nickname[i] == 'O'){
            answer += "0";
        }
        else{
            answer += nickname[i];
        }
    }
    while(answer.size() < 4){
        answer += "o";
    }
    if(answer.size() > 8){
        answer = answer.substr(0,8);
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 다룰 string
// #include <vector>  // 길이를 늘릴 수 있는 vector
//
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// string solution(string nickname) {  // [PCCE 기출문제] 8번 / 닉네임 규칙 풀이 시작
//     string answer = "";  // 규칙대로 바꾼 닉네임을 모을 문자열
//     for(int i=0; i<nickname.size(); i++){  // 원래 닉네임의 문자를 앞에서부터 확인
//         if(nickname[i] == 'l'){  // 소문자 l을 대문자 I로 바꿀 차례
//             answer += "I";  // l 대신 I 추가
//         }  // 블록 끝
//         else if(nickname[i] == 'w'){  // 소문자 w를 두 글자로 바꿀 차례
//             answer += "vv";  // w 대신 vv 추가
//         }  // 블록 끝
//         else if(nickname[i] == 'W'){  // 대문자 W를 두 글자로 바꿀 차례
//             answer += "VV";  // W 대신 VV 추가
//         }  // 블록 끝
//         else if(nickname[i] == 'O'){  // 대문자 O를 숫자 0으로 바꿀 차례
//             answer += "0";  // O 대신 0 추가
//         }  // 블록 끝
//         else{  // 바꿀 필요가 없는 문자
//             answer += nickname[i];  // 나머지 문자는 원래 모습으로 추가
//         }  // 블록 끝
//     }  // 블록 끝
//     while(answer.size() < 4){  // while로 길이가 네 글자가 될 때까지 뒤에 문자를 붙이는 블록을 반복
//         answer += "o";  // 최소 길이 4가 될 때까지 o로 뒤를 채우기
//     }  // 블록 끝
//     if(answer.size() > 8){  // 최대 길이 8을 넘은 경우
//         answer = answer.substr(0,8);  // 앞의 여덟 글자만 남기기
//     }  // 블록 끝
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// l→I, w→vv, W→VV, O→0으로 바꾸기. 네 글자보다 짧으면 o를 붙이고 여덟 글자보다 길면 뒤를 자르기
