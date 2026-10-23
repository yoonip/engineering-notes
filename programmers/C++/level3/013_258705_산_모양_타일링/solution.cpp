#include <vector>
using namespace std;

int solution(int n, vector<int> tops) {
    (void)n;
    const int MOD = 10007; int joined = 0, free = 1;
    for (int top : tops) {
        int next_joined = (joined + free) % MOD;
        int next_free = ((1 + top) * joined + (2 + top) * free) % MOD;
        joined = next_joined; free = next_free;
    }
    return (joined + free) % MOD;
}

// 전체 코드 줄별 설명
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(int n, vector<int> tops) {  // 경계 연결 상태를 나눠 산 모양 타일링 수 계산
// (void)n;  // 위쪽 삼각형 정보 배열의 각 위치를 순회
// const int MOD = 10007; int joined = 0, free = 1;  // 오른쪽 경계 상태별 타일링 수 초기화
// for (int top : tops) {  // 산 모양의 한 구간씩 추가
// int next_joined = (joined + free) % MOD;  // 다음 구간과 이어지는 타일의 경우 합치기
// int next_free = ((1 + top) * joined + (2 + top) * free) % MOD;  // 위쪽 삼각형 유무에 따른 독립 배치 수를 더하기
// joined = next_joined; free = next_free;  // 현재 구간의 두 상태 갱신
// }  // 블록 끝
// return (joined + free) % MOD;  // 마지막 경계의 두 상태를 합쳐 반환
// }  // 블록 끝

// 풀이 요약
// 오른쪽 경계의 연결 여부 두 상태를 유지하며 위쪽 삼각형 유무에 따른 타일링 수를 구간마다 갱신
