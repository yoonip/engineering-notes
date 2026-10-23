#include <algorithm>
#include <functional>
#include <vector>
using namespace std;

int solution(int n, vector<vector<int>> q, vector<int> ans) {
    vector<int> chosen;
    int answer = 0;
    function<void(int)> dfs = [&](int start) {
        if (chosen.size() == 5) {
            for (int i = 0; i < (int)q.size(); ++i) {
                int matches = 0;
                for (int value : chosen) if (find(q[i].begin(), q[i].end(), value) != q[i].end()) ++matches;
                if (matches != ans[i]) return;
            }
            ++answer;
            return;
        }
        for (int value = start; value <= n - (4 - (int)chosen.size()); ++value) {
            chosen.push_back(value);
            dfs(value + 1);
            chosen.pop_back();
        }
    };
    dfs(1);
    return answer;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <functional>  // 재귀 람다를 담는 function과 함수 객체
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(int n, vector<vector<int>> q, vector<int> ans) {  // 모든 응답에 맞는 다섯 숫자 조합 세기
// vector<int> chosen;  // 현재 선택한 서로 다른 숫자들을 오름차순으로 저장
// int answer = 0;  // 조건을 만족하는 비밀 코드 수 초기화
// function<void(int)> dfs = [&](int start) {  // 다음으로 선택 가능한 최소 숫자를 상태로 조합을 생성
// if (chosen.size() == 5) {  // 다섯 숫자를 고르면 모든 시도와 비교
// for (int i = 0; i < (int)q.size(); ++i) {  // 주어진 시도를 차례대로 검사
// int matches = 0;  // 이번 시도의 공통 숫자 수 초기화
// for (int value : chosen) if (find(q[i].begin(), q[i].end(), value) != q[i].end()) ++matches;  // 선택한 숫자가 시도에 포함되는지 세기
// if (matches != ans[i]) return;  // 응답과 다르면 이 조합을 제외
// }  // 블록 끝
// ++answer;  // 모든 조건을 만족하는 조합을 하나 세기
// return;  // 완성한 조합의 탐색을 끝
// }  // 블록 끝
// for (int value = start; value <= n - (4 - (int)chosen.size()); ++value) {  // 다섯 개를 채울 수 있는 범위에서 다음 숫자 선택
// chosen.push_back(value);  // 선택한 숫자 추가
// dfs(value + 1);  // 더 큰 숫자만 선택해 중복 조합을 막기
// chosen.pop_back();  // 다른 선택을 위해 마지막 숫자 되돌리기
// }  // 블록 끝
// };  // 블록 끝
// dfs(1);  // 숫자 1부터 다섯 개의 조합을 생성
// return answer;  // 가능한 비밀 코드 수 반환
// }  // 블록 끝

// 풀이 요약
// 1부터 n까지의 숫자 중 다섯 개를 조합으로 만들고 모든 시도의 공통 숫자 수가 응답과 같은지 검사
