#include <stdio.h> // 순서 있는 작업량 입력과 용량 출력
int n, limit, values[20]; // 작업 수·허용 그룹 수·순서대로 처리할 작업량
int feasible(long long capacity) { // 이 용량으로 제한 그룹 안에 담기는지 판정
    int groups = 1; // 첫 그룹부터 사용
    long long current = 0; // 현재 그룹의 작업량 합
    for (int i = 0; i < n; ++i) { // 작업 순서를 유지하며 하나씩 배치
        if (values[i] > capacity) return 0; // 작업 하나도 못 담는 용량 거절
        if (current + values[i] > capacity) { // 현재 그룹에 더 넣을 수 없는 경우
            ++groups; // 다음 연속 그룹 열기
            current = values[i]; // 새 그룹의 첫 작업 저장
        } else current += values[i]; // 아직 여유가 있으면 현재 그룹에 추가
    } // 모든 작업의 탐욕 배치 끝
    return groups <= limit; // 필요한 그룹 수가 제한 이내인지 반환
} // 판정 함수 끝
int main(void) { // 실행 시작점
    long long low = 0, high = 0; // 정답이 포함될 용량의 양 끝
    scanf("%d %d", &n, &limit); // 작업 수와 허용 그룹 수 읽기
    for (int i = 0; i < n; ++i) { // 각 작업량 입력과 탐색 경계 계산
        scanf("%d", &values[i]); // 이번 작업량 읽기
        if (values[i] > low) low = values[i]; // 가장 큰 작업보다 용량이 작을 수 없음
        high += values[i]; // 전부 한 그룹에 담을 용량 계산
    } // 초기 탐색 범위 완성
    while (low < high) { // 가능한 최소 용량이 하나로 좁혀질 때까지 반복
        long long middle = low + (high - low) / 2; // 넘침을 피한 중간 용량
        if (feasible(middle)) high = middle; // 가능한 용량이면 더 작은 쪽도 탐색
        else low = middle + 1; // 불가능한 용량과 그 아래를 제외
    } // 최소 가능한 용량 확정
    printf("%lld\n", low); // 최소 용량 출력
    return 0; // 정상 종료
} // 매개변수 탐색 예제 끝
