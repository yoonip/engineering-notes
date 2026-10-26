#include <stdio.h>  // 표준 입력과 출력 함수

int right_count, adjacent[8][8], degree[8], owner[8], visited[8];  // 작은 이분 그래프와 오른쪽 배정
int augment(int left) {  // left의 새 작업을 찾는 증가 경로
    for (int i = 0; i < degree[left]; ++i) {  // 허용된 작업만 확인
        int right = adjacent[left][i];  // 현재 작업 후보
        if (visited[right]) continue;  // 같은 탐색에서 반복 작업 제외
        visited[right] = 1;  // 이 증가 경로 탐색의 방문 표시
        if (owner[right] == -1 || augment(owner[right])) {  // 비었거나 기존 사람을 다른 작업으로 이동
            owner[right] = left;  // 현재 사람에게 작업 배정
            return 1;  // 매칭 크기 하나 증가
        }  // 재배정 성공 조건 끝
    }  // 작업 후보 확인 끝
    return 0;  // 증가 경로가 없는 상태
}  // 증가 경로 탐색 끝
int main(void) {  // 최대 이분 매칭 실행
    int left_count, edge_count;  // 왼쪽 정점과 허용 간선 수
    scanf("%d %d %d", &left_count, &right_count, &edge_count);  // 이분 그래프 크기
    for (int i = 0; i < edge_count; ++i) {  // 중복 없는 허용 관계 저장
        int left, right;  // 간선 양끝
        scanf("%d %d", &left, &right);  // 정점 번호 입력
        adjacent[left][degree[left]++] = right;  // 왼쪽 인접 목록에 추가
    }  // 그래프 입력 끝
    for (int r = 0; r < right_count; ++r) owner[r] = -1;  // 아직 배정되지 않은 작업
    int answer = 0;  // 현재 매칭 크기
    for (int left = 0; left < left_count; ++left) {  // 각 사람의 증가 경로를 시도
        for (int r = 0; r < right_count; ++r) visited[r] = 0;  // 이번 탐색의 방문 표 초기화
        answer += augment(left);  // 성공한 경우에만 한 개 증가
    }  // 모든 사람 처리 끝
    printf("%d\n", answer);  // 최대 배정 수
    return 0;  // 정상 종료
}  // 프로그램 끝
