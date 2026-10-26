#include <stdio.h> // 기록 입력과 결과 출력
#include <stdlib.h> // qsort 표준 정렬 함수
typedef struct { int id, score, penalty; } Record; // 한 기록의 식별자와 두 정렬 기준
static int compare(const void* a, const void* b) { // qsort가 사용할 일관된 비교 관계
    const Record* x = a; const Record* y = b; // 원소 주소를 기록 주소로 해석
    if (x->score != y->score) return x->score > y->score ? -1 : 1; // 높은 점수가 먼저 오도록 비교
    if (x->penalty != y->penalty) return x->penalty < y->penalty ? -1 : 1; // 동점이면 작은 벌점 우선
    return (x->id > y->id) - (x->id < y->id); // 완전 동률에서는 작은 식별자 우선
} // 세 기준의 비교 끝
int main(void) { // 실행 시작점
    int n; Record data[20]; scanf("%d", &n); // 최대 20개 기록 공간과 개수 준비
    for (int i = 0; i < n; ++i) scanf("%d %d %d", &data[i].id, &data[i].score, &data[i].penalty); // 기록의 세 필드 입력
    qsort(data, n, sizeof(data[0]), compare); // 같은 비교 기준으로 전체 기록 정렬
    for (int i = 0; i < n; ++i) printf("%s%d", i ? " " : "", data[i].id); // 정렬된 식별자만 출력
    printf("\n"); // 출력 줄 끝내기
    return 0; // 정상 종료
} // 다중 기준 정렬 끝
