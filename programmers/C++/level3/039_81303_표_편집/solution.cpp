#include <array>
#include <string>
#include <vector>
using namespace std;

string solution(int n, int k, vector<string> cmd) {
    vector<int> previous(n), following(n);
    for (int i = 0; i < n; ++i) { previous[i] = i - 1; following[i] = i + 1; }
    string alive(n, 'O'); vector<array<int,3>> deleted;
    for (const string& command : cmd) {
        char action = command[0];
        if (action == 'U' || action == 'D') { int distance = stoi(command.substr(2)); while (distance--) k = action == 'U' ? previous[k] : following[k]; }
        else if (action == 'C') {
            int left = previous[k], right = following[k]; deleted.push_back({k,left,right}); alive[k] = 'X';
            if (left != -1) following[left] = right; if (right != n) previous[right] = left;
            k = right != n ? right : left;
        } else {
            auto [row,left,right] = deleted.back(); deleted.pop_back(); alive[row] = 'O';
            if (left != -1) following[left] = row; if (right != n) previous[right] = row;
        }
    }
    return alive;
}

// 전체 코드 줄별 설명
// #include <array>  // 크기가 고정된 array
// #include <string>  // 문자열을 담는 string
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// string solution(int n, int k, vector<string> cmd) {  // 이전·다음 행 연결과 삭제 스택으로 표 편집
// vector<int> previous(n), following(n);  // 각 행의 살아 있는 이전 및 다음 행 저장
// for (int i = 0; i < n; ++i) { previous[i] = i - 1; following[i] = i + 1; }  // 처음에는 인접한 원래 행끼리 연결
// string alive(n, 'O'); vector<array<int,3>> deleted;  // 행의 최종 상태와 삭제 복구 스택 만들기
// for (const string& command : cmd) {  // 편집 명령을 순서대로 적용
// char action = command[0];  // 명령 종류 읽기
// if (action == 'U' || action == 'D') { int distance = stoi(command.substr(2)); while (distance--) k = action == 'U' ? previous[k] : following[k]; }  // 연결 목록을 따라 위나 아래로 이동
// else if (action == 'C') {  // 현재 행을 삭제
// int left = previous[k], right = following[k]; deleted.push_back({k,left,right}); alive[k] = 'X';  // 복구할 이웃 정보를 저장하고 삭제 표시
// if (left != -1) following[left] = right; if (right != n) previous[right] = left;  // 양쪽 살아 있는 행을 서로 연결
// k = right != n ? right : left;  // 다음 행이 없으면 이전 행 선택
// } else {  // 가장 최근 삭제한 행을 복구하기
// auto [row,left,right] = deleted.back(); deleted.pop_back(); alive[row] = 'O';  // 삭제 정보를 꺼내 행을 복구 표시
// if (left != -1) following[left] = row; if (right != n) previous[right] = row;  // 원래 두 이웃 사이에 다시 연결
// }  // 블록 끝
// }  // 블록 끝
// return alive;  // 원래 행 순서의 생존 상태 반환
// }  // 블록 끝

// 풀이 요약
// 각 행의 살아 있는 이전 및 다음 행을 연결 목록으로 관리하고 삭제 정보는 스택에 저장해 최근 순서대로 복구하기
