#include <algorithm> // 정렬과 두 삽입 경계 검색
#include <iostream> // 표준 입력과 출력
#include <vector> // 절반의 부분합 목록
using namespace std; // 표준 이름의 접두사 생략
int main() { // 실행 시작점
    int n; long long target; cin >> n >> target; // 원소 수와 목표 합 입력
    vector<int> values(n); // 각 위치의 값 저장
    for (int& value : values) cin >> value; // 원소 입력
    vector<long long> left_sums{0}, right_sums{0}; // 빈 부분집합의 합부터 시작
    for (int i = 0; i < n / 2; ++i) { // 왼쪽 절반의 선택 확장
        int old_count = static_cast<int>(left_sums.size()); // 확장 전 길이 고정
        for (int j = 0; j < old_count; ++j) left_sums.push_back(left_sums[j] + values[i]); // 원소를 넣는 새 부분집합 추가
    } // 왼쪽 부분합 생성 끝
    for (int i = n / 2; i < n; ++i) { // 오른쪽 절반의 선택 확장
        int old_count = static_cast<int>(right_sums.size()); // 이번 확장 전 길이 고정
        for (int j = 0; j < old_count; ++j) right_sums.push_back(right_sums[j] + values[i]); // 이번 원소를 넣은 부분합 추가
    } // 오른쪽 부분합 생성 끝
    sort(right_sums.begin(), right_sums.end()); // 보완 합의 개수를 셀 수 있게 정렬
    long long answer = 0; // 목표 합을 만드는 부분집합 수
    for (long long left : left_sums) { // 왼쪽의 모든 선택 확인
        long long need = target - left; // 오른쪽에서 필요한 합
        answer += upper_bound(right_sums.begin(), right_sums.end(), need) - lower_bound(right_sums.begin(), right_sums.end(), need); // 같은 보완 합의 개수 누적
    } // 양쪽 절반 결합 끝
    cout << answer << '\n'; // 부분집합 개수 출력
    return 0; // 정상 종료
} // 중간에서 만나기 예제 끝
