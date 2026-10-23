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

int solution(vector<vector<int>> lines) {
    int covered[200] = {}, answer = 0;
    for (const auto& line : lines)
        for (int x = line[0]; x < line[1]; ++x) ++covered[x + 100];
    for (int count : covered) answer += count >= 2;
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
// int solution(vector<vector<int>> lines) {  // 겹치는 선분의 길이 풀이 시작
//     int covered[200] = {}, answer = 0;  // 길이 1인 각 구간을 덮는 선분 수와 겹친 총길이
//     for (const auto& line : lines)  // 세 선분을 하나씩 구간에 표시
//         for (int x = line[0]; x < line[1]; ++x) ++covered[x + 100];  // [x, x+1] 구간의 덮임 수 증가, 음수 좌표는 100만큼 옮기기
//     for (int count : covered) answer += count >= 2;  // 두 선분 이상이 덮은 단위 구간만 길이에 포함
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 점이 아니라 길이 1인 구간의 덮인 횟수를 세면 끝점만 만나는 경우를 길이에 포함하지 않음
