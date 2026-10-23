#include <algorithm>
#include <string>
#include <vector>
using namespace std;

vector<int> solution(string s) {
    int conversions = 0, removed = 0;
    while (s != "1") {
        int ones = (int)count(s.begin(), s.end(), '1');
        removed += (int)s.size() - ones;
        s.clear();
        while (ones > 0) { s.push_back(char('0' + ones % 2)); ones /= 2; }
        reverse(s.begin(), s.end());
        ++conversions;
    }
    return {conversions, removed};
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <string>  // 문자열을 담는 string
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// vector<int> solution(string s) {  // 0을 제거하고 남은 길이를 이진수로 반복 변환
// int conversions = 0, removed = 0;  // 변환 횟수와 제거한 0의 수 초기화
// while (s != "1") {  // 문자열이 1이 될 때까지 반복
// int ones = (int)count(s.begin(), s.end(), '1');  // 남길 1의 개수 세기
// removed += (int)s.size() - ones;  // 현재 문자열에서 제거한 0의 수를 더하기
// s.clear();  // 다음 이진수 문자열을 만들기 위해 비우기
// while (ones > 0) { s.push_back(char('0' + ones % 2)); ones /= 2; }  // 1의 개수를 이진수의 낮은 자릿수부터 바꾸기
// reverse(s.begin(), s.end());  // 이진수 자릿수 순서를 바로잡기
// ++conversions;  // 완료한 변환 횟수 늘리기
// }  // 블록 끝
// return {conversions, removed};  // 변환 수와 제거한 0의 총수 반환
// }  // 블록 끝

// 풀이 요약
// 1의 개수를 세고 0의 수를 누적한 뒤 1의 개수를 다시 이진수로 바꾸는 변환을 1이 될 때까지 반복
