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

int solution(int n) {
    vector<bool> prime(n + 1, true); prime[0] = prime[1] = false;
    for (int p = 2; p * p <= n; ++p) if (prime[p]) for (int multiple = p * p; multiple <= n; multiple += p) prime[multiple] = false;
    return count(prime.begin(), prime.end(), true);
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
// int solution(int n) {  // 소수 찾기 풀이 함수 정의
//     vector<bool> prime(n + 1, true); prime[0] = prime[1] = false;  // 0과 1을 제외한 수를 우선 소수로 표시
//     for (int p = 2; p * p <= n; ++p) if (prime[p]) for (int multiple = p * p; multiple <= n; multiple += p) prime[multiple] = false;  // 남은 소수 p마다 p²부터 n까지의 배수를 소수 후보에서 제거
//     return count(prime.begin(), prime.end(), true);  // 끝까지 소수 표시가 남은 원소 수 반환
// }  // 함수 끝
//

// 풀이 요약
// 에라토스테네스의 체로 소수의 배수를 제거. p보다 작은 배수는 이미 처리됐으므로 p²부터 지움.
