#include <iostream> // 정수 입력과 결과 출력
#include <unordered_map> // 키에서 빈도를 찾을 해시 테이블
using namespace std; // 표준 이름 접두사 생략
int main() { // 실행 시작점
    int n, q; cin >> n >> q; unordered_map<int, int> counts; // 개수와 빈도 테이블 준비
    for (int i = 0; i < n; ++i) { // 모든 입력 값을 집계
        int key; cin >> key; ++counts[key]; // 없는 키는 0에서 시작해 빈도 증가
    } // 빈도 구축 끝
    for (int i = 0; i < q; ++i) { // 질의 키를 순서대로 조회
        int key; cin >> key; auto found = counts.find(key); // 조회만 하고 없는 키를 새로 넣지 않기
        int answer = found == counts.end() ? 0 : found->second; // 찾지 못하면 빈도 0
        cout << (i ? " " : "") << answer; // 질의 순서대로 빈도 출력
    } // 질의 처리 끝
    cout << '\n'; // 출력 줄 끝내기
    return 0; // 정상 종료
} // 해시 빈도 집계 끝
