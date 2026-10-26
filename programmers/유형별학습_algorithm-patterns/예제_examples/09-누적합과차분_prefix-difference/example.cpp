#include <iostream> // 표준 입력과 출력
#include <vector> // 길이에 맞춘 값과 차분 배열
using namespace std; // 표준 이름의 접두사 생략
int main() { // 실행 시작점
    int n, q; cin >> n >> q; // 배열 크기와 갱신 개수 읽기
    vector<long long> a(n), diff(n + 1, 0), prefix(n + 1, 0); // 값과 끝 경계를 포함한 두 보조 배열
    for (long long& value : a) cin >> value; // 원래 값 입력
    for (int i = 0; i < q; ++i) { // 구간 갱신을 차분에만 기록
        int l, r; long long delta; cin >> l >> r >> delta; // 반열린 경계와 증가량 읽기
        diff[l] += delta; // 시작 경계에서 증가량 추가
        diff[r] -= delta; // 끝 경계에서 증가량 취소
    } // 모든 갱신 기록 끝
    int left, right; cin >> left >> right; // 최종 합 질의 경계
    long long running = 0; // 현재 위치에 적용할 누적 증가량
    for (int i = 0; i < n; ++i) { // 최종 배열과 접두 합 동시 복원
        running += diff[i]; // 새 경계의 증가·취소 반영
        a[i] += running; // 현재 원소의 최종 값 계산
        prefix[i + 1] = prefix[i] + a[i]; // 최종 배열의 접두 합 갱신
        cout << (i ? " " : "") << a[i]; // 복원한 원소 출력
    } // 한 번의 복원 순회 끝
    cout << '\n' << prefix[right] - prefix[left] << '\n'; // 구간 합을 별도 줄에 출력
    return 0; // 정상 종료
} // 차분과 누적합 예제 끝
