#include <iostream> // 표준 입력과 출력
#include <vector> // 작업량 배열
using namespace std; // 표준 이름의 접두사 생략
int main() { // 실행 시작점
    int n, limit; cin >> n >> limit; // 작업 수와 허용 그룹 수 읽기
    vector<int> values(n); // 작업 순서를 보관할 배열
    long long low = 0, high = 0; // 최소 작업 용량과 전체 작업 합
    for (int& value : values) { // 각 작업량으로 탐색 범위 계산
        cin >> value; // 작업량 입력
        if (value > low) low = value; // 가장 큰 작업량을 하한으로 유지
        high += value; // 전부 합친 안전한 상한 계산
    } // 탐색 경계 완성
    auto feasible = [&](long long capacity) { // 작업 배열과 그룹 제한을 캡처한 판정 함수
        int groups = 1; long long current = 0; // 사용 그룹 수와 현재 그룹 합
        for (int value : values) { // 원래 순서대로 작업 배치
            if (value > capacity) return false; // 단일 작업도 못 담으면 거절
            if (current + value > capacity) { // 현재 그룹의 용량을 넘는 경우
                ++groups; // 새 연속 그룹 열기
                current = value; // 새 그룹을 이번 작업으로 시작
            } else current += value; // 용량 이내면 현재 그룹에 추가
        } // 탐욕 배치 끝
        return groups <= limit; // 그룹 수 제한 만족 여부
    }; // 판정 람다 정의 끝
    while (low < high) { // 최소 가능한 용량의 구간 축소
        long long middle = low + (high - low) / 2; // 중간 용량 계산
        if (feasible(middle)) high = middle; // 가능하면 이 용량을 포함해 왼쪽 탐색
        else low = middle + 1; // 불가능하면 더 큰 용량만 남기기
    } // 한 용량으로 수렴
    cout << low << '\n'; // 최소 용량 출력
    return 0; // 정상 종료
} // 매개변수 탐색 예제 끝
