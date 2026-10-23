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

vector<int> solution(vector<int> emergency) {
    vector<int> answer(emergency.size(), 1);
    for (size_t i = 0; i < emergency.size(); ++i)
        for (int value : emergency) answer[i] += value > emergency[i];
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
// vector<int> solution(vector<int> emergency) {  // 진료순서 정하기 풀이 시작
//     vector<int> answer(emergency.size(), 1);  // 자신보다 높은 응급도 인원 수에 1을 더한 순위
//     for (size_t i = 0; i < emergency.size(); ++i)  // 각 환자의 순위를 따로 계산
//         for (int value : emergency) answer[i] += value > emergency[i];  // 현재 환자보다 응급도가 높은 사람마다 순위를 1씩 뒤로
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 각 환자보다 응급도가 높은 사람 수를 세어 1을 더하면 진료 순서. 결과는 원래 입력 순서에 맞춰 기록
