#include <algorithm>
#include <climits>
#include <sstream>
#include <string>
using namespace std;

string solution(string s) {
    istringstream input(s); int value, lowest = INT_MAX, highest = INT_MIN;
    while (input >> value) { lowest = min(lowest, value); highest = max(highest, value); }
    return to_string(lowest) + " " + to_string(highest);
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <climits>  // 정수 자료형의 최솟값·최댓값
// #include <sstream>  // 문자열에서 공백 단위로 값을 읽는 스트림
// #include <string>  // 문자열을 담는 string
// using namespace std;  // std:: 접두사 생략
// string solution(string s) {  // 공백으로 구분된 정수의 최솟값·최댓값 찾기
// istringstream input(s); int value, lowest = INT_MAX, highest = INT_MIN;  // 정수 입력 스트림과 최솟값 및 최댓값 초기화
// while (input >> value) { lowest = min(lowest, value); highest = max(highest, value); }  // 문자열의 모든 정수를 읽어 두 경계 갱신
// return to_string(lowest) + " " + to_string(highest);  // 최솟값과 최댓값을 공백으로 연결해 반환
// }  // 블록 끝

// 풀이 요약
// 문자열에서 모든 정수를 읽어 최솟값과 최댓값을 구한 뒤 공백으로 연결
