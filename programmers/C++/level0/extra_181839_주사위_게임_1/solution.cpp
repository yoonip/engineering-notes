#include <string>
#include <vector>
#include <algorithm>
#include <numeric>
#include <functional>
#include <unordered_set>
#include <sstream>
#include <cctype>
#include <cstdlib>
using namespace std;

int solution(int a, int b) {
    if (a % 2 && b % 2) return a * a + b * b;
    if (a % 2 || b % 2) return 2 * (a + b);
    return abs(a - b);
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 다룰 string
// #include <vector>  // 길이를 늘릴 수 있는 vector
// #include <algorithm>  // 정렬·검색·뒤집기 알고리즘
// #include <numeric>  // accumulate·iota 등 수치 연산
// #include <functional>  // greater·multiplies 등 함수 객체
// #include <unordered_set>  // 중복을 거를 해시 집합
// #include <sstream>  // 문자열을 항목별로 읽을 스트림
// #include <cctype>  // 문자 검사와 대소문자 변환
// #include <cstdlib>  // 정수 변환과 절댓값 등 표준 함수
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// int solution(int a, int b) {  // 주사위 게임 1 풀이 시작
//     if (a % 2 && b % 2) return a * a + b * b;  // % 2와 논리 AND로 두 값이 모두 홀수인지 검사하여 참이면 두 제곱의 합을 반환
//     if (a % 2 || b % 2) return 2 * (a + b);  // 앞선 경우를 제외하고 논리 OR가 참이면 한 값만 홀수이므로 두 값의 합에 2를 곱해 반환
//     return abs(a - b);  // 두 값이 모두 짝수인 나머지 경우에는 abs로 차이의 절댓값을 구해 반환
// }  // 블록 끝

// 풀이 요약
// 두 값이 모두 홀수이면 제곱의 합을 반환. 그다음 한 값만 홀수인 경우에는 합의 두 배를, 둘 다 짝수이면 차이의 절댓값을 반환
