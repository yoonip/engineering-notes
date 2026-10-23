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

int solution(int k, int m, vector<int> score) {
    sort(score.rbegin(), score.rend());
    int answer = 0;
    for (int i = m - 1; i < (int)score.size(); i += m) answer += score[i] * m;
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
// int solution(int k, int m, vector<int> score) {  // 과일 장수 풀이 함수 정의
//     sort(score.rbegin(), score.rend());  // 높은 점수 과일부터 묶도록 내림차순 정렬
//     int answer = 0;  // 전체 판매 이익 answer를 0으로 시작
//     for (int i = m - 1; i < (int)score.size(); i += m) answer += score[i] * m;  // m개 묶음의 마지막 원소만 순회하며 묶음 최저 점수 × 사과 수 m을 이익에 추가
//     return answer;  // 완성된 상자들의 총이익 반환
// }  // 함수 끝
//

// 풀이 요약
// 점수를 내림차순 정렬해 m개씩 묶음. 각 묶음의 마지막 점수가 최솟값이므로 여기에 m을 곱해 합산.
