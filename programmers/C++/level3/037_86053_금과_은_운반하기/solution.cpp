#include <algorithm>
#include <vector>
using namespace std;

long long solution(int a, int b, vector<int> g, vector<int> s, vector<int> w, vector<int> t) {
    long long left = 0, right = 400000000000000LL;
    while (left < right) {
        long long middle = left + (right - left) / 2, gold = 0, silver = 0, total = 0;
        for (int i = 0; i < (int)g.size(); ++i) {
            long long capacity = ((middle + t[i]) / (2LL * t[i])) * w[i];
            gold += min(1LL * g[i], capacity); silver += min(1LL * s[i], capacity); total += min(1LL * g[i] + s[i], capacity);
            if (gold >= a && silver >= b && total >= 1LL * a + b) break;
        }
        if (gold >= a && silver >= b && total >= 1LL * a + b) right = middle;
        else left = middle + 1;
    }
    return left;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// long long solution(int a, int b, vector<int> g, vector<int> s, vector<int> w, vector<int> t) {  // 운반 가능한 금·은의 양으로 최소 시간 이분 탐색
// long long left = 0, right = 400000000000000LL;  // 운반 시간의 이분 탐색 범위를 설정하기
// while (left < right) {  // 필요한 자원을 옮길 수 있는 최소 시간 찾기
// long long middle = left + (right - left) / 2, gold = 0, silver = 0, total = 0;  // 시간 후보와 운반 가능한 세 자원 합계 초기화
// for (int i = 0; i < (int)g.size(); ++i) {  // 각 도시의 운반 한도 계산
// long long capacity = ((middle + t[i]) / (2LL * t[i])) * w[i];  // 마지막 편도를 포함한 운반 횟수에 적재량 곱하기
// gold += min(1LL * g[i], capacity); silver += min(1LL * s[i], capacity); total += min(1LL * g[i] + s[i], capacity);  // 금, 은, 전체 운반량 상한을 각각 누적
// if (gold >= a && silver >= b && total >= 1LL * a + b) break;  // 이미 충분하면 도시 계산을 중단
// }  // 블록 끝
// if (gold >= a && silver >= b && total >= 1LL * a + b) right = middle;  // 가능하면 더 짧은 시간 찾기
// else left = middle + 1;  // 부족하면 시간 하한 늘리기
// }  // 블록 끝
// return left;  // 최소 운반 시간 반환
// }  // 블록 끝

// 풀이 요약
// 시간을 이분 탐색하고 도시별 운반 횟수로 금, 은, 전체 운반량의 세 조건을 모두 만족하는지 검사
