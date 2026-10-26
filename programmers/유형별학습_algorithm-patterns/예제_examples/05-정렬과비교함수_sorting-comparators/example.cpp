#include <algorithm> // 비교자 기반 표준 정렬
#include <iostream> // 기록의 입출력
#include <vector> // 기록 배열
using namespace std; // 표준 이름 접두사 생략
struct Record { int id, score, penalty; }; // 기록의 세 필드 정의
int main() { // 실행 시작점
    int n; cin >> n; vector<Record> data(n); // 입력 수에 맞는 기록 배열
    for (auto& item : data) cin >> item.id >> item.score >> item.penalty; // 각 기록 입력
    sort(data.begin(), data.end(), [](const Record& x, const Record& y) { // 먼저 와야 하는지 반환할 람다 비교자
        if (x.score != y.score) return x.score > y.score; // 점수 내림차순
        if (x.penalty != y.penalty) return x.penalty < y.penalty; // 같은 점수에서는 벌점 오름차순
        return x.id < y.id; // 나머지 동률은 식별자로 결정
    }); // 비교자와 정렬 호출 완료
    for (int i = 0; i < n; ++i) cout << (i ? " " : "") << data[i].id; // 정렬 결과의 식별자 출력
    cout << '\n'; // 출력 줄 끝내기
    return 0; // 정상 종료
} // 다중 기준 정렬 끝
