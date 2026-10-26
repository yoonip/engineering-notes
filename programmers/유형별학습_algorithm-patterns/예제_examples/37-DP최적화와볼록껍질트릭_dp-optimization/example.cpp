#include <iostream>  // C++ 스트림 입력과 출력

long long slope[31], intercept[31];  // 이전 DP 상태를 나타내는 직선
long long evaluate(int line, long long x) {  // 현재 x에서 직선 값
    return slope[line] * x + intercept[line];  // 기울기와 절편의 선형식
}  // 직선 평가 끝
int redundant(int first, int middle, int last) {  // 가운데 직선이 아래 껍질에 불필요한지 확인
    return (intercept[middle] - intercept[first]) * (slope[middle] - slope[last]) >= (intercept[last] - intercept[middle]) * (slope[first] - slope[middle]);  // 감소 기울기의 교점 순서를 정수 곱으로 비교
}  // 후보 제거 판정 끝
int main() {  // 단조 CHT로 DP 계산
    int n, queue[31], head = 0, tail = 1;  // 앞과 뒤에서 줄일 후보 덱
    long long cost, x[31] = {0}, dp[31] = {0};  // x0과 D0은0
    std::cin >> n >> cost;  // 상태 수와 매 전이의 상수 비용
    for (int i = 1; i <= n; ++i) std::cin >> x[i];  // 엄격 증가 좌표
    queue[0] = 0;  // 초기 직선 y=0
    for (int i = 1; i <= n; ++i) {  // 질의 x도 증가하는 순서
        while (tail - head >= 2 && evaluate(queue[head], x[i]) >= evaluate(queue[head + 1], x[i])) ++head;  // 앞으로도 불리한 앞 직선 제거
        dp[i] = x[i] * x[i] + cost + evaluate(queue[head], x[i]);  // 직선 최솟값과 공통 항 결합
        slope[i] = -2 * x[i];  // 새로운 상태의 감소 기울기
        intercept[i] = dp[i] + x[i] * x[i];  // 새로운 상태의 절편
        while (tail - head >= 2 && redundant(queue[tail - 2], queue[tail - 1], i)) --tail;  // 앞으로도 선택되지 않는 가운데 후보 제거
        queue[tail++] = i;  // 새 직선을 덱 뒤에 삽입
    }  // 모든 상태 계산 끝
    std::cout << dp[n] << "\n";  // 마지막 최적 비용
    return 0;  // 정상 종료
}  // 프로그램 끝
