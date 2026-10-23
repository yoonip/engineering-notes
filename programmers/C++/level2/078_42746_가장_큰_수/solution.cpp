#include <algorithm>
#include <string>
#include <vector>
using namespace std;

string solution(vector<int> numbers) {
    vector<string> parts;
    for (int number : numbers) parts.push_back(to_string(number));
    sort(parts.begin(), parts.end(), [](const string& a, const string& b) { return a + b > b + a; });
    if (parts[0] == "0") return "0";
    string answer;
    for (const string& part : parts) answer += part;
    return answer;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <string>  // 문자열을 담는 string
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// string solution(vector<int> numbers) {  // 이어 붙인 문자열이 커지는 순서로 정렬
// vector<string> parts;  // 숫자를 연결 순서로 비교할 문자열로 바꾸기
// for (int number : numbers) parts.push_back(to_string(number));  // 각 정수를 문자열로 변환
// sort(parts.begin(), parts.end(), [](const string& a, const string& b) { return a + b > b + a; });  // 두 순서로 이어 붙였을 때 더 큰 순서를 앞에 두기
// if (parts[0] == "0") return "0";  // 모든 수가 0이면 하나의 0만 반환
// string answer;  // 최종 연결 문자열 초기화
// for (const string& part : parts) answer += part;  // 정렬한 순서대로 숫자를 이어 붙이기
// return answer;  // 만들 수 있는 가장 큰 수 반환
// }  // 블록 끝

// 풀이 요약
// 두 수를 이어 붙이는 두 순서를 비교해 정렬하고 전체가 0인 경우는 문자열 0 하나로 처리
