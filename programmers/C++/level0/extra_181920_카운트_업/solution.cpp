#include <vector>
using namespace std;

vector<int> solution(int start_num, int end_num) {
    vector<int> answer;
    for (int value = start_num; value <= end_num; ++value) answer.push_back(value);
    return answer;
}

// 전체 코드 줄별 설명
// #include <vector>  // 길이를 늘릴 수 있는 vector
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// vector<int> solution(int start_num, int end_num) {  // 카운트 업 풀이 시작
//     vector<int> answer;  // 시작값부터 끝값까지의 증가 수열
//     for (int value = start_num; value <= end_num; ++value) answer.push_back(value);  // for로 시작값부터 끝값까지 1씩 증가시키며 push_back으로 저장
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 시작값부터 끝값까지 1씩 증가하는 정수를 저장
