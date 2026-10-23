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

vector<vector<int>> solution(vector<int> num_list, int n) {
    vector<vector<int>> answer;
    for (size_t i = 0; i < num_list.size(); i += n)
        answer.emplace_back(num_list.begin() + i, num_list.begin() + i + n);
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
// vector<vector<int>> solution(vector<int> num_list, int n) {  // 2차원으로 만들기 풀이 시작
//     vector<vector<int>> answer;  // n개씩 묶은 각 행
//     for (size_t i = 0; i < num_list.size(); i += n)  // 한 행의 시작점을 n개 간격으로 이동
//         answer.emplace_back(num_list.begin() + i, num_list.begin() + i + n);  // answer 끝에 num_list.begin() + i, num_list.begin() + i + n 추가
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 앞에서 n개씩 잘라 한 행으로 만들고 입력 순서대로 모으기
