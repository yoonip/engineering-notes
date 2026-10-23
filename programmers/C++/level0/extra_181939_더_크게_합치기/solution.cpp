#include <algorithm>
#include <string>
using namespace std;

int solution(int a, int b) {
    return max(stoi(to_string(a) + to_string(b)), stoi(to_string(b) + to_string(a)));
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·검색·뒤집기 알고리즘
// #include <string>  // 문자열을 다룰 string
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// int solution(int a, int b) {  // 더 크게 합치기 풀이 시작
//     return max(stoi(to_string(a) + to_string(b)), stoi(to_string(b) + to_string(a)));  // to_string과 +로 두 순서의 문자열을 만들고 stoi와 max로 큰 정수를 구하기
// }  // 블록 끝

// 풀이 요약
// 두 정수를 두 순서로 이어 붙이고 더 큰 값을 반환
