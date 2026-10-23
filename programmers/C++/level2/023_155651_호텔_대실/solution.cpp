#include <algorithm>
#include <string>
#include <vector>
using namespace std;

int solution(vector<vector<string>> book_time) {
    vector<int> changes(1450, 0);
    auto minute = [](const string& time) { return stoi(time.substr(0, 2)) * 60 + stoi(time.substr(3, 2)); };
    for (const auto& booking : book_time) {
        ++changes[minute(booking[0])];
        --changes[minute(booking[1]) + 10];
    }
    int active = 0, answer = 0;
    for (int change : changes) { active += change; answer = max(answer, active); }
    return answer;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <string>  // 문자열을 담는 string
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(vector<vector<string>> book_time) {  // 청소 시간을 포함한 최대 동시 객실 수 계산
// vector<int> changes(1450, 0);  // 하루의 분 단위 입실과 청소 종료 변화 저장
// auto minute = [](const string& time) { return stoi(time.substr(0, 2)) * 60 + stoi(time.substr(3, 2)); };  // 시와 분을 자정 이후의 분으로 바꾸기
// for (const auto& booking : book_time) {  // 각 예약의 시작과 종료 기록
// ++changes[minute(booking[0])];  // 입실 시각에 필요한 방 수 늘리기
// --changes[minute(booking[1]) + 10];  // 퇴실 후 청소 10분이 끝날 때 방 수 줄이기
// }  // 블록 끝
// int active = 0, answer = 0;  // 현재 사용 방 수와 최대 방 수 초기화
// for (int change : changes) { active += change; answer = max(answer, active); }  // 변화량의 누적합에서 최댓값 찾기
// return answer;  // 필요한 최소 객실 수 반환
// }  // 블록 끝

// 풀이 요약
// 입실 시각에 방 수를 늘리고 퇴실 후 청소 10분이 끝날 때 줄이는 변화량의 누적합에서 최대 동시 사용 수 구하기
