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

int solution(vector<int> numbers, int n) {
    int sum = 0;
    for (int value : numbers) { sum += value; if (sum > n) break; }
    return sum;
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
// int solution(vector<int> numbers, int n) {  // n보다 커질 때까지 더하기 풀이 시작
//     int sum = 0;  // 앞에서부터 더한 원소의 합
//     for (int value : numbers) { sum += value; if (sum > n) break; }  // 현재 원소까지 더한 뒤 합이 n을 초과하면 중단
//     return sum;  // 누적 합계 값을 반환하고 함수를 끝
// }  // 블록 끝

// 풀이 요약
// 앞에서부터 더하되 합이 n과 같을 때는 계속하고, n보다 커진 순간의 합 반환
