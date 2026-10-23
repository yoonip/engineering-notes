int solution(int a, int b) {
    int scale_a = 10, scale_b = 10;
    while (scale_a <= a) scale_a *= 10;
    while (scale_b <= b) scale_b *= 10;
    int ab = a * scale_b + b, ba = b * scale_a + a;
    return ab > ba ? ab : ba;
}

// 전체 코드 줄별 설명
// int solution(int a, int b) {  // 더 크게 합치기 풀이 시작
//     int scale_a = 10, scale_b = 10;  // 각 정수를 이어 붙일 때 사용할 자릿수 배율을 10으로 초기화
//     while (scale_a <= a) scale_a *= 10;  // while과 *=로 a를 뒤에 붙일 때 필요한 자릿수 배율을 구하기
//     while (scale_b <= b) scale_b *= 10;  // while과 *=로 b를 뒤에 붙일 때 필요한 자릿수 배율을 구하기
//     int ab = a * scale_b + b, ba = b * scale_a + a;  // 자릿수 배율을 곱해 두 순서로 이어 붙인 수를 계산
//     return ab > ba ? ab : ba;  // 삼항 연산자 ?:로 두 연결 결과 중 큰 값을 반환
// }  // 블록 끝

// 풀이 요약
// 두 정수를 두 순서로 이어 붙이고 더 큰 값을 반환
