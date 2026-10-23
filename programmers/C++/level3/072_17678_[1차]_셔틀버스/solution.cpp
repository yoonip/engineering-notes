#include <algorithm>
#include <iomanip>
#include <sstream>
#include <string>
#include <vector>
using namespace std;

string solution(int n, int t, int m, vector<string> timetable) {
    vector<int> crew;
    for (const string& time : timetable) crew.push_back(stoi(time.substr(0,2)) * 60 + stoi(time.substr(3,2)));
    sort(crew.begin(), crew.end()); int index = 0, answer = 0;
    for (int trip = 0; trip < n; ++trip) {
        int departure = 9 * 60 + trip * t, boarded = 0;
        while (index < (int)crew.size() && crew[index] <= departure && boarded < m) { ++index; ++boarded; }
        answer = boarded == m ? crew[index - 1] - 1 : departure;
    }
    ostringstream output; output << setfill('0') << setw(2) << answer / 60 << ':' << setw(2) << answer % 60;
    return output.str();
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <iomanip>  // 문자열 출력의 자리 수와 채움 문자 설정
// #include <sstream>  // 문자열에서 공백 단위로 값을 읽는 스트림
// #include <string>  // 문자열을 담는 string
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// string solution(int n, int t, int m, vector<string> timetable) {  // 마지막 셔틀의 잔여석에 맞춰 최종 도착 시각 계산
// vector<int> crew;  // 크루의 도착 시각을 분 단위로 저장
// for (const string& time : timetable) crew.push_back(stoi(time.substr(0,2)) * 60 + stoi(time.substr(3,2)));  // 시와 분을 정수 시각으로 바꾸기
// sort(crew.begin(), crew.end()); int index = 0, answer = 0;  // 도착 순서와 다음 탑승자 인덱스 초기화
// for (int trip = 0; trip < n; ++trip) {  // 셔틀을 출발 순서대로 채우기
// int departure = 9 * 60 + trip * t, boarded = 0;  // 현재 셔틀 출발 시각과 탑승 수 구하기
// while (index < (int)crew.size() && crew[index] <= departure && boarded < m) { ++index; ++boarded; }  // 도착한 크루를 정원까지 태우기
// answer = boarded == m ? crew[index - 1] - 1 : departure;  // 꽉 차면 마지막 탑승자보다 1분 먼저, 아니면 출발 시각에 오면 됨
// }  // 블록 끝
// ostringstream output; output << setfill('0') << setw(2) << answer / 60 << ':' << setw(2) << answer % 60;  // 두 자리 시와 분 문자열 만들기
// return output.str();  // 마지막 셔틀을 탈 수 있는 가장 늦은 도착 시각 반환
// }  // 블록 끝

// 풀이 요약
// 각 셔틀에 도착순으로 크루를 태우고 마지막 셔틀이 차면 마지막 탑승자보다 1분 먼저, 비면 출발 시각 선택
