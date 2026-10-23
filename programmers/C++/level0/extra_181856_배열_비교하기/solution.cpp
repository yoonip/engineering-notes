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

int solution(vector<int> arr1, vector<int> arr2) {
    if (arr1.size() != arr2.size()) return arr1.size() > arr2.size() ? 1 : -1;
    int sum1 = accumulate(arr1.begin(), arr1.end(), 0), sum2 = accumulate(arr2.begin(), arr2.end(), 0);
    return (sum1 > sum2) - (sum1 < sum2);
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
// int solution(vector<int> arr1, vector<int> arr2) {  // 배열 비교하기 풀이 시작
//     if (arr1.size() != arr2.size()) return arr1.size() > arr2.size() ? 1 : -1;  // 길이가 다르면 더 긴 배열을 큰 쪽으로 판정
//     int sum1 = accumulate(arr1.begin(), arr1.end(), 0), sum2 = accumulate(arr2.begin(), arr2.end(), 0);  // 길이가 같은 경우 두 배열의 원소 합을 따로 계산
//     return (sum1 > sum2) - (sum1 < sum2);  // 첫 합이 크면 1, 작으면 -1, 같으면 0
// }  // 블록 끝

// 풀이 요약
// 배열 길이를 먼저 비교하고 길이가 같을 때만 원소 합을 비교. 두 기준이 모두 같으면 0
