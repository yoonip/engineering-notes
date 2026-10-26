#include <iostream>  // C++ 스트림 입출력
#include <algorithm>  // 회의 배열의 std::sort 정렬

typedef struct { int start, end; } Meeting;  // 회의의 시작과 종료를 묶는 값
int compare(const void *left, const void *right) {  // 종료순 정렬에 사용할 비교
    const Meeting *a = (const Meeting *)left, *b = (const Meeting *)right;  // 비교할 두 회의
    if (a->end != b->end) return (a->end > b->end) - (a->end < b->end);  // 종료가 이른 쪽 우선
    return (a->start > b->start) - (a->start < b->start);  // 같은 종료에서는 시작순
}  // 회의 비교 끝
int main() {  // 독립 실행의 시작점
    int n, count = 0, finish = 0;  // 회의 수와 선택 결과
    Meeting meetings[30];  // 허용된 회의 30개 저장
    std::cin >> n;  // 회의 수 읽기
    for (int i = 0; i < n; ++i) {  // 입력한 회의를 차례로 저장
        std::cin >> meetings[i].start >> meetings[i].end;  // 회의 경계 읽기
    }  // 회의 입력 끝
    std::sort(meetings, meetings + n, [](const Meeting &a, const Meeting &b) { return compare(&a, &b) < 0; });  // 종료가 빠른 순서 확정
    for (int i = 0; i < n; ++i) {  // 정렬한 후보를 한 번씩 확인
        if (count == 0 || meetings[i].start >= finish) {  // 직전 선택과 양립하는 회의
            finish = meetings[i].end;  // 다음 회의가 시작할 수 있는 경계
            ++count;  // 선택한 회의 수 증가
        }  // 선택 조건 처리 끝
    }  // 그리디 순회 끝
    std::cout << count << "\n";  // 최대 회의 수 출력
    return 0;  // 정상 종료
}  // 프로그램 끝
