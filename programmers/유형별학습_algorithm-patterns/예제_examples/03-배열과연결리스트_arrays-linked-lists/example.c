#include <stdio.h> // 값과 삽입 명령의 입출력
int main(void) { // 실행 시작점
    int n, m, value[20], next[20]; // 최대 20노드의 값과 다음 노드 번호
    scanf("%d %d", &n, &m); // 초기 노드 수와 삽입 수 입력
    for (int i = 0; i < n; ++i) { // 초기 노드들을 입력 순서대로 연결
        scanf("%d", &value[i]); // 노드에 들어갈 값 읽기
        next[i] = i + 1 < n ? i + 1 : -1; // 다음 노드 또는 끝 표시 지정
    } // 초기 연결 완료
    for (int i = 0; i < m; ++i) { // 알려진 노드 뒤에 차례로 삽입
        int after, item, node = n + i; // 삽입 위치·값·새 노드 번호
        scanf("%d %d", &after, &item); // 위치와 새 값 입력
        value[node] = item; // 새 노드의 값 저장
        next[node] = next[after]; // 기존 뒷부분을 새 노드가 먼저 가리키게 설정
        next[after] = node; // 앞 노드를 새 노드에 연결
    } // 모든 연결 변경 끝
    int first = 1; // 출력 공백을 제어할 표시
    for (int node = 0; node != -1; node = next[node]) { // 머리부터 다음 연결을 따라 순회
        printf("%s%d", first ? "" : " ", value[node]); first = 0; // 순서대로 값을 출력하고 다음부터 공백 추가
    } // 연결된 전체 순회 끝
    printf("\n"); // 출력 줄 끝내기
    return 0; // 정상 종료
} // 인덱스 연결 리스트 예제 끝
