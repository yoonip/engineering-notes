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

string solution(vector<string> survey, vector<int> choices) {
    int points[128] = {0};
    for (int i = 0; i < (int)survey.size(); ++i) {
        if (choices[i] < 4) points[(int)survey[i][0]] += 4 - choices[i];
        else if (choices[i] > 4) points[(int)survey[i][1]] += choices[i] - 4;
    }
    string answer;
    for (const string& pair : vector<string>{"RT", "CF", "JM", "AN"}) answer += points[(int)pair[0]] >= points[(int)pair[1]] ? pair[0] : pair[1];
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
// string solution(vector<string> survey, vector<int> choices) {  // 성격 유형 검사하기 풀이 함수 정의
//     int points[128] = {0};  // 성격 문자 코드별 누적 점수를 0으로 초기화
//     for (int i = 0; i < (int)survey.size(); ++i) {  // 문항별 성격 쌍과 선택 점수 확인
//         if (choices[i] < 4) points[(int)survey[i][0]] += 4 - choices[i];  // 비동의 응답이면 첫 성격에 4 - choices[i]점 추가
//         else if (choices[i] > 4) points[(int)survey[i][1]] += choices[i] - 4;  // 동의 응답이면 두 번째 성격에 choices[i] - 4점 추가. 중립은 반영하지 않음
//     }  // 블록 끝
//     string answer;  // 네 성격 문자를 이어 붙일 결과 문자열 준비
//     for (const string& pair : vector<string>{"RT", "CF", "JM", "AN"}) answer += points[(int)pair[0]] >= points[(int)pair[1]] ? pair[0] : pair[1];  // 정해진 네 쌍마다 점수가 높은 문자를 선택하고 동점이면 앞 문자 선택
//     return answer;  // 완성한 네 글자 성격 유형 반환
// }  // 함수 끝
//

// 풀이 요약
// 응답의 중립점 4에서 떨어진 만큼 해당 성격에 점수 추가. 성격 쌍마다 높은 쪽을 고르고 동점이면 사전순 앞 문자 선택.
