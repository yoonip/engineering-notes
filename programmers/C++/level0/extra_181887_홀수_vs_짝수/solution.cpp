#include <string>
#include <vector>
#include <algorithm>
#include <numeric>
#include <functional>
#include <unordered_set>
#include <sstream>
#include <cctype>
#include <cstdlib>
using namespace std;

int solution(vector<int> num_list) {
    int sums[2] = {0, 0};
    for (int i = 0; i < (int)num_list.size(); ++i) sums[i % 2] += num_list[i];
    return max(sums[0], sums[1]);
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 다룰 string
// #include <vector>  // 길이를 늘릴 수 있는 vector
// #include <algorithm>  // 정렬·검색·뒤집기 알고리즘
// #include <numeric>  // accumulate·iota 등 수치 연산
// #include <functional>  // greater·multiplies 등 함수 객체
// #include <unordered_set>  // 중복을 거를 해시 집합
// #include <sstream>  // 문자열을 항목별로 읽을 스트림
// #include <cctype>  // 문자 검사와 대소문자 변환
// #include <cstdlib>  // 정수 변환과 절댓값 등 표준 함수
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// int solution(vector<int> num_list) {  // 홀수 vs 짝수 풀이 시작
//     int sums[2] = {0, 0};  // 홀수 번째와 짝수 번째 원소의 합을 나눠 저장
//     for (int i = 0; i < (int)num_list.size(); ++i) sums[i % 2] += num_list[i];  // 인덱스 홀짝으로 순번을 구분해 각 합계에 더하기
//     return max(sums[0], sums[1]);  // 두 순번 그룹의 합 중 큰 값
// }  // 블록 끝

// 풀이 요약
// 원소의 값이 홀수인지가 아니라 원소의 순번이 홀수·짝수인지 구분
