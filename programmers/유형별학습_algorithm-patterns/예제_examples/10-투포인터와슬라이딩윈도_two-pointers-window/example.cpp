#include <iostream> // 표준 입력과 출력
#include <vector> // 입력 배열 저장
using namespace std; // 표준 이름의 접두사 생략
int main() { // 실행 시작점
    int n, target; cin >> n >> target; // 배열 길이와 목표 합 읽기
    vector<int> a(n); // 원소 수에 맞춘 배열
    for (int& value : a) cin >> value; // 양수 원소 입력
    int left = 0, best = n + 1; // 왼쪽 경계와 미발견 표식
    long long sum = 0; // 현재 창의 합
    for (int right = 0; right < n; ++right) { // 오른쪽 경계를 순서대로 확장
        sum += a[right]; // 새 원소를 합에 추가
        while (sum >= target) { // 합이 충분한 동안 짧은 창 탐색
            int length = right - left + 1; // 현재 창의 길이 계산
            if (length < best) best = length; // 가장 짧은 길이 유지
            sum -= a[left++]; // 왼쪽 원소를 빼고 시작 위치 이동
        } // 이번 끝점의 축소 끝
    } // 전체 순회 끝
    cout << (best == n + 1 ? 0 : best) << '\n'; // 최소 길이 또는 미발견0 출력
    return 0; // 정상 종료
} // 양수 슬라이딩 윈도 예제 끝
