// string은 문자열 자료형.
#include <string>
// vector는 가변 길이 배열.
#include <vector>
// pair는 두 값을 묶는 자료형.
#include <utility>
// min·max 함수 제공.
#include <algorithm>
// std 이름 공간 도구를 접두사 없이 사용.
using namespace std;

// int는 정수, vector<string>은 보드 행 문자열 목록.
string solution(int m, int n, vector<string> board) {
    // 알파벳 26개별 두 타일 좌표 저장.
    vector<vector<pair<int, int>>> positions(26);
    // 남은 타일 종류 수.
    int remaining = 0;
    // ++는 1 증가.
    for (int r = 0; r < m; ++r) {
        for (int c = 0; c < n; ++c) {
            // []로 칸 조회.
            char ch = board[r][c];
            // 대문자 타일인지 검사.
            if ('A' <= ch && ch <= 'Z') {
                // 첫 타일이면 종류 수 증가.
                if (positions[ch - 'A'].empty()) ++remaining;
                // {}로 좌표 pair 생성.
                positions[ch - 'A'].push_back({r, c});
            }
        }
    }
    // 축에 나란한 선분 검사.
    auto clear = [&](int r1, int c1, int r2, int c2, char ch) {
        // 가로 선분이면 한 행만.
        for (int r = min(r1, r2); r <= max(r1, r2); ++r) {
            // 세로 선분이면 한 열만.
            for (int c = min(c1, c2); c <= max(c1, c2); ++c) {
                // 다른 타일이나 장애물이 있으면 거짓.
                if (board[r][c] != '.' && board[r][c] != ch) return false;
            }
        }
        // 방해물이 없으면 참.
        return true;
    };
    // 제거 순서 문자열.
    string answer;
    // 남은 타일이 있는 동안 반복.
    while (remaining > 0) {
        // 이번에 제거한 쌍이 있는지 표시.
        bool found = false;
        // 알파벳순으로 검사.
        for (int i = 0; i < 26; ++i) {
            // 없는 타일은 제외.
            if (positions[i].empty()) continue;
            // pair의 first·second로 첫 좌표 분리.
            int r1 = positions[i][0].first, c1 = positions[i][0].second;
            // 둘째 좌표 분리.
            int r2 = positions[i][1].first, c2 = positions[i][1].second;
            // 인덱스를 대문자로 변환.
            char ch = 'A' + i;
            // 가로→세로 L자 경로 검사.
            bool a = clear(r1, c1, r1, c2, ch) && clear(r1, c2, r2, c2, ch);
            // 세로→가로 L자 경로 검사.
            bool b = clear(r1, c1, r2, c1, ch) && clear(r2, c1, r2, c2, ch);
            // 경로가 있으면 제거.
            if (a || b) {
                // 두 칸을 빈칸으로 변경.
                board[r1][c1] = board[r2][c2] = '.';
                // 이 쌍은 이후 건너뜀.
                positions[i].clear();
                // 문자열 끝에 제거 글자 추가.
                answer += ch;
                // 남은 종류 수 하나 감소.
                --remaining;
                // 이번 제거 성공 표시.
                found = true;
                // 다음 제거는 다시 A부터 확인.
                break;
            }
        }
        // 하나도 제거하지 못했으면 실패.
        if (!found) return "IMPOSSIBLE";
    }
    // 사전순 최소 제거 순서 반환.
    return answer;
}
