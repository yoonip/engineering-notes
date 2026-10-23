#include <vector>
#include <algorithm>
#include <climits>
using namespace std;

int solution(int n, vector<vector<int>> data) {
    sort(data.begin(), data.end());
    int answer = 0;
    for (int i = 0; i < n; ++i) {
        int y = data[i][1];
        int low = -1, high = INT_MAX;
        int j = i + 1;
        while (j < n && data[j][0] == data[i][0]) ++j;
        while (j < n) {
            int end = j;
            while (end < n && data[end][0] == data[j][0]) ++end;
            for (int p = j; p < end; ++p) {
                int other = data[p][1];
                if (other != y && low <= other && other <= high) ++answer;
            }
            for (int p = j; p < end; ++p) {
                int other = data[p][1];
                if (other > y) high = min(high, other);
                else if (other < y) low = max(low, other);
            }
            j = end;
        }
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <vector>  // #include는 헤더 가져오기. vector는 가변 길이 배열.
// #include <algorithm>  // sort·min·max 함수 제공.
// #include <climits>  // INT_MAX 등 정수 범위 상수 제공.
// using namespace std;  // std 이름 공간 도구 사용.
// 
// int solution(int n, vector<vector<int>> data) {  // int는 정수. 중첩 vector로 좌표 목록을 받는 함수.
//     sort(data.begin(), data.end());  // begin·end는 배열 범위. x를 우선으로, 같으면 y순으로 제자리 정렬.
//     int answer = 0;  // 유효한 쌍 수.
//     for (int i = 0; i < n; ++i) {  // 각 점을 왼쪽 꼭짓점으로 고정. ++는 1 증가.
//         int y = data[i][1];  // []로 기준 y좌표 조회.
//         int low = -1, high = INT_MAX;  // 이전 x들에서 본 가장 가까운 아래·위 y경계. 좌표 범위 전체를 허용하며 시작.
//         int j = i + 1;  // 오른쪽 후보 탐색 시작.
//         while (j < n && data[j][0] == data[i][0]) ++j;  // &&는 모두 참, ==는 같음. 같은 x는 너비가 0이므로 통째로 건너뜀.
//         while (j < n) {  // 남은 오른쪽 x그룹을 순회.
//             int end = j;  // 같은 x그룹의 끝 인덱스.
//             while (end < n && data[end][0] == data[j][0]) ++end;  // 현재 x에 속한 모든 점의 범위 찾기.
//             for (int p = j; p < end; ++p) {  // 그룹의 모든 점을 먼저 후보로 판정.
//                 int other = data[p][1];  // 오른쪽 꼭짓점의 y좌표.
//                 if (other != y && low <= other && other <= high) ++answer;  // 높이 0은 제외하고 경계를 넘지 않은 점만 계수. 경계와 같은 y는 허용.
//             }  // 후보 판정 종료.
//             for (int p = j; p < end; ++p) {  // 현재 그룹은 다음 그룹부터 직사각형 안쪽에 들어가므로 경계 갱신.
//                 int other = data[p][1];  // 현재 점 y조회.
//                 if (other > y) high = min(high, other);  // 기준 위에서 가장 가까운 y 유지.
//                 else if (other < y) low = max(low, other);  // 기준 아래에서 가장 가까운 y 유지. 기준과 같으면 변 위이므로 무시.
//             }  // 경계 갱신 종료.
//             j = end;  // 다음 x그룹으로 이동.
//         }  // 오른쪽 그룹 반복 종료.
//     }  // 왼쪽 꼭짓점 반복 종료.
//     return answer;  // 유효한 텐트 꼭짓점 쌍 수 반환.
// }  // 함수 종료.

// 풀이 요약
// 점을 x순으로 정렬한다. 왼쪽 꼭짓점 하나를 고정하고 오른쪽으로 훑으며, 지금까지 안쪽 x구간에서 본 y 중 기준보다 바로 위·아래 값을 경계로 유지한다.
// 오른쪽 꼭짓점의 y가 그 경계를 넘으면 내부에 쐐기가 생긴다. 같은 x의 점들은 모두 후보로 검사한 후 경계를 갱신해 직사각형 경계의 점을 허용한다.
// 예제는 세 쌍만 가능하고 (0,2)-(2,0)은 (1,1)이 안에 있어 제외된다. 시간 O(N²+N log N), 공간 O(N).
// 