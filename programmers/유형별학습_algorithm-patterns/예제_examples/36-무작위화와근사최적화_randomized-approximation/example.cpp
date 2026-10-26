#include <iostream>  // 그래프와 정수 결과 입출력
#include <iomanip>  // 기대값의 소수점6자리 고정

int main() {  // 작은 MAX-CUT 분할의 전수 계산
    int n, m, first[30], second[30];  // 그래프와 간선 양끝
    std::cin >> n >> m;  // 정점과 간선 수
    for (int i = 0; i < m; ++i) std::cin >> first[i] >> second[i];  // 무방향 간선 입력
    int partitions = 1 << n, total = 0, best = 0;  // 균등한 분할 수와 집계
    for (int mask = 0; mask < partitions; ++mask) {  // 모든 정점의 0과1 배치
        int score = 0;  // 현재 절단 간선 수
        for (int i = 0; i < m; ++i) {  // 각 간선의 양쪽 집합 비교
            if (((mask >> first[i]) & 1) != ((mask >> second[i]) & 1)) ++score;  // 서로 다른 쪽의 간선
        }  // 현재 분할 평가 끝
        total += score;  // 정확한 기대값의 분자
        if (score > best) best = score;  // 전수 최적값 유지
    }  // 전체 분할 열거 끝
    double expectation = (double)total / partitions;  // 모든 분할의 균등 평균
    std::cout << "EXPECTED " << std::fixed << std::setprecision(6) << expectation << "\nBEST " << best << "\n";  // 기대값과 최적값 구분
    return 0;  // 정상 종료
}  // 프로그램 끝
