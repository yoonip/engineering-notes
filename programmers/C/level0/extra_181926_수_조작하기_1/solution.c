int solution(int n, const char* control) {
    for (; *control; ++control) {
        if (*control == 'w') ++n;
        else if (*control == 's') --n;
        else if (*control == 'd') n += 10;
        else if (*control == 'a') n -= 10;
    }
    return n;
}

// 전체 코드 줄별 설명
// int solution(int n, const char* control) {  // 수 조작하기 1 풀이 시작
//     for (; *control; ++control) {  // 포인터가 가리키는 문자가 널 문자가 아닐 동안 for로 순회하며 포인터를 이동
//         if (*control == 'w') ++n;  // if와 ==로 w 명령을 검사하고 ++로 현재 수에 1을 더하기
//         else if (*control == 's') --n;  // else if로 s 명령을 검사하고 --로 현재 수에서 1을 빼기
//         else if (*control == 'd') n += 10;  // else if로 d 명령을 검사하고 +=로 현재 수에 10을 더하기
//         else if (*control == 'a') n -= 10;  // else if로 a 명령을 검사하고 -=로 현재 수에서 10을 빼기
//     }  // 블록 끝
//     return n;  // return으로 조작을 모두 적용한 정수를 반환
// }  // 블록 끝

// 풀이 요약
// 조작 문자마다 정해진 증감량을 현재 수에 적용
