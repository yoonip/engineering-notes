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

vector<int> solution(vector<vector<int>> score) {
    vector<int> answer(score.size(), 1);
    for (size_t i = 0; i < score.size(); ++i)
        for (const auto& other : score) answer[i] += other[0] + other[1] > score[i][0] + score[i][1];
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
// vector<int> solution(vector<vector<int>> score) {  // 등수 매기기 풀이 시작
//     vector<int> answer(score.size(), 1);  // 각 학생의 등수는 자신보다 높은 사람 수에 1을 더한 값
//     for (size_t i = 0; i < score.size(); ++i)  // 등수를 매길 학생을 하나씩 선택
//         for (const auto& other : score) answer[i] += other[0] + other[1] > score[i][0] + score[i][1];  // 평균 대신 두 점수의 합으로 비교해 더 높은 학생 수 추가
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 자신보다 점수가 높은 학생 수+1이 등수임. 평균 대신 합계를 비교해도 같음
