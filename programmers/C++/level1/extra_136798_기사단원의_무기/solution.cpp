#include <string>
#include <vector>
#include <algorithm>
#include <numeric>
#include <functional>
#include <unordered_set>
#include <unordered_map>
#include <sstream>
#include <cctype>
#include <cstdlib>
#include <cstdio>
#include <cmath>
#include <queue>
#include <set>
#include <climits>
#include <iostream>
using namespace std;

int solution(int number, int limit, int power) {
    vector<int> counts(number + 1, 0);
    for (int divisor = 1; divisor <= number; ++divisor) for (int multiple = divisor; multiple <= number; multiple += divisor) ++counts[multiple];
    int answer = 0;
    for (int i = 1; i <= number; ++i) answer += counts[i] > limit ? power : counts[i];
    return answer;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열 string 사용 준비
// #include <vector>  // 가변 길이 배열 vector 사용 준비
// #include <algorithm>  // 정렬·탐색·최솟값 등 표준 알고리즘 사용 준비
// #include <numeric>  // gcd·accumulate 등 수치 알고리즘 사용 준비
// #include <functional>  // 함수 래퍼와 greater 등 비교 함수 객체 사용 준비
// #include <unordered_set>  // 중복 없는 원소를 저장하는 해시 집합 사용 준비
// #include <unordered_map>  // 키로 값을 찾는 해시 맵 사용 준비
// #include <sstream>  // 문자열을 토큰으로 나눠 읽을 스트림 사용 준비
// #include <cctype>  // 숫자·대소문자 검사와 변환 함수 사용 준비
// #include <cstdlib>  // 정수 절댓값 등 표준 유틸리티 함수 사용 준비
// #include <cstdio>  // snprintf 등 형식 있는 입출력 함수 사용 준비
// #include <cmath>  // 제곱근 등 수학 함수 사용 준비
// #include <queue>  // FIFO 큐와 우선순위 큐 사용 준비
// #include <set>  // 중복 제거와 정렬을 함께 하는 집합 사용 준비
// #include <climits>  // 정수 범위 상수 사용 준비
// #include <iostream>  // cin·cout 표준 입출력 사용 준비
// using namespace std;  // 표준 이름의 std:: 접두사 생략
//
// int solution(int number, int limit, int power) {  // 기사단원의 무기 풀이 함수 정의
//     vector<int> counts(number + 1, 0);  // 기사 번호별 약수 개수를 0으로 초기화
//     for (int divisor = 1; divisor <= number; ++divisor) for (int multiple = divisor; multiple <= number; multiple += divisor) ++counts[multiple];  // divisor의 모든 배수에 약수 하나를 추가해 번호별 약수 수 계산
//     int answer = 0;  // 필요 철의 총량 answer를 0으로 시작
//     for (int i = 1; i <= number; ++i) answer += counts[i] > limit ? power : counts[i];  // 번호별 약수 수가 limit를 넘으면 power, 아니면 약수 수만큼 철 합산
//     return answer;  // 모든 무기에 필요한 철의 총량 반환
// }  // 함수 끝
//

// 풀이 요약
// 각 수의 배수에 약수 개수를 하나씩 더하는 방식으로 전체 약수 수 계산. 제한을 넘은 기사는 정해진 대체 공격력 사용.
