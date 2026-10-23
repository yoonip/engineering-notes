#include <string>
#include <vector>
#include <algorithm>
#include <numeric>
#include <cmath>
#include <sstream>
#include <climits>
#include <cctype>
#include <iostream>
#include <functional>

using namespace std;

vector<int> solution(int n) {
    vector<int> answer;
    for (int value = 1; value <= n; value += 2) answer.push_back(value);
    return answer;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 다룰 string
// #include <vector>  // 길이를 늘릴 수 있는 vector
// #include <algorithm>  // 정렬·검색·뒤집기 알고리즘
// #include <numeric>  // accumulate·iota 등 수치 연산
// #include <cmath>  // 제곱근 등 수학 함수
// #include <sstream>  // 문자열을 항목별로 읽을 스트림
// #include <climits>  // INT_MIN·INT_MAX 등 정수 범위 상수
// #include <cctype>  // 문자 검사와 대소문자 변환
// #include <iostream>  // cin·cout 표준 입출력
// #include <functional>  // greater·multiplies 등 함수 객체
//
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// vector<int> solution(int n) {  // 짝수는 싫어요 풀이 시작
//     vector<int> answer;  // 홀수를 발견하는 순서대로 저장할 빈 정수 vector answer를 선언
//     for (int value = 1; value <= n; value += 2) answer.push_back(value);  // int 변수 value를 1부터 시작해 2씩 늘리며 홀수만 생성. value가 n 이하일 때마다 push_back으로 answer 끝에 추가
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 1에서 시작해 2씩 증가시키면 홀수만 얻을 수 있음. n을 넘기 전까지 나온 홀수를 차례대로 결과에 추가
