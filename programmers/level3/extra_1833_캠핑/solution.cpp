// vector는 가변 길이 배열.
#include <vector>
// sort·min·max 함수 제공.
#include <algorithm>
// INT_MAX 등 정수 범위 상수 제공.
#include <climits>
// std 이름 공간 도구 사용.
using namespace std;

// 중첩 vector로 좌표 목록을 받는 함수.
int solution(int n, vector<vector<int>> data) {
    // x를 우선으로, 같으면 y순으로 제자리 정렬.
    sort(data.begin(), data.end());
    int answer = 0;
    // ++는 1 증가.
    for (int i = 0; i < n; ++i) {
        // []로 기준 y좌표 조회.
        int y = data[i][1];
        // 좌표 범위 전체를 허용하며 시작.
        int low = -1, high = INT_MAX;
        // 오른쪽 후보 탐색 시작.
        int j = i + 1;
        // 같은 x는 너비가 0이므로 통째로 건너뜀.
        while (j < n && data[j][0] == data[i][0]) ++j;
        // 남은 오른쪽 x그룹을 순회.
        while (j < n) {
            // 같은 x그룹의 끝 인덱스.
            int end = j;
            // 현재 x에 속한 모든 점의 범위 찾기.
            while (end < n && data[end][0] == data[j][0]) ++end;
            // 현재 그룹은 다음 그룹부터 직사각형 안쪽에 들어가므로 경계 갱신.
            for (int p = j; p < end; ++p) {
                // 현재 점 y조회.
                int other = data[p][1];
                // 경계와 같은 y는 허용.
                if (other != y && low <= other && other <= high) ++answer;
            }
            // 현재 그룹은 다음 그룹부터 직사각형 안쪽에 들어가므로 경계 갱신.
            for (int p = j; p < end; ++p) {
                // 현재 점 y조회.
                int other = data[p][1];
                // 기준 위에서 가장 가까운 y 유지.
                if (other > y) high = min(high, other);
                // 기준과 같으면 변 위이므로 무시.
                else if (other < y) low = max(low, other);
            }
            // 다음 x그룹으로 이동.
            j = end;
        }
    }
    // 유효한 텐트 꼭짓점 쌍 수 반환.
    return answer;
}
