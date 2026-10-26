#include <stdio.h> // 정수 입력과 부분집합 개수 출력
#include <stdlib.h> // 오른쪽 부분합 정렬 함수
long long left_sums[4096], right_sums[4096]; // 절반당 최대 12개 원소의 모든 부분합
int compare(const void* a, const void* b) { // qsort가 사용할 오름차순 비교
    long long x = *(const long long*)a, y = *(const long long*)b; // 비교 대상의 실제 부분합 읽기
    return (x > y) - (x < y); // 뺄셈 넘침 없이 비교 부호 반환
} // 비교 함수 끝
int lower_bound_index(long long* sums, int count, long long target) { // target 이상인 첫 위치 검색
    int low = 0, high = count; // 정답 위치가 포함된 반열린 탐색 구간
    while (low < high) { // 경계가 하나로 좁혀질 때까지 반복
        int middle = low + (high - low) / 2; // 중앙 인덱스
        if (sums[middle] < target) low = middle + 1; // target보다 작은 부분을 제외
        else high = middle; // target 이상인 첫 위치를 왼쪽에서 탐색
    } // 경계 탐색 끝
    return low; // 첫 이상 위치 반환
} // lower bound 함수 끝
int upper_bound_index(long long* sums, int count, long long target) { // target보다 큰 첫 위치 검색
    int low = 0, high = count; // 가능한 삽입 위치 범위
    while (low < high) { // 첫 초과 위치를 찾을 때까지 반복
        int middle = low + (high - low) / 2; // 중앙 인덱스
        if (sums[middle] <= target) low = middle + 1; // target과 같은 부분까지 제외
        else high = middle; // 초과 값이 시작되는 왼쪽 경계 탐색
    } // 경계 탐색 끝
    return low; // 첫 초과 위치 반환
} // upper bound 함수 끝
int main(void) { // 실행 시작점
    int n, values[24], left_count = 1, right_count = 1; // 원소와 양쪽 부분합 개수
    long long target, answer = 0; // 목표 합과 찾은 부분집합 수
    scanf("%d %lld", &n, &target); // 원소 수와 목표 합 입력
    for (int i = 0; i < n; ++i) scanf("%d", &values[i]); // 각 위치의 원소 입력
    left_sums[0] = right_sums[0] = 0; // 두 절반 모두 빈 부분집합부터 시작
    for (int i = 0; i < n / 2; ++i) { // 왼쪽 절반의 모든 부분합 생성
        int old_count = left_count; // 새 원소를 넣기 전 부분합 수 고정
        for (int j = 0; j < old_count; ++j) left_sums[left_count++] = left_sums[j] + values[i]; // 기존 부분합마다 이번 원소를 넣은 경우 추가
    } // 왼쪽 부분합 생성 끝
    for (int i = n / 2; i < n; ++i) { // 오른쪽 절반의 모든 부분합 생성
        int old_count = right_count; // 확장 전 부분합 수 고정
        for (int j = 0; j < old_count; ++j) right_sums[right_count++] = right_sums[j] + values[i]; // 이번 원소를 넣는 선택 추가
    } // 오른쪽 부분합 생성 끝
    qsort(right_sums, right_count, sizeof(long long), compare); // 같은 보완 합이 연속하도록 정렬
    for (int i = 0; i < left_count; ++i) { // 각 왼쪽 선택에 맞는 오른쪽 선택 수 누적
        long long need = target - left_sums[i]; // 오른쪽에서 필요한 보완 합
        answer += upper_bound_index(right_sums, right_count, need) - lower_bound_index(right_sums, right_count, need); // 같은 합의 전체 개수를 두 경계 차이로 더하기
    } // 모든 양쪽 조합 계산 끝
    printf("%lld\n", answer); // 목표 합을 만드는 부분집합 수 출력
    return 0; // 정상 종료
} // 중간에서 만나기 예제 끝
