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

vector<int> solution(vector<int> arr) {
    vector<int> answer;
    for (int value : arr) answer.insert(answer.end(), value, value);
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
// vector<int> solution(vector<int> arr) {  // 배열의 원소만큼 추가하기 풀이 시작
//     vector<int> answer;  // 각 값을 그 값만큼 반복해 담을 배열
//     for (int value : arr) answer.insert(answer.end(), value, value);  // 각 값 value를 value번씩 뒤에 이어 붙이기
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 각 수 a를 a번 반복한 묶음을 입력 순서대로 연결
