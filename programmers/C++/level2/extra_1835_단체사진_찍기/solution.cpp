#include <algorithm>
#include <cstdlib>
#include <string>
#include <vector>
using namespace std;

int solution(int n, vector<string> data) {
    (void)n;
    string order = "ACFJMNRT"; int answer = 0;
    do {
        bool valid = true;
        for (const string& condition : data) {
            int gap = abs((int)order.find(condition[0]) - (int)order.find(condition[2])) - 1, wanted = condition[4] - '0';
            char op = condition[3];
            if ((op == '=' && gap != wanted) || (op == '<' && gap >= wanted) || (op == '>' && gap <= wanted)) { valid = false; break; }
        }
        answer += valid;
    } while (next_permutation(order.begin(), order.end()));
    return answer;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <cstdlib>  // 정수 절댓값 같은 기본 유틸리티
// #include <string>  // 문자열을 담는 string
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(int n, vector<string> data) {  // 여덟 친구의 모든 순열에서 거리 조건 검사
// (void)n;  // 조건은 data 전체를 순회하므로 별도 조건 수를 쓰지 않음
// string order = "ACFJMNRT"; int answer = 0;  // 여덟 친구의 사전순 첫 배치와 결과 수 초기화
// do {  // 여덟 친구의 모든 순열 확인
// bool valid = true;  // 현재 배치가 모든 조건을 만족한다고 초기화
// for (const string& condition : data) {  // 두 친구 사이 거리 조건 검사
// int gap = abs((int)order.find(condition[0]) - (int)order.find(condition[2])) - 1, wanted = condition[4] - '0';  // 두 친구 사이에 있는 사람 수와 요구 거리 구하기
// char op = condition[3];  // 비교 연산자 읽기
// if ((op == '=' && gap != wanted) || (op == '<' && gap >= wanted) || (op == '>' && gap <= wanted)) { valid = false; break; }  // 하나라도 거리 조건을 어기면 현재 배치를 제외
// }  // 블록 끝
// answer += valid;  // 모든 조건을 만족하는 배치 세기
// } while (next_permutation(order.begin(), order.end()));  // 다음 친구 순열을 생성
// return answer;  // 가능한 사진 배치 수 반환
// }  // 블록 끝

// 풀이 요약
// 여덟 친구의 모든 순열에서 두 친구 사이의 사람 수가 주어진 비교 조건을 모두 만족하는지 검사
