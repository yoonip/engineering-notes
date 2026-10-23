#include <algorithm>
#include <string>
using namespace std;

int solution(string s) {
    int n = (int)s.size(), answer = 1;
    for (int center = 0; center < 2 * n - 1; ++center) {
        int left = center / 2, right = left + center % 2;
        while (left >= 0 && right < n && s[left] == s[right]) { --left; ++right; }
        answer = max(answer, right - left - 1);
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <string>  // 문자열을 담는 string
// using namespace std;  // std:: 접두사 생략
// int solution(string s) {  // 문자와 문자 사이를 중심으로 회문 확장
// int n = (int)s.size(), answer = 1;  // 문자열 길이와 최장 회문 길이 초기화
// for (int center = 0; center < 2 * n - 1; ++center) {  // 문자 중심과 문자 사이 중심을 모두 검사
// int left = center / 2, right = left + center % 2;  // 홀수 및 짝수 길이 회문의 두 시작점 구하기
// while (left >= 0 && right < n && s[left] == s[right]) { --left; ++right; }  // 양쪽 문자가 같은 동안 확장
// answer = max(answer, right - left - 1);  // 마지막으로 성공한 회문 길이 비교
// }  // 블록 끝
// return answer;  // 가장 긴 팰린드롬 길이 반환
// }  // 블록 끝

// 풀이 요약
// 각 문자와 문자 사이를 중심으로 양쪽 같은 문자를 확장해 가장 긴 회문 길이 구하기
