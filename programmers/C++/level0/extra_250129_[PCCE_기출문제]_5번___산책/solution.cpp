#include <string>
#include <vector>

using namespace std;

vector<int> solution(string route) {
    int east = 0;
    int north = 0;
    vector<int> answer(2);
    for(int i=0; i<route.length(); i++){
        switch(route[i]){
            case 'N':
                north++;
                break;
            case 'S':
                north--;
                break;
            case 'E':
                east++;
                break;
            case 'W':
                east--;
                break;
        }
    }
    answer[0] = east;
    answer[1] = north;
    return answer;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 다룰 string
// #include <vector>  // 길이를 늘릴 수 있는 vector
//
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// vector<int> solution(string route) {  // [PCCE 기출문제] 5번 / 산책 풀이 시작
//     int east = 0;  // 출발점을 기준으로 동쪽 이동량
//     int north = 0;  // 출발점을 기준으로 북쪽 이동량
//     vector<int> answer(2);  // 동서 좌표와 남북 좌표를 담을 두 칸
//     for(int i=0; i<route.length(); i++){  // 이동 경로의 문자를 순서대로 적용
//         switch(route[i]){  // switch로 이동 문자에 해당하는 case를 선택
//             case 'N':  // switch에서 현재 이동 문자가 이 case에 해당하면 다음 구문을 실행
//                 north++;  // 북쪽으로 한 칸
//                 break;  // break로 가장 가까운 반복문이나 switch를 끝
//             case 'S':  // switch에서 현재 이동 문자가 이 case에 해당하면 다음 구문을 실행
//                 north--;  // 남쪽으로 한 칸
//                 break;  // break로 가장 가까운 반복문이나 switch를 끝
//             case 'E':  // switch에서 현재 이동 문자가 이 case에 해당하면 다음 구문을 실행
//                 east++;  // 동쪽으로 한 칸
//                 break;  // break로 가장 가까운 반복문이나 switch를 끝
//             case 'W':  // switch에서 현재 이동 문자가 이 case에 해당하면 다음 구문을 실행
//                 east--;  // 서쪽으로 한 칸
//                 break;  // break로 가장 가까운 반복문이나 switch를 끝
//         }  // 블록 끝
//     }  // 블록 끝
//     answer[0] = east;  // 첫 원소에 동서 방향의 최종 좌표
//     answer[1] = north;  // 둘째 원소에 남북 방향의 최종 좌표
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 동·서를 east의 증감으로, 남·북을 north의 증감으로 표현. switch의 각 case에서 이동한 뒤 break로 끝
