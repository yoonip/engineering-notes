#include <iostream>
using namespace std;
int main(void) {
    string code;
    cin >> code;
    string last_four_words = code.substr(code.size()-4, 4);
    if(last_four_words == "_eye"){
        cout << "Ophthalmologyc";
    }
    else if(last_four_words == "head"){
        cout << "Neurosurgery";
    }
    else if(last_four_words == "infl"){
        cout << "Orthopedics";
    }
    else if(last_four_words == "skin"){
        cout << "Dermatology";
    }
    else {
        cout << "direct recommendation";
    }
    return 0;
}

// 전체 코드 줄별 설명
// #include <iostream>  // cin·cout 표준 입출력
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
// int main(void) {  // 입력을 읽고 답을 출력할 시작점
//     string code;  // 환자 코드를 저장할 string 변수를 선언
//     cin >> code;  // 입력 연산자 >>로 표준 입력의 값을 변수에 저장
//     string last_four_words = code.substr(code.size()-4, 4);  // size()로 길이를 구하고 substr()로 마지막 네 글자를 추출
//     if(last_four_words == "_eye"){  // ==로 마지막 네 글자를 병과 분류 표의 문자열과 비교해 해당 분기를 선택
//         cout << "Ophthalmologyc";  // <<로 현재 조건에 해당하는 병과 이름 또는 추천 문구를 출력
//     }  // 블록 끝
//     else if(last_four_words == "head"){  // ==로 마지막 네 글자를 병과 분류 표의 문자열과 비교해 해당 분기를 선택
//         cout << "Neurosurgery";  // <<로 현재 조건에 해당하는 병과 이름 또는 추천 문구를 출력
//     }  // 블록 끝
//     else if(last_four_words == "infl"){  // ==로 마지막 네 글자를 병과 분류 표의 문자열과 비교해 해당 분기를 선택
//         cout << "Orthopedics";  // <<로 현재 조건에 해당하는 병과 이름 또는 추천 문구를 출력
//     }  // 블록 끝
//     else if(last_four_words == "skin"){  // ==로 마지막 네 글자를 병과 분류 표의 문자열과 비교해 해당 분기를 선택
//         cout << "Dermatology";  // <<로 현재 조건에 해당하는 병과 이름 또는 추천 문구를 출력
//     }  // 블록 끝
//     else {  // 앞의 모든 병과 분류 조건이 거짓인 경우를 처리
//         cout << "direct recommendation";  // <<로 현재 조건에 해당하는 병과 이름 또는 추천 문구를 출력
//     }  // 블록 끝
//     return 0;  // 0으로 정상 종료
// }  // 블록 끝

// 풀이 요약
// 코드의 마지막 네 글자만 추출하고 병과 분류 표와 차례로 비교
