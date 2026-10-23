int solution(int a, int b) {
    int scale = 10;
    while (scale <= b) scale *= 10;
    int joined = a * scale + b, product = 2 * a * b;
    return joined > product ? joined : product;
}

// 전체 코드 줄별 설명
// int solution(int a, int b) {  // 두 수의 연산값 비교하기 풀이 시작
//     int scale = 10;  // 한 자리 수를 이어 붙일 때의 배율 10으로 초기화
//     while (scale <= b) scale *= 10;  // while과 *=로 b의 자릿수에 맞는 10의 거듭제곱을 구하기
//     int joined = a * scale + b, product = 2 * a * b;  // 곱셈과 덧셈으로 이어 붙인 수와 2ab를 각각 계산
//     return joined > product ? joined : product;  // 삼항 연산자 ?:로 비교한 두 값 중 큰 값을 반환
// }  // 블록 끝

// 풀이 요약
// a와 b를 이어 붙인 수와 2ab를 계산한 뒤 큰 값을 반환
