#include <vector>
using namespace std;

vector<int> solution(int n, int k) {
    vector<int> answer;
    for (int value = k; value <= n; value += k) answer.push_back(value);
    return answer;
}

// 전체 코드 줄별 설명
// #include <vector>  // 길이를 늘릴 수 있는 vector
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// vector<int> solution(int n, int k) {  // 배열 만들기 1 풀이 시작
//     vector<int> answer;  // n 이하의 양의 k 배수
//     for (int value = k; value <= n; value += k) answer.push_back(value);  // for로 k부터 k씩 증가시키며 n 이하의 배수를 push_back으로 추가
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// k부터 n까지 k씩 증가시키며 양의 배수를 저장
