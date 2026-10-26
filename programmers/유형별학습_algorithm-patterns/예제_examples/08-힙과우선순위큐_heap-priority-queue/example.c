#include <stdio.h> // 정수 입력과 선택한 값 출력
int heap[20], size = 0; // 작은 값이 맨 위인 힙과 현재 원소 수
void push(int value) { // 새 값을 힙에 넣는 함수
    int child = size++; // 새 값이 들어갈 마지막 위치 확보
    while (child > 0) { // 부모보다 작으면 위로 이동
        int parent = (child - 1) / 2; // 완전 이진 트리의 부모 인덱스
        if (heap[parent] <= value) break; // 부모가 더 작으면 힙 순서 확보
        heap[child] = heap[parent]; // 큰 부모를 한 칸 아래로 이동
        child = parent; // 다음 비교 위치를 부모로 변경
    } // 올라갈 경로 확인 끝
    heap[child] = value; // 정해진 위치에 새 값 저장
} // 삽입 함수 끝
int pop_min(void) { // 힙의 최솟값을 꺼내는 함수
    int result = heap[0], value = heap[--size], parent = 0; // 반환할 뿌리와 끝에서 가져올 값
    while (2 * parent + 1 < size) { // 왼쪽 자식이 있는 동안 아래로 이동
        int child = 2 * parent + 1; // 우선 왼쪽 자식 선택
        if (child + 1 < size && heap[child + 1] < heap[child]) ++child; // 두 자식 중 작은 쪽 선택
        if (value <= heap[child]) break; // 두 자식보다 작으면 이동 종료
        heap[parent] = heap[child]; // 작은 자식을 빈 부모 자리로 이동
        parent = child; // 빈자리를 자식 위치로 변경
    } // 내려갈 경로 확인 끝
    if (size > 0) heap[parent] = value; // 남은 힙이 있으면 끝 값을 빈자리에 저장
    return result; // 제거한 최솟값 반환
} // 삭제 함수 끝
int main(void) { // 실행 시작점
    int n, k, result[20]; // 입력 개수와 유지할 개수 및 정렬 출력 버퍼
    scanf("%d %d", &n, &k); // N과 K 읽기
    for (int i = 0; i < n; ++i) { // 값을 입력 순서대로 처리
        int value; scanf("%d", &value); // 이번 후보 값 읽기
        if (size < k) push(value); // K개가 차기 전에는 모두 보관
        else if (value > heap[0]) { // 현재 보관한 최솟값보다 큰 후보만 교체
            pop_min(); // 상위 K개에서 빠질 가장 작은 값 제거
            push(value); // 새 후보를 넣어 K개 유지
        } // 교체 판단 끝
    } // 전체 후보 확인 끝
    for (int i = 0; i < k; ++i) result[i] = pop_min(); // 남은 K개를 오름차순으로 꺼내기
    for (int i = k - 1; i >= 0; --i) printf("%s%d", i == k - 1 ? "" : " ", result[i]); // 역순으로 출력해 큰 값부터 나열
    printf("\n"); // 출력 줄 끝내기
    return 0; // 정상 종료
} // 상위 K개 예제 끝
