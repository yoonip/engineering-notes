int solution(int storey) {
    int answer = 0;
    while (storey > 0) {
        int digit = storey % 10; storey /= 10;
        if (digit > 5 || (digit == 5 && storey % 10 >= 5)) {
            answer += 10 - digit;
            ++storey;
        } else answer += digit;
    }
    return answer;
}

// 전체 코드 줄별 설명
// int solution(int storey) {  // 낮은 자리부터 올림·내림 버튼 수 비교
// int answer = 0;  // 필요한 버튼 횟수 초기화
// while (storey > 0) {  // 낮은 자릿수부터 처리
// int digit = storey % 10; storey /= 10;  // 마지막 자릿수와 남은 상위 자릿수를 분리
// if (digit > 5 || (digit == 5 && storey % 10 >= 5)) {  // 올림이 더 유리하거나 다음 자릿수가 올림을 지지하는지 검사
// answer += 10 - digit;  // 위로 이동해 다음 자릿수로 넘기는 횟수를 더하기
// ++storey;  // 상위 자릿수에 올림을 반영
// } else answer += digit;  // 내림이 유리하면 현재 자릿수만큼 아래로 이동
// }  // 블록 끝
// return answer;  // 최소 버튼 횟수 반환
// }  // 블록 끝

// 풀이 요약
// 낮은 자릿수부터 올림과 내림 중 적은 버튼 수를 고르며 자릿수 5에서는 다음 자릿수까지 확인
