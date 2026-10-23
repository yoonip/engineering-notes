#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <limits.h>
#include <stdint.h>

long long solution(int sequence[], size_t sequence_len) {
    long long prefix = 0, lowest = 0, highest = 0;
    for (size_t i = 0; i < sequence_len; ++i) {
        prefix += i % 2 ? -(long long)sequence[i] : sequence[i];
        if (prefix < lowest) lowest = prefix; if (prefix > highest) highest = prefix;
    }
    return highest - lowest;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // 문자열 형식 읽기·쓰기용 표준 입출력 선언
// #include <stdlib.h>  // 동적 메모리, 정수 변환, 정렬 함수 선언
// #include <string.h>  // 문자열 길이·비교·복사와 메모리 함수 선언
// #include <stdbool.h>  // 참·거짓 표시용 bool, true, false
// #include <limits.h>  // 최솟값·최댓값 초기화에 쓸 정수 범위 상수
// #include <stdint.h>  // 비트 마스크와 해시 키에 쓸 고정 폭 정수
//
// long long solution(int sequence[], size_t sequence_len) {  // 전체 수열에 +1,-1을 번갈아 곱한 뒤 누적합을 계산; 어떤 구간의 합은 두 누적합의 차이
//     long long prefix = 0, lowest = 0, highest = 0;  // 번갈아 부호를 적용한 누적합 / 지금까지 가장 작은 누적합 / 지금까지 가장 큰 누적합 저장
//     for (size_t i = 0; i < sequence_len; ++i) {  // 펄스 부호를 적용할 원소 위치 순서대로 확인
//         prefix += i % 2 ? -(long long)sequence[i] : sequence[i];  // 번갈아 부호를 적용한 누적합 / 펄스 부호를 적용할 원소 위치 더해 누적
//         if (prefix < lowest) lowest = prefix; if (prefix > highest) highest = prefix;  // 펄스 누적합의 최솟값과 최댓값 갱신
//     }  // 이 범위 끝
//     return highest - lowest;  // 지금까지 가장 큰 누적합 / 지금까지 가장 작은 누적합로 최종값 계산
// }  // 이 범위 끝

// 풀이 요약
// 전체 수열에 +1,-1을 번갈아 곱한 뒤 누적합을 계산; 어떤 구간의 합은 두 누적합의 차이
// 반대 부호의 펄스도 허용되므로 구간 합 절댓값의 최댓값을 찾으면 됨; 이는 전체 누적합의 최댓값-최솟값; 시간 O(N), 추가 공간 O(1)
// 예: [2,3,-6,1,3,-1,2,4]를 변환한 누적합은 0,2,-1,-7,-8,-5,-4,-2,-6.; 최대 2와 최소 -8의 차이는 10
