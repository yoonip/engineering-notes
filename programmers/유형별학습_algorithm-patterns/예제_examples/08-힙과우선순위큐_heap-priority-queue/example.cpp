#include <functional> // 작은 값 우선 비교자
#include <iostream> // 표준 입력과 출력
#include <queue> // 우선순위 큐
#include <vector> // 힙의 바탕 배열과 결과 저장
using namespace std; // 표준 이름의 접두사 생략
int main() { // 실행 시작점
    int n, k; cin >> n >> k; // 입력 개수와 유지할 개수 읽기
    priority_queue<int, vector<int>, greater<int>> heap; // 최솟값이 top인 힙
    for (int i = 0; i < n; ++i) { // 모든 후보를 입력 순서대로 처리
        int value; cin >> value; // 이번 후보 값 읽기
        if (static_cast<int>(heap.size()) < k) heap.push(value); // 빈자리가 있으면 후보 보관
        else if (value > heap.top()) { // 보관 중인 최솟값보다 클 때 교체
            heap.pop(); // 상위 K개에서 빠질 값 제거
            heap.push(value); // 새 값으로 K개 유지
        } // 교체 판단 끝
    } // 모든 후보 확인 끝
    vector<int> result; // 오름차순으로 꺼낸 값 저장
    while (!heap.empty()) { // 힙을 비울 때까지 반복
        result.push_back(heap.top()); // 현재 최솟값을 결과 끝에 저장
        heap.pop(); // 저장한 값을 힙에서 제거
    } // 오름차순 결과 완성
    for (int i = k - 1; i >= 0; --i) cout << (i == k - 1 ? "" : " ") << result[i]; // 역순으로 큰 값부터 출력
    cout << '\n'; // 출력 줄 끝내기
    return 0; // 정상 종료
} // 상위 K개 예제 끝
