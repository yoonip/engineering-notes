#include <string>
#include <unordered_map>
#include <vector>
using namespace std;

int solution(vector<vector<string>> clothes) {
    unordered_map<string, int> counts;
    for (const auto& item : clothes) ++counts[item[1]];
    int answer = 1;
    for (const auto& entry : counts) answer *= entry.second + 1;
    return answer - 1;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 담는 string
// #include <unordered_map>  // 키로 값을 찾는 해시 맵
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(vector<vector<string>> clothes) {  // 종류별 선택 수를 곱하고 빈 조합 하나 제외
// unordered_map<string, int> counts;  // 옷 종류별 선택 가능한 개수 세기
// for (const auto& item : clothes) ++counts[item[1]];  // 각 옷의 종류 빈도를 증가시키기
// int answer = 1;  // 종류별 선택 수를 곱할 초기값
// for (const auto& entry : counts) answer *= entry.second + 1;  // 해당 종류를 안 입는 경우 한 가지를 더해 곱하기
// return answer - 1;  // 모든 종류를 안 입는 경우를 제외
// }  // 블록 끝

// 풀이 요약
// 각 의상 종류에서 하나를 고르거나 고르지 않는 경우의 수를 곱하고 아무것도 입지 않는 경우를 제외
