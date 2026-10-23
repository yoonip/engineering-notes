#include <string>
#include <vector>
#include <algorithm>
#include <cstdlib>
using namespace std;

int solution(int n, vector<string> data) {
    string friends = "ACFJMNRT";
    vector<int> order{0, 1, 2, 3, 4, 5, 6, 7};
    int answer = 0;
    do {
        int positions[8];
        for (int i = 0; i < 8; ++i) positions[order[i]] = i;
        bool valid = true;
        for (const string &condition : data) {
            int first = friends.find(condition[0]);
            int second = friends.find(condition[2]);
            int gap = abs(positions[first] - positions[second]) - 1;
            char op = condition[3];
            int wanted = condition[4] - '0';
            if ((op == '=' && gap != wanted) || (op == '<' && gap >= wanted) || (op == '>' && gap <= wanted)) {
                valid = false;
                break;
            }
        }
        if (valid) ++answer;
    } while (next_permutation(order.begin(), order.end()));
    return answer;
}

// 전체 코드 줄별 설명
// #include <string>  // #include는 헤더 가져오기. string은 문자열 자료형.
// #include <vector>  // vector는 가변 길이 배열.
// #include <algorithm>  // next_permutation은 다음 사전순 순열을 만드는 함수.
// #include <cstdlib>  // abs는 정수의 절댓값 계산.
// using namespace std;  // std 이름 공간 도구를 접두사 없이 사용.
// 
// int solution(int n, vector<string> data) {  // int는 정수. 조건 목록을 받아 가능한 순서 수를 반환하는 함수.
//     string friends = "ACFJMNRT";  // 친구 번호 0~7에 대응하는 문자 표.
//     vector<int> order{0, 1, 2, 3, 4, 5, 6, 7};  // {}는 초기값 목록. 최초 사전순 순열.
//     int answer = 0;  // 유효한 순서 수 초기화.
//     do {  // do-while은 본문을 먼저 한 번 실행. 최초 순열도 검사.
//         int positions[8];  // 고정 길이 정수 배열. 친구별 현재 위치 저장.
//         for (int i = 0; i < 8; ++i) positions[order[i]] = i;  // []는 인덱스 조회, ++는 1 증가. 순열을 역위치 표로 변환.
//         bool valid = true;  // bool은 참·거짓. 현재 순서의 조건 만족 여부.
//         for (const string &condition : data) {  // const 참조 &로 문자열을 복사 없이 읽기 전용 순회.
//             int first = friends.find(condition[0]);  // find는 해당 글자의 위치 반환. 첫 친구 번호 조회.
//             int second = friends.find(condition[2]);  // 두 번째 친구 번호 조회.
//             int gap = abs(positions[first] - positions[second]) - 1;  // 위치 차이에서 본인 한 칸을 빼 두 친구 사이 사람 수 계산.
//             char op = condition[3];  // char는 한 글자. 비교 연산자 추출.
//             int wanted = condition[4] - '0';  // 숫자 문자에서 '0'을 빼 정수 간격으로 변환.
//             if ((op == '=' && gap != wanted) || (op == '<' && gap >= wanted) || (op == '>' && gap <= wanted)) {  // &&는 모두 참, ||는 하나라도 참. 세 비교 조건 중 해당 조건 위반 여부 검사.
//                 valid = false;  // 조건 하나라도 어기면 유효하지 않음.
//                 break;  // 현재 조건 반복 종료.
//             }  // 조건 분기 종료.
//         }  // 조건 검사 종료.
//         if (valid) ++answer;  // 모든 조건을 만족하면 경우의 수 증가.
//     } while (next_permutation(order.begin(), order.end()));  // begin·end는 배열 범위. 다음 순열이 있으면 계속하고 마지막이면 종료.
//     return answer;  // 가능한 전체 줄서기 수 반환.
// }  // 함수 종료.

// 풀이 요약
// 친구는 여덟 명으로 고정되어 8!=40320개 순서를 모두 검사할 수 있다. 각 순서에서 친구의 위치를 기록하고 모든 조건을 확인한다.
// 두 친구 사이의 다른 사람 수는 abs(위치 차이)-1이다. 옆에 서 있으면 간격은 1이 아니라 0이다.
// 예제 1은 인접 조건과 최소 간격 조건을 함께 만족하는 순서 3648개. 조건 Q개일 때 시간 O(8!·(8+Q)), 추가 공간 O(8+Q).
// 