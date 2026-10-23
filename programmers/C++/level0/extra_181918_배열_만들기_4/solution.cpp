#include <vector>
using namespace std;

vector<int> solution(vector<int> arr) {
    vector<int> answer;
    for (int value : arr) {
        while (!answer.empty() && answer.back() >= value) answer.pop_back();
        answer.push_back(value);
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <vector>  // 길이를 늘릴 수 있는 vector
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// vector<int> solution(vector<int> arr) {  // 배열 만들기 4 풀이 시작
//     vector<int> answer;  // 작은 값부터 남겨 둘 결과 스택
//     for (int value : arr) {  // 범위 for로 배열의 값을 입력 순서대로 읽기
//         while (!answer.empty() && answer.back() >= value) answer.pop_back();  // 스택이 비지 않고 끝값이 현재 값 이상인 동안 pop_back으로 끝 원소를 제거
//         answer.push_back(value);  // push_back으로 현재 정수를 결과 vector 끝에 추가
//     }  // 블록 끝
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 현재 값 이상인 스택 끝 원소를 제거한 뒤 현재 값을 넣기
