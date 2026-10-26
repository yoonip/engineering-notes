#include <iostream>  // C++ 스트림 입력과 출력

int main() {  // 비트집합 부분합 계산 시작
    int n, target;  // 물건 수와 목표 합
    std::cin >> n >> target;  // 목표는 60 이하로 제한
    unsigned long long bits = 1ULL;  // 합 0의 비트만 설정
    unsigned long long limit = (1ULL << (target + 1)) - 1ULL;  // 목표 이하의 비트 범위
    for (int i = 0; i < n; ++i) {  // 각 물건을 한 번만 반영
        int weight;  // 현재 물건의 양의 무게
        std::cin >> weight;  // 무게 입력
        if (weight <= target) bits = (bits | (bits << weight)) & limit;  // 선택과 미선택을 합치고 상한 적용
    }  // 모든 물건 반영 끝
    int possible = (int)((bits >> target) & 1ULL);  // 목표 위치의 비트 확인
    std::cout << (possible ? "YES" : "NO") << "\n";  // 가능 여부 출력
    return 0;  // 정상 종료
}  // 프로그램 끝
