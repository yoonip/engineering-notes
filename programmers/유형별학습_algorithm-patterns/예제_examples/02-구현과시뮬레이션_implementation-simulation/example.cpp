#include <iostream> // 표준 입력과 출력
#include <string> // 격자 행 문자열
#include <vector> // 격자 높이에 맞춘 행 배열
using namespace std; // 표준 이름 접두사 생략
int main() { // 실행 시작점
    int h, w, row, col, direction, count; // 격자와 로봇 상태
    cin >> h >> w; // 격자 크기 입력
    vector<string> grid(h); // 각 행을 문자열로 보관
    for (string& line : grid) cin >> line; // 격자 행 읽기
    cin >> row >> col >> direction >> count; // 시작 위치·방향·명령 수 읽기
    int dr[4] = {-1, 0, 1, 0}, dc[4] = {0, 1, 0, -1}; // 북·동·남·서 이동량
    for (int i = 0; i < count; ++i) { // 명령을 입력 순서대로 반복
        char command; cin >> command; // 다음 명령 문자 읽기
        if (command == 'R') direction = (direction + 1) % 4; // 제자리에서 방향만 회전
        else { // 전진 명령의 허용 여부 검사
            int nr = row + dr[direction], nc = col + dc[direction]; // 다음 좌표 임시 계산
            if (0 <= nr && nr < h && 0 <= nc && nc < w && grid[nr][nc] != '#') { // 유효한 빈칸인지 확인
                row = nr; col = nc; // 이동할 수 있는 경우만 현재 위치 교체
            } // 다음 칸 검사 끝
        } // 전진 처리 끝
    } // 모든 상태 전이 완료
    cout << row << ' ' << col << ' ' << direction << '\n'; // 최종 상태 출력
    return 0; // 정상 종료
} // 로봇 시뮬레이션 끝
