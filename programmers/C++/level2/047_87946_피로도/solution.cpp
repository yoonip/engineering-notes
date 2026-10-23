#include <algorithm>
#include <functional>
#include <vector>
using namespace std;

int solution(int k, vector<vector<int>> dungeons) {
    vector<bool> used(dungeons.size(), false);
    int answer = 0;
    function<void(int, int)> dfs = [&](int remaining, int count) {
        answer = max(answer, count);
        for (int i = 0; i < (int)dungeons.size(); ++i) if (!used[i] && remaining >= dungeons[i][0]) {
            used[i] = true;
            dfs(remaining - dungeons[i][1], count + 1);
            used[i] = false;
        }
    };
    dfs(k, 0);
    return answer;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <functional>  // 재귀 람다를 담는 function과 함수 객체
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(int k, vector<vector<int>> dungeons) {  // 현재 피로도로 갈 수 있는 던전 방문 순서 탐색
// vector<bool> used(dungeons.size(), false);  // 이미 탐험한 던전을 표시
// int answer = 0;  // 최대 탐험 수 초기화
// function<void(int, int)> dfs = [&](int remaining, int count) {  // 남은 피로도와 탐험 수를 상태로 재귀 탐색
// answer = max(answer, count);  // 현재까지의 최대 탐험 수 갱신
// for (int i = 0; i < (int)dungeons.size(); ++i) if (!used[i] && remaining >= dungeons[i][0]) {  // 아직 가지 않았고 입장 조건을 만족하는 던전만 고르기
// used[i] = true;  // 현재 던전을 사용 처리
// dfs(remaining - dungeons[i][1], count + 1);  // 소모 피로도를 빼고 다음 던전 탐색
// used[i] = false;  // 다른 순서를 위해 선택 되돌리기
// }  // 블록 끝
// };  // 블록 끝
// dfs(k, 0);  // 초기 피로도에서 탐색을 시작
// return answer;  // 최대 탐험 던전 수 반환
// }  // 블록 끝

// 풀이 요약
// 현재 피로도로 입장할 수 있는 미방문 던전을 하나씩 선택하고 방문 표시를 되돌리며 최대 탐험 수 구하기
