#include <algorithm>
#include <string>
using namespace std;

int solution(int a, int b) {
    return max(stoi(to_string(a) + to_string(b)), 2 * a * b);
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·검색·뒤집기 알고리즘
// #include <string>  // 문자열을 다룰 string
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// int solution(int a, int b) {  // 두 수의 연산값 비교하기 풀이 시작
//     return max(stoi(to_string(a) + to_string(b)), 2 * a * b);  // to_string으로 연결한 수를 stoi로 정수화하고 max로 2ab와 비교
// }  // 블록 끝

// 풀이 요약
// a와 b를 이어 붙인 수와 2ab를 계산한 뒤 큰 값을 반환
