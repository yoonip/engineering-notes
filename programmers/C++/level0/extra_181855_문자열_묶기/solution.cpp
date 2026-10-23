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

int solution(vector<string> strArr) {
    int counts[31] = {0}, answer = 0;
    for (const string& text : strArr) answer = max(answer, ++counts[text.size()]);
    return answer;
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
// int solution(vector<string> strArr) {  // 문자열 묶기 풀이 시작
//     int counts[31] = {0}, answer = 0;  // 길이별 문자열 개수를 담을 counts 배열과 최대 그룹 크기 answer를 모두 0으로 초기화
//     for (const string& text : strArr) answer = max(answer, ++counts[text.size()]);  // const string&로 문자열을 복사하지 않고 순회하며 해당 길이의 개수를 먼저 늘린 뒤 max로 최댓값을 갱신
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 문자열의 길이를 counts의 인덱스로 사용해 같은 길이의 개수를 세기. 개수가 늘 때마다 answer와 비교하여 가장 큰 그룹의 크기를 유지
