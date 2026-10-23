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

int solution(string s) {
    int answer = 0, same = 0, different = 0;
    char first = 0;
    for (char c : s) {
        if (same == 0 && different == 0) first = c;
        if (c == first) ++same; else ++different;
        if (same == different) { ++answer; same = different = 0; }
    }
    return answer + (same != 0 || different != 0);
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
// int solution(string s) {  // 문자열 나누기 풀이 함수 정의
//     int answer = 0, same = 0, different = 0;  // 완성한 조각 수 answer와 같은 문자 수 same·다른 문자 수 different를 0으로 초기화
//     char first = 0;  // 현재 조각의 기준 문자 first 준비
//     for (char c : s) {  // 문자열의 문자를 앞에서부터 확인
//         if (same == 0 && different == 0) first = c;  // 새 조각의 시작이면 현재 문자를 기준 문자로 선택
//         if (c == first) ++same; else ++different;  // 기준 문자와 같으면 same, 다르면 different 증가
//         if (same == different) { ++answer; same = different = 0; }  // 두 개수가 같아지면 조각 하나를 완성하고 두 개수 초기화
//     }  // 블록 끝
//     return answer + (same != 0 || different != 0);  // 완성된 조각 수에 아직 남은 조각이 있으면 1을 더해 반환
// }  // 함수 끝
//

// 풀이 요약
// 현재 조각의 첫 문자와 같은 수·다른 수를 셈. 두 수가 같아지면 조각을 끊고, 마지막에 남은 조각도 하나 추가.
