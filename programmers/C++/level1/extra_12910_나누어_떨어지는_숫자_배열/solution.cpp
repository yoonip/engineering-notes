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

vector<int> solution(vector<int> arr, int divisor) {
    vector<int> answer;
    for (int n : arr) if (n % divisor == 0) answer.push_back(n);
    if (answer.empty()) return {-1};
    sort(answer.begin(), answer.end());
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
// vector<int> solution(vector<int> arr, int divisor) {  // 나누어 떨어지는 숫자 배열 풀이 함수 정의
//     vector<int> answer;  // 나누어떨어지는 원소를 담을 배열 준비
//     for (int n : arr) if (n % divisor == 0) answer.push_back(n);  // 나머지가 0인 원소만 결과에 추가
//     if (answer.empty()) return {-1};  // 조건에 맞는 수가 없으면 {-1} 반환
//     sort(answer.begin(), answer.end());  // 선택한 수들을 오름차순 정렬
//     return answer;  // 정렬된 결과 배열 반환
// }  // 함수 끝
//

// 풀이 요약
// divisor로 나누어떨어지는 원소만 모아 정렬. 남는 원소가 없으면 -1 하나 반환.
