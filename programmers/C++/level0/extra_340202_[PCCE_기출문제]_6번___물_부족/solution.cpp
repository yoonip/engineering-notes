#include <string>
#include <vector>

using namespace std;

int solution(int storage, int usage, vector<int> change) {
    int total_usage = 0;
    for(int i=0; i<change.size(); i++){
        usage = usage * (100 + change[i]) / 100;
        total_usage += usage;
        if(total_usage > storage){
            return i;
        }
    }
    return -1;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 다룰 string
// #include <vector>  // 길이를 늘릴 수 있는 vector
//
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// int solution(int storage, int usage, vector<int> change) {  // [PCCE 기출문제] 6번 / 물 부족 풀이 시작
//     int total_usage = 0;  // 매달 사용한 물의 누적량
//     for(int i=0; i<change.size(); i++){  // 첫 달부터 사용량 변동률을 차례로 적용
//         usage = usage * (100 + change[i]) / 100;  // 이전 사용량에 100과 변동률의 합을 곱하고 100으로 나눠 이번 달 사용량을 구하기
//         total_usage += usage;  // 이번 달 사용량까지 저장량에서 사용한 총량에 포함
//         if(total_usage > storage){  // 누적 사용량이 저장량을 넘으면 이 달부터 물 부족
//             return i;  // 현재 인덱스 값을 반환하고 함수를 끝
//         }  // 블록 끝
//     }  // 블록 끝
//     return -1;  // 조건을 만족하는 위치가 없으므로 -1을 반환
// }  // 블록 끝

// 풀이 요약
// 지난달 사용량에 변동률을 적용해 이번 달 사용량을 계산. 누적 사용량이 저장량보다 커지는 첫 달의 인덱스를 반환
