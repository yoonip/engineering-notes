#include <string>
#include <vector>
#include <algorithm>
#include <numeric>
#include <functional>
#include <unordered_set>
#include <unordered_map>
#include <sstream>
#include <cctype>
#include <cstdlib>
#include <cstdio>
#include <cmath>
#include <queue>
#include <set>
#include <climits>
#include <iostream>
using namespace std;

vector<int> solution(vector<string> park, vector<string> routes) {
    int height = (int)park.size(), width = (int)park[0].size(), row = 0, col = 0;
    for (int r = 0; r < height; ++r) for (int c = 0; c < width; ++c) if (park[r][c] == 'S') { row = r; col = c; }
    for (const string& route : routes) {
        char direction = route[0]; int distance = stoi(route.substr(2));
        int dr = direction == 'N' ? -1 : direction == 'S' ? 1 : 0;
        int dc = direction == 'W' ? -1 : direction == 'E' ? 1 : 0;
        int nr = row, nc = col; bool valid = true;
        for (int step = 0; step < distance; ++step) {
            nr += dr; nc += dc;
            if (nr < 0 || nr >= height || nc < 0 || nc >= width || park[nr][nc] == 'X') { valid = false; break; }
        }
        if (valid) { row = nr; col = nc; }
    }
    return {row, col};
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열 string 사용 준비
// #include <vector>  // 가변 길이 배열 vector 사용 준비
// #include <algorithm>  // 정렬·탐색·최솟값 등 표준 알고리즘 사용 준비
// #include <numeric>  // gcd·accumulate 등 수치 알고리즘 사용 준비
// #include <functional>  // 함수 래퍼와 greater 등 비교 함수 객체 사용 준비
// #include <unordered_set>  // 중복 없는 원소를 저장하는 해시 집합 사용 준비
// #include <unordered_map>  // 키로 값을 찾는 해시 맵 사용 준비
// #include <sstream>  // 문자열을 토큰으로 나눠 읽을 스트림 사용 준비
// #include <cctype>  // 숫자·대소문자 검사와 변환 함수 사용 준비
// #include <cstdlib>  // 정수 절댓값 등 표준 유틸리티 함수 사용 준비
// #include <cstdio>  // snprintf 등 형식 있는 입출력 함수 사용 준비
// #include <cmath>  // 제곱근 등 수학 함수 사용 준비
// #include <queue>  // FIFO 큐와 우선순위 큐 사용 준비
// #include <set>  // 중복 제거와 정렬을 함께 하는 집합 사용 준비
// #include <climits>  // 정수 범위 상수 사용 준비
// #include <iostream>  // cin·cout 표준 입출력 사용 준비
// using namespace std;  // 표준 이름의 std:: 접두사 생략
//
// vector<int> solution(vector<string> park, vector<string> routes) {  // 공원 산책 풀이 함수 정의
//     int height = (int)park.size(), width = (int)park[0].size(), row = 0, col = 0;  // 공원 크기 height·width와 현재 위치 row·col 준비
//     for (int r = 0; r < height; ++r) for (int c = 0; c < width; ++c) if (park[r][c] == 'S') { row = r; col = c; }  // 공원을 훑어 시작 표시 S의 좌표를 현재 위치에 저장
//     for (const string& route : routes) {  // 이동 경로 명령을 순서대로 처리
//         char direction = route[0]; int distance = stoi(route.substr(2));  // 명령에서 방향 문자와 이동 거리 분리
//         int dr = direction == 'N' ? -1 : direction == 'S' ? 1 : 0;  // 북쪽이면 -1, 남쪽이면 1인 행 이동량 계산
//         int dc = direction == 'W' ? -1 : direction == 'E' ? 1 : 0;  // 서쪽이면 -1, 동쪽이면 1인 열 이동량 계산
//         int nr = row, nc = col; bool valid = true;  // 임시 위치 nr·nc를 현재 위치에서 시작하고 이동이 가능하다고 가정
//         for (int step = 0; step < distance; ++step) {  // 명령의 거리만큼 한 칸씩 검사
//             nr += dr; nc += dc;  // 임시 좌표를 다음 칸으로 이동
//             if (nr < 0 || nr >= height || nc < 0 || nc >= width || park[nr][nc] == 'X') { valid = false; break; }  // 범위를 벗어나거나 장애물 X이면 이 명령을 취소하고 검사 중단
//         }  // 블록 끝
//         if (valid) { row = nr; col = nc; }  // 모든 칸이 유효할 때만 임시 좌표를 실제 위치로 반영
//     }  // 블록 끝
//     return {row, col};  // 최종 행과 열 반환
// }  // 함수 끝
//

// 풀이 요약
// 시작점을 찾고 각 경로를 임시 좌표로 끝까지 검사. 중간에 경계나 장애물을 만나면 전체 명령을 무시하고, 끝까지 가능할 때만 실제 위치 갱신.
