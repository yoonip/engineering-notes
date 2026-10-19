#include <string>
#include <vector>
#include <algorithm>
#include <cstdlib>
using namespace std;

// 조건 목록을 받아 가능한 순서 수를 반환하는 함수.
int solution(int n, vector<string> data) {
    string friends = "ACFJMNRT";
    // 최초 사전순 순열.
    vector<int> order{0, 1, 2, 3, 4, 5, 6, 7};
    int answer = 0;
    do {
        // 친구별 현재 위치 저장.
        int positions[8];
        for (int i = 0; i < 8; ++i) positions[order[i]] = i;
        // 현재 순서의 조건 만족 여부.
        bool valid = true;
        for (const string &condition : data) {
            // 첫 친구 번호 조회.
            int first = friends.find(condition[0]);
            int second = friends.find(condition[2]);
            // 위치 차이에서 본인 한 칸을 빼 두 친구 사이 사람 수 계산.
            int gap = abs(positions[first] - positions[second]) - 1;
            char op = condition[3];
            // 숫자 문자에서 '0'을 빼 정수 간격으로 변환.
            int wanted = condition[4] - '0';
            if ((op == '=' && gap != wanted) || (op == '<' && gap >= wanted) || (op == '>' && gap <= wanted)) {
                // 조건 하나라도 어기면 유효하지 않음.
                valid = false;
                break;
            }
        }
        if (valid) ++answer;
    // 다음 순열이 있으면 계속하고 마지막이면 종료.
    } while (next_permutation(order.begin(), order.end()));
    return answer;
}
