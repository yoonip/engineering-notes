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
    int answer = 0;
    while (n > 0) { answer = answer * 3 + n % 3; n /= 3; }
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
// int solution(int n) {  // 3진법 뒤집기 풀이 함수 정의
//     int answer = 0;  // 뒤집힌 3진수의 값을 담을 answer를 0으로 시작
//     while (n > 0) { answer = answer * 3 + n % 3; n /= 3; }  // 현재 3진수 끝자리를 결과 뒤에 붙이고 원래 수의 끝자리 제거
//     return answer;  // 뒤집힌 3진수를 십진수로 계산한 값 반환
// }  // 함수 끝
//

// 풀이 요약
// n을 3으로 나눈 나머지를 낮은 자리부터 꺼냄. 꺼낸 순서대로 결과 × 3에 붙이면 뒤집힌 3진수의 십진값이 됨.
