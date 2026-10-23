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

int solution(vector<int> arr) {
    int longest = 0;
    for (int value : arr) {
        int steps = 0;
        while (true) {
            int next = value >= 50 && value % 2 == 0 ? value / 2 : value < 50 && value % 2 ? value * 2 + 1 : value;
            if (next == value) break;
            value = next;
            ++steps;
        }
        longest = max(longest, steps);
    }
    return longest;
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
// int solution(vector<int> arr) {  // 조건에 맞게 수열 변환하기 2 풀이 시작
//     int longest = 0;  // 모든 원소 중 가장 오래 걸린 변환 횟수
//     for (int value : arr) {  // 각 원소가 고정되는 시점을 따로 계산
//         int steps = 0;  // 이번 원소의 값이 바뀐 횟수
//         while (true) {  // 다음 값이 현재 값과 같아질 때까지 반복
//             int next = value >= 50 && value % 2 == 0 ? value / 2 : value < 50 && value % 2 ? value * 2 + 1 : value;  // 50 이상 짝수는 절반, 50 미만 홀수는 두 배에 1을 더하고 나머지는 유지
//             if (next == value) break;  // 더 바뀌지 않는 고정값이면 중단
//             value = next;  // 다음 변환의 기준을 방금 얻은 값으로 교체
//             ++steps;  // 실제로 값이 바뀐 횟수 추가
//         }  // 블록 끝
//         longest = max(longest, steps);  // 가장 늦게 고정되는 원소의 횟수 유지
//     }  // 블록 끝
//     return longest;  // 가장 오래 걸리는 변환 횟수 값을 반환하고 함수를 끝
// }  // 블록 끝

// 풀이 요약
// 원소마다 값이 더 바뀌지 않을 때까지의 횟수를 따로 계산. 그 최댓값이 전체 배열이 고정되는 시점
