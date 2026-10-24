#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <limits.h>
#include <stdint.h>

static size_t upper_bound(const long long* values, size_t size, long long value) { size_t low = 0, high = size; while (low < high) { size_t mid = (low + high) / 2; if (values[mid] <= value) low = mid + 1; else high = mid; } return low; }
static long long prefix(long long count, int* arr, size_t n, const long long* lengths, const long long* sums) {
    size_t index = upper_bound(lengths,n + 1,count) - 1; if (index == n) --index;
    return sums[index] + (count - lengths[index]) * arr[index];
}
long long* solution(int arr[], size_t arr_len, long long l, long long r) {
    size_t n = arr_len; long long* lengths = calloc(n + 1, sizeof(*lengths)); long long* sums = calloc(n + 1, sizeof(*sums));
    for (size_t i = 0; i < n; ++i) { lengths[i + 1] = lengths[i] + arr[i]; sums[i + 1] = sums[i] + (long long)arr[i] * arr[i]; }
    long long target = prefix(r,arr,n,lengths,sums) - prefix(l - 1,arr,n,lengths,sums), window = r - l + 1, last = lengths[n] - window, current = prefix(window,arr,n,lengths,sums), start = 0, answer_count = 0;
    size_t left = 0, right = upper_bound(lengths,n + 1,window) - 1;
    while (start < last) {
        long long span = lengths[left + 1] - start, other = lengths[right + 1] - start - window;
        if (other < span) span = other; if (last - start < span) span = last - start;
        long long slope = (long long)arr[right] - arr[left], difference = target - current;
        if (!slope) { if (current == target) answer_count += span; }
        else if (difference % slope == 0 && difference / slope >= 0 && difference / slope < span) ++answer_count;
        current += slope * span; start += span;
        if (start == lengths[left + 1]) ++left; if (start + window == lengths[right + 1]) ++right;
    }
    answer_count += current == target; long long* answer = malloc(2 * sizeof(*answer)); answer[0] = target; answer[1] = answer_count;
    free(lengths); free(sums);
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // 문자열 형식 읽기·쓰기용 표준 입출력 선언
// #include <stdlib.h>  // 동적 메모리, 정수 변환, 정렬 함수 선언
// #include <string.h>  // 문자열 길이·비교·복사와 메모리 함수 선언
// #include <stdbool.h>  // 참·거짓 표시용 bool, true, false
// #include <limits.h>  // 최솟값·최댓값 초기화에 쓸 정수 범위 상수
// #include <stdint.h>  // 비트 마스크와 해시 키에 쓸 고정 폭 정수
//
// static size_t upper_bound(const long long* values, size_t size, long long value) { size_t low = 0, high = size; while (low < high) { size_t mid = (low + high) / 2; if (values[mid] <= value) low = mid + 1; else high = mid; } return low; }  // 현재 길이를 넘는 첫 누적 경계 찾기
// static long long prefix(long long count, int* arr, size_t n, const long long* lengths, const long long* sums) {  // 구간 합을 빠르게 구할 수 있도록 지정한 길이까지의 누적합을 계산
//     size_t index = upper_bound(lengths,n + 1,count) - 1; if (index == n) --index;  // 접두사가 끝나는 압축 블록 저장
//     return sums[index] + (count - lengths[index]) * arr[index];  // 압축 블록의 값 합 누적합 / 접두사가 끝나는 압축 블록 / 접두사에서 읽을 길이로 최종값 계산
// }  // 이 범위 끝
// long long* solution(int arr[], size_t arr_len, long long l, long long r) {  // brr를 만들면 길이가 매우 커짐; 각 묶음의 길이·합만 누적해 K를 구하고, 고정 길이 구간을 묶음 경계 사이에서 한꺼번에 이동하기
//     size_t n = arr_len; long long* lengths = calloc(n + 1, sizeof(*lengths)); long long* sums = calloc(n + 1, sizeof(*sums));  // 압축 블록 수 / 압축 블록의 펼친 길이 누적합 / 압축 블록의 값 합 누적합 공간 확보하고 0으로 시작
//     for (size_t i = 0; i < n; ++i) { lengths[i + 1] = lengths[i] + arr[i]; sums[i + 1] = sums[i] + (long long)arr[i] * arr[i]; }  // 압축 블록 번호 순서대로 확인; 압축 블록의 펼친 길이 누적합 / 압축 블록의 값 합 누적합 갱신
//     long long target = prefix(r,arr,n,lengths,sums) - prefix(l - 1,arr,n,lengths,sums), window = r - l + 1, last = lengths[n] - window, current = prefix(window,arr,n,lengths,sums), start = 0, answer_count = 0;  // 주어진 l부터 r까지의 합 / 고정 구간 길이 / 마지막으로 가능한 시작 위치 / 현재 시작점의 구간 합 / 현재 슬라이딩 시작 위치 저장
//     size_t left = 0, right = upper_bound(lengths,n + 1,window) - 1;  // 왼쪽 경계가 있는 블록 / 오른쪽 경계가 있는 블록 저장
//     while (start < last) {  // 처리할 압축 구간이 남아 있는 동안 같은 기울기 범위씩 건너뛰기
//         long long span = lengths[left + 1] - start, other = lengths[right + 1] - start - window;  // 두 경계가 같은 블록에 머무는 이동 폭 / 오른쪽 경계가 블록을 벗어나기 전 폭 저장
//         if (other < span) span = other; if (last - start < span) span = last - start;  // 양끝 값이 바뀌는 시점과 마지막 처리 위치 중 가장 가까운 경계 선택
//         long long slope = (long long)arr[right] - arr[left], difference = target - current;  // 한 칸 움직일 때 구간 합 변화 / 목표 합과 현재 합 차이 저장
//         if (!slope) { if (current == target) answer_count += span; }  // 한 칸 움직일 때 구간 합 변화가 없으면 현재 시작점의 구간 합 / 주어진 l부터 r까지의 합 / 목표 합과 같은 고정 길이 구간 수 더해 누적
//         else if (difference % slope == 0 && difference / slope >= 0 && difference / slope < span) ++answer_count;  // 목표 합에 도달하는 정수 이동량이 현재 구간 안에 있으면 한 경우 추가
//         current += slope * span; start += span;  // 현재 시작점의 구간 합 / 한 칸 움직일 때 구간 합 변화 / 두 경계가 같은 블록에 머무는 이동 폭 더해 누적
//         if (start == lengths[left + 1]) ++left; if (start + window == lengths[right + 1]) ++right;  // 창의 양끝이 누적 길이 경계를 지나면 해당 구간 번호 이동
//     }  // 이 범위 끝
//     answer_count += current == target; long long* answer = malloc(2 * sizeof(*answer)); answer[0] = target; answer[1] = answer_count;  // 목표 구간 합과 같은 합의 구간 수 공간 확보
//     free(lengths); free(sums);  // 압축 블록의 펼친 길이 누적합 / 압축 블록의 값 합 누적합 임시 공간 정리
//     return answer;  // 목표 구간 합과 같은 합의 구간 수 반환
// }  // 이 범위 끝

// 풀이 요약
// brr를 만들면 길이가 매우 커짐; 각 묶음의 길이·합만 누적해 K를 구하고, 고정 길이 구간을 묶음 경계 사이에서 한꺼번에 이동하기
// 같은 묶음 안에서는 구간 합이 일정한 등차수열이므로 목표 합과 같은 위치를 나눗셈으로 세기; 시간 O(N), 공간 O(N)
// 예: [2,2,2]는 2가 여섯 번인 배열; 길이 1인 모든 구간 합이 2이므로 [2,6]
