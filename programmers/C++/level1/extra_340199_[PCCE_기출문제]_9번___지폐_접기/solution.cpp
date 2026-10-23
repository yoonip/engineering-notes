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

int solution(vector<int> wallet, vector<int> bill) {
    sort(wallet.begin(), wallet.end()); sort(bill.begin(), bill.end());
    int answer = 0;
    while (bill[0] > wallet[0] || bill[1] > wallet[1]) {
        bill[1] /= 2; sort(bill.begin(), bill.end()); ++answer;
    }
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
// int solution(vector<int> wallet, vector<int> bill) {  // [PCCE 기출문제] 9번 / 지폐 접기 풀이 함수 정의
//     sort(wallet.begin(), wallet.end()); sort(bill.begin(), bill.end());  // 지갑과 지폐를 각각 짧은 변, 긴 변 순서로 정렬
//     int answer = 0;  // 접은 횟수 answer를 0으로 시작
//     while (bill[0] > wallet[0] || bill[1] > wallet[1]) {  // 짧은 변이나 긴 변 중 하나라도 지갑보다 크면 계속 접음
//         bill[1] /= 2; sort(bill.begin(), bill.end()); ++answer;  // 지폐의 긴 변을 절반으로 접고 변 순서를 다시 맞춘 뒤 횟수 증가
//     }  // 블록 끝
//     return answer;  // 지갑에 들어갈 때까지 접은 횟수 반환
// }  // 함수 끝
//

// 풀이 요약
// 지갑과 지폐의 짧은 변·긴 변을 정렬해 비교. 들어가지 않으면 지폐의 긴 변을 절반으로 접고 다시 정렬.
