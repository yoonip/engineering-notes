#include <stdio.h> // 빈도 입력과 출력
enum { CAPACITY = 53 }; // 서로 다른 키 최대 20개보다 넉넉한 해시 칸 수
static int used[CAPACITY], keys[CAPACITY], counts[CAPACITY]; // 빈 칸 표시·키·빈도 배열
static int locate(int key) { // 키가 있거나 처음 빈 칸인 위치 찾기
    int slot = (key % CAPACITY + CAPACITY) % CAPACITY; // 음수 키도 0~52의 시작 위치로 변환
    while (used[slot] && keys[slot] != key) slot = (slot + 1) % CAPACITY; // 충돌한 다른 키 뒤를 선형 탐사
    return slot; // 같은 키 또는 삽입 가능한 빈 칸 반환
} // 해시 위치 탐색 끝
int main(void) { // 실행 시작점
    int n, q; scanf("%d %d", &n, &q); // 값 수와 질의 수 읽기
    for (int i = 0; i < n; ++i) { // 값을 한 번씩 집계
        int key; scanf("%d", &key); int slot = locate(key); // 값과 해시 칸 찾기
        used[slot] = 1; keys[slot] = key; ++counts[slot]; // 키를 보관하고 빈도 증가
    } // 전체 빈도 구축 끝
    for (int i = 0; i < q; ++i) { // 질의 키를 차례로 조회
        int key; scanf("%d", &key); int slot = locate(key); // 찾는 키의 칸 확인
        printf("%s%d", i ? " " : "", used[slot] ? counts[slot] : 0); // 없는 키는 0으로 출력
    } // 모든 질의 처리 끝
    printf("\n"); // 출력 줄 끝내기
    return 0; // 정상 종료
} // 해시 빈도 집계 끝
