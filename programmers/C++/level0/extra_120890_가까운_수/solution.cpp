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

int solution(vector<int> array, int n) {
    int answer = array[0];
    for (int value : array)
        if (abs(value - n) < abs(answer - n) || (abs(value - n) == abs(answer - n) && value < answer)) answer = value;
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
// int solution(vector<int> array, int n) {  // 가까운 수 풀이 시작
//     int answer = array[0];  // 첫 원소 array[0]을 현재까지 가장 가까운 수 answer로 정하여 비교를 시작
//     for (int value : array)  // 범위 기반 for로 배열의 각 후보 원소를 value에 읽기
//         if (abs(value - n) < abs(answer - n) || (abs(value - n) == abs(answer - n) && value < answer)) answer = value;  // abs로 후보와 n의 거리, 현재 answer와 n의 거리를 비교. 후보의 거리가 더 작거나, 거리가 같으면서 후보 값이 더 작을 때만 answer를 교체
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 각 원소와 n의 절댓값 차이를 비교. 거리가 더 가까운 원소를 선택하고, 거리가 같으면 더 작은 원소를 선택
