#include <iostream> // 정수 입력과 정렬 결과 출력
#include <vector> // 원래 배열과 공유 병합 버퍼
using namespace std; // 표준 이름의 접두사 생략
vector<int> values, buffer; // 모든 재귀 호출이 공유할 배열
void sort_range(int left, int right) { // 반열린 구간 병합 정렬
    if (right - left <= 1) return; // 빈 구간이나 원소 하나는 그대로 종료
    int middle = left + (right - left) / 2; // 좌우 절반의 경계
    sort_range(left, middle); // 왼쪽 부분 문제 해결
    sort_range(middle, right); // 오른쪽 부분 문제 해결
    int i = left, j = middle, out = left; // 양쪽 읽기 위치와 결과 쓰기 위치
    while (i < middle && j < right) { // 두 절반에 모두 값이 남은 동안 반복
        if (values[i] <= values[j]) buffer[out++] = values[i++]; // 동률이면 왼쪽을 먼저 배치
        else buffer[out++] = values[j++]; // 더 작은 오른쪽 원소 배치
    } // 두 절반의 비교 끝
    while (i < middle) buffer[out++] = values[i++]; // 남은 왼쪽 원소 복사
    while (j < right) buffer[out++] = values[j++]; // 남은 오른쪽 원소 복사
    for (int pos = left; pos < right; ++pos) values[pos] = buffer[pos]; // 병합된 구간을 원래 배열에 복사
} // 정렬 재귀 함수 끝
int main() { // 실행 시작점
    int n; cin >> n; // 배열 길이 입력
    values.resize(n); buffer.resize(n); // 두 배열을 같은 크기로 확보
    for (int& value : values) cin >> value; // 원소 입력
    sort_range(0, n); // 전체 구간 정렬
    for (int i = 0; i < n; ++i) cout << (i ? " " : "") << values[i]; // 정렬 결과 출력
    cout << '\n'; // 빈 배열도 빈 줄 하나 출력
    return 0; // 정상 종료
} // 병합 정렬 예제 끝
