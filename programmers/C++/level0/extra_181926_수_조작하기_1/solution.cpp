#include <string>
using namespace std;

int solution(int n, string control) {
    for (char c : control) {
        if (c == 'w') ++n;
        else if (c == 's') --n;
        else if (c == 'd') n += 10;
        else if (c == 'a') n -= 10;
    }
    return n;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 다룰 string
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// int solution(int n, string control) {  // 수 조작하기 1 풀이 시작
//     for (char c : control) {  // 범위 for로 각 조작 문자를 읽기
//         if (c == 'w') ++n;  // if와 ==로 w 명령을 검사하고 ++로 현재 수에 1을 더하기
//         else if (c == 's') --n;  // else if로 s 명령을 검사하고 --로 현재 수에서 1을 빼기
//         else if (c == 'd') n += 10;  // else if로 d 명령을 검사하고 +=로 현재 수에 10을 더하기
//         else if (c == 'a') n -= 10;  // else if로 a 명령을 검사하고 -=로 현재 수에서 10을 빼기
//     }  // 블록 끝
//     return n;  // return으로 조작을 모두 적용한 정수를 반환
// }  // 블록 끝

// 풀이 요약
// 조작 문자마다 정해진 증감량을 현재 수에 적용
