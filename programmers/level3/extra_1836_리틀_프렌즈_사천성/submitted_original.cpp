#include <string>
#include <vector>
#include <utility>
#include <algorithm>
using namespace std;

string solution(int m, int n, vector<string> board) {
    vector<vector<pair<int, int>>> positions(26);
    int remaining = 0;
    for (int r = 0; r < m; ++r) {
        for (int c = 0; c < n; ++c) {
            char ch = board[r][c];
            if ('A' <= ch && ch <= 'Z') {
                if (positions[ch - 'A'].empty()) ++remaining;
                positions[ch - 'A'].push_back({r, c});
            }
        }
    }
    auto clear = [&](int r1, int c1, int r2, int c2, char ch) {
        for (int r = min(r1, r2); r <= max(r1, r2); ++r) {
            for (int c = min(c1, c2); c <= max(c1, c2); ++c) {
                if (board[r][c] != '.' && board[r][c] != ch) return false;
            }
        }
        return true;
    };
    string answer;
    while (remaining > 0) {
        bool found = false;
        for (int i = 0; i < 26; ++i) {
            if (positions[i].empty()) continue;
            int r1 = positions[i][0].first, c1 = positions[i][0].second;
            int r2 = positions[i][1].first, c2 = positions[i][1].second;
            char ch = 'A' + i;
            bool a = clear(r1, c1, r1, c2, ch) && clear(r1, c2, r2, c2, ch);
            bool b = clear(r1, c1, r2, c1, ch) && clear(r2, c1, r2, c2, ch);
            if (a || b) {
                board[r1][c1] = board[r2][c2] = '.';
                positions[i].clear();
                answer += ch;
                --remaining;
                found = true;
                break;
            }
        }
        if (!found) return "IMPOSSIBLE";
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <string>  // #include는 헤더 가져오기. string은 문자열 자료형.
// #include <vector>  // vector는 가변 길이 배열.
// #include <utility>  // pair는 두 값을 묶는 자료형.
// #include <algorithm>  // min·max 함수 제공.
// using namespace std;  // std 이름 공간 도구를 접두사 없이 사용.
// 
// string solution(int m, int n, vector<string> board) {  // string 반환 함수. int는 정수, vector<string>은 보드 행 문자열 목록.
//     vector<vector<pair<int, int>>> positions(26);  // 알파벳 26개별 두 타일 좌표 저장.
//     int remaining = 0;  // 남은 타일 종류 수.
//     for (int r = 0; r < m; ++r) {  // 행 순회. ++는 1 증가.
//         for (int c = 0; c < n; ++c) {  // 열 순회.
//             char ch = board[r][c];  // char는 한 글자. []로 칸 조회.
//             if ('A' <= ch && ch <= 'Z') {  // &&는 모두 참. 대문자 타일인지 검사.
//                 if (positions[ch - 'A'].empty()) ++remaining;  // 문자 차이로 0~25 인덱스 생성. empty는 비었는지 확인. 첫 타일이면 종류 수 증가.
//                 positions[ch - 'A'].push_back({r, c});  // push_back은 추가. {}로 좌표 pair 생성.
//             }  // 타일 조건 종료.
//         }  // 열 반복 종료.
//     }  // 행 반복 종료.
//     auto clear = [&](int r1, int c1, int r2, int c2, char ch) {  // [&]는 주변 변수를 참조하는 람다 함수. 축에 나란한 선분 검사.
//         for (int r = min(r1, r2); r <= max(r1, r2); ++r) {  // 선분의 행 범위 순회. 가로 선분이면 한 행만.
//             for (int c = min(c1, c2); c <= max(c1, c2); ++c) {  // 열 범위 순회. 세로 선분이면 한 열만.
//                 if (board[r][c] != '.' && board[r][c] != ch) return false;  // !=는 다름. 다른 타일이나 장애물이 있으면 거짓.
//             }  // 열 반복 종료.
//         }  // 행 반복 종료.
//         return true;  // 방해물이 없으면 참.
//     };  // 람다 정의 문장의 끝.
//     string answer;  // 제거 순서 문자열.
//     while (remaining > 0) {  // 남은 타일이 있는 동안 반복.
//         bool found = false;  // bool은 참·거짓 자료형. 이번에 제거한 쌍이 있는지 표시.
//         for (int i = 0; i < 26; ++i) {  // 알파벳순으로 검사.
//             if (positions[i].empty()) continue;  // continue는 이번 반복 건너뜀. 없는 타일은 제외.
//             int r1 = positions[i][0].first, c1 = positions[i][0].second;  // pair의 first·second로 첫 좌표 분리.
//             int r2 = positions[i][1].first, c2 = positions[i][1].second;  // 둘째 좌표 분리.
//             char ch = 'A' + i;  // 인덱스를 대문자로 변환.
//             bool a = clear(r1, c1, r1, c2, ch) && clear(r1, c2, r2, c2, ch);  // 가로→세로 L자 경로 검사.
//             bool b = clear(r1, c1, r2, c1, ch) && clear(r2, c1, r2, c2, ch);  // 세로→가로 L자 경로 검사.
//             if (a || b) {  // ||는 둘 중 하나라도 참. 경로가 있으면 제거.
//                 board[r1][c1] = board[r2][c2] = '.';  // 두 칸을 빈칸으로 변경.
//                 positions[i].clear();  // clear는 배열 원소 전부 제거. 이 쌍은 이후 건너뜀.
//                 answer += ch;  // 문자열 끝에 제거 글자 추가.
//                 --remaining;  // 남은 종류 수 하나 감소.
//                 found = true;  // 이번 제거 성공 표시.
//                 break;  // 다음 제거는 다시 A부터 확인.
//             }  // 제거 분기 종료.
//         }  // 알파벳 순회 종료.
//         if (!found) return "IMPOSSIBLE";  // !는 부정. 하나도 제거하지 못했으면 실패.
//     }  // 모든 타일 제거 반복 종료.
//     return answer;  // 사전순 최소 제거 순서 반환.
// }  // 함수 종료.

// 풀이 요약
// 한 번만 꺾는 경로는 두 L자 모양 중 하나다. 두 선분을 확인하고 제거 가능한 타일 중 알파벳이 가장 빠른 것을 매번 제거한다.
// 타일 제거는 다른 경로를 막지 않고 더 열어주므로 현재 제거 가능한 작은 글자를 먼저 골라도 완성 가능성을 잃지 않는다.
// 예: DBA/C*A/CDB는 처음 A·C가 가능하지만 A를 먼저 골라 ABCD가 된다. 타일 종류 T≤26, 시간 O(MN+T²(M+N)), 공간 O(MN).
// 