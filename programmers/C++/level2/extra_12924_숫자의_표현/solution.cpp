int solution(int n) {
    int answer = 0;
    for (int length = 1; length * (length + 1) / 2 <= n; ++length) {
        int remaining = n - length * (length - 1) / 2;
        if (remaining % length == 0) ++answer;
    }
    return answer;
}

// 전체 코드 줄별 설명
// int solution(int n) {  // 가능한 연속 수열 길이별 시작값 존재 여부 확인
// int answer = 0;  // 연속한 양의 정수 표현 수 초기화
// for (int length = 1; length * (length + 1) / 2 <= n; ++length) {  // 최소 합이 n 이하인 수열 길이만 검사
// int remaining = n - length * (length - 1) / 2;  // 시작값 외에 연속 증가로 더해지는 부분 빼기
// if (remaining % length == 0) ++answer;  // 나머지가 없으면 양의 정수 시작값이 존재
// }  // 블록 끝
// return answer;  // 가능한 연속합 표현 수 반환
// }  // 블록 끝

// 풀이 요약
// 연속 수열 길이별로 증가분의 합을 뺀 나머지가 길이로 나누어떨어지는지 검사
