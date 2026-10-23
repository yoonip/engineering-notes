#include <algorithm>
#include <vector>
using namespace std;

int solution(vector<int> players, int m, int k) {
    vector<int> expires(players.size() + k, 0);
    int active = 0, answer = 0;
    for (int hour = 0; hour < (int)players.size(); ++hour) {
        active -= expires[hour];
        int added = max(0, players[hour] / m - active);
        active += added;
        answer += added;
        expires[hour + k] += added;
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(vector<int> players, int m, int k) {  // 시간별 부족한 서버만 추가하고 만료 반영
// vector<int> expires(players.size() + k, 0);  // 시간별로 사용 기간이 끝나는 서버 수 저장
// int active = 0, answer = 0;  // 현재 서버 수와 누적 증설 수 초기화
// for (int hour = 0; hour < (int)players.size(); ++hour) {  // 시간별 이용자 수를 순회
// active -= expires[hour];  // 현재 시간에 만료되는 서버 제거
// int added = max(0, players[hour] / m - active);  // 필요한 서버 수에서 가동 중인 서버 수 빼기
// active += added;  // 새 서버를 가동 서버 수에 더하기
// answer += added;  // 누적 증설 수를 더하기
// expires[hour + k] += added;  // k시간 뒤의 만료 시각을 예약
// }  // 블록 끝
// return answer;  // 전체 증설 횟수 반환
// }  // 블록 끝

// 풀이 요약
// 시간별 서버 만료 수를 기록하고 현재 가동 수로 부족한 서버만 추가
