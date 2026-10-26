#include <iostream> // 표준 입력과 출력 스트림
#include <vector> // 입력 크기에 맞춘 값과 질의 배열
using namespace std; // 표준 이름의 접두사 생략
int main() { // 실행 시작점
    int n, q; cin >> n >> q; // 원소 수와 질의 수 읽기
    vector<int> a(n), l(q), r(q); // 값과 반열린 질의 경계 저장
    vector<long long> prefix(n + 1, 0); // 빈 구간을 포함한 접두 합
    for (int& value : a) cin >> value; // 원래 배열 입력
    for (int i = 0; i < q; ++i) cin >> l[i] >> r[i]; // 질의 경계 입력
    for (int i = 0; i < q; ++i) { // 직접 합산으로 질의 처리
        long long total = 0; // 이번 구간 합 초기화
        for (int j = l[i]; j < r[i]; ++j) total += a[j]; // 구간 원소를 하나씩 더하기
        cout << (i ? " " : "") << total; // 직접 계산 결과 출력
    } // 직접 합산 종료
    cout << '\n'; // 첫 결과 줄 끝내기
    for (int i = 0; i < n; ++i) prefix[i + 1] = prefix[i] + a[i]; // 한 번의 순회로 접두 합 구축
    for (int i = 0; i < q; ++i) cout << (i ? " " : "") << prefix[r[i]] - prefix[l[i]]; // 공통 앞부분을 빼 같은 질의 처리
    cout << '\n'; // 둘째 결과 줄 끝내기
    return 0; // 정상 종료
} // 두 방식의 비교 끝
