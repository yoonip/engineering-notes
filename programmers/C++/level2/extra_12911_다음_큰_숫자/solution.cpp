int solution(int n) {
    int lowest = n & -n;
    int raised = n + lowest;
    int tail = ((n ^ raised) >> 2) / lowest;
    return raised | tail;
}

// 전체 코드 줄별 설명
// int solution(int n) {  // 1비트 수를 유지하는 다음 큰 정수 계산
// int lowest = n & -n;  // 가장 낮은 1비트를 비트 AND로 분리
// int raised = n + lowest;  // 그 1비트를 위쪽의 첫 0 자리로 올리기
// int tail = ((n ^ raised) >> 2) / lowest;  // 이동으로 바뀐 나머지 1비트를 가장 낮은 자리에 모으기
// return raised | tail;  // 1비트 수가 같으면서 가장 작은 큰 정수 반환
// }  // 블록 끝

// 풀이 요약
// 가장 낮은 1비트를 위쪽으로 올리고 나머지 바뀐 1비트를 낮은 자리에 모아 다음 큰 정수 구하기
