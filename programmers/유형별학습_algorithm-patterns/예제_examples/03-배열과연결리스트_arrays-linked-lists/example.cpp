#include <iostream> // 표준 입력과 출력
#include <vector> // 노드별 값과 연결 번호 저장
using namespace std; // 표준 이름 접두사 생략
int main() { // 실행 시작점
    int n, m; cin >> n >> m; // 초기 노드와 삽입 개수 읽기
    vector<int> value(n + m), next(n + m, -1); // 필요한 전체 노드 수만큼 배열 준비
    for (int i = 0; i < n; ++i) { // 초기 노드 연결
        cin >> value[i]; // 초기 값 읽기
        next[i] = i + 1 < n ? i + 1 : -1; // 다음 노드 또는 끝 표시 지정
    } // 초기 연결 완료
    for (int i = 0; i < m; ++i) { // 삽입 명령 처리
        int after, item, node = n + i; cin >> after >> item; // 삽입 위치와 새 노드 번호 준비
        value[node] = item; // 새 값 저장
        next[node] = next[after]; // 옛 뒷부분의 연결 보존
        next[after] = node; // 새 노드를 앞 노드 뒤에 삽입
    } // 연결 변경 끝
    bool first = true; // 첫 출력의 공백 생략 표시
    for (int node = 0; node != -1; node = next[node]) { // 머리에서 연결을 따라 값 순회
        cout << (first ? "" : " ") << value[node]; first = false; // 현재 값 출력
    } // 전체 연결 순회 끝
    cout << '\n'; // 출력 줄 끝내기
    return 0; // 정상 종료
} // 인덱스 연결 리스트 예제 끝
