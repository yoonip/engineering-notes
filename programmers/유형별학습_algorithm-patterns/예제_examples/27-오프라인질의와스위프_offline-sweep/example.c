#include <stdio.h>  // 점과 질의 입출력
#include <stdlib.h>  // 압축과 이벤트 정렬

typedef struct { int x, y, id; } Event;  // 점이나 질의의 좌표와 원래 번호
int coordinates[30], bit[31], unique_count;  // 압축 좌표와 활성 점의 Fenwick 개수
int compare_int(const void *a, const void *b) {  // 좌표 순서 비교
    int x = *(const int *)a, y = *(const int *)b;  // 비교할 정수
    return (x > y) - (x < y);  // 뺄셈 오버플로 없는 대소 비교
}  // 정수 비교 끝
int compare_event(const void *a, const void *b) {  // x순과 동률 번호순 비교
    const Event *x = (const Event *)a, *y = (const Event *)b;  // 두 이벤트
    if (x->x != y->x) return (x->x > y->x) - (x->x < y->x);  // 작은 x 우선
    return (x->id > y->id) - (x->id < y->id);  // 같은 x의 결정적 순서
}  // 이벤트 비교 끝
int upper(int value) {  // value 이하인 압축 좌표 개수
    int left = 0, right = unique_count;  // 첫 초과 위치를 찾는 구간
    while (left < right) {  // 이분 탐색 구간 축소
        int middle = (left + right) / 2;  // 비교할 좌표 번호
        if (coordinates[middle] <= value) left = middle + 1; else right = middle;  // 포함 조건에 맞는 경계
    }  // 첫 초과 위치 확정
    return left;  // Fenwick 접두 끝 위치
}  // 좌표 경계 탐색 끝
void add(int index) {  // 압축된 1기반 y에 점 하나 추가
    for (; index <= unique_count; index += index & -index) ++bit[index];  // 상위 블록 개수 증가
}  // 활성 점 추가 끝
int prefix(int end) {  // 압축 접두 개수 조회
    int result = 0;  // 조건을 만족하는 점 수
    for (; end > 0; end -= end & -end) result += bit[end];  // 서로소 접두 블록 합산
    return result;  // y 조건까지 만족하는 개수
}  // Fenwick 조회 끝
int main(void) {  // 오프라인 점 개수 처리
    int n, q, answer[30], cursor = 0;  // 입력 수와 점 추가 위치
    Event points[30], queries[30];  // 정렬할 점과 질의
    scanf("%d %d", &n, &q);  // 두 목록의 길이
    for (int i = 0; i < n; ++i) {  // 입력 점 저장
        scanf("%d %d", &points[i].x, &points[i].y);  // 점 좌표
        points[i].id = i; coordinates[i] = points[i].y;  // 동률 순서와 압축 후보
    }  // 점 입력 끝
    for (int i = 0; i < q; ++i) { scanf("%d %d", &queries[i].x, &queries[i].y); queries[i].id = i; }  // 원래 질의 번호 보관
    qsort(coordinates, n, sizeof(int), compare_int);  // y 좌표 정렬
    for (int i = 0; i < n; ++i) if (i == 0 || coordinates[i] != coordinates[i - 1]) coordinates[unique_count++] = coordinates[i];  // 중복 좌표 제거
    qsort(points, n, sizeof(Event), compare_event);  // 추가할 점을 x순으로 정렬
    qsort(queries, q, sizeof(Event), compare_event);  // 질의도 x순으로 재배치
    for (int i = 0; i < q; ++i) {  // 작은 X부터 질의
        while (cursor < n && points[cursor].x <= queries[i].x) {  // 현재 X에 포함되는 점만 추가
            add(upper(points[cursor].y)); ++cursor;  // 같은 y는 같은 빈도 위치 사용
        }  // x 조건 반영 끝
        answer[queries[i].id] = prefix(upper(queries[i].y));  // y 조건과 원래 번호 반영
    }  // 오프라인 처리 끝
    for (int i = 0; i < q; ++i) printf("%d\n", answer[i]);  // 원래 순서로 출력
    return 0;  // 정상 종료
}  // 프로그램 끝
