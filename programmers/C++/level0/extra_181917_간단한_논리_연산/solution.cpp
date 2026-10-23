bool solution(bool x1, bool x2, bool x3, bool x4) {
    return (x1 || x2) && (x3 || x4);
}

// 전체 코드 줄별 설명
// bool solution(bool x1, bool x2, bool x3, bool x4) {  // 간단한 논리 연산 풀이 시작
//     return (x1 || x2) && (x3 || x4);  // ||로 각 쌍의 논리합을 구하고 &&로 두 결과의 논리곱을 반환
// }  // 블록 끝

// 풀이 요약
// 두 쌍의 논리합을 각각 구한 뒤 두 결과의 논리곱을 반환
