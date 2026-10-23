#include <vector>
using namespace std;

vector<int> solution(vector<int> num_list) {
    int last = num_list.back(), previous = num_list[num_list.size() - 2];
    num_list.push_back(last > previous ? last - previous : last * 2);
    return num_list;
}

// 전체 코드 줄별 설명
// #include <vector>  // 길이를 늘릴 수 있는 vector
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// vector<int> solution(vector<int> num_list) {  // 마지막 두 원소 풀이 시작
//     int last = num_list.back(), previous = num_list[num_list.size() - 2];  // back과 []로 마지막 원소와 직전 원소를 각각 저장
//     num_list.push_back(last > previous ? last - previous : last * 2);  // 삼항 연산자로 추가할 값을 고르고 push_back으로 배열 끝에 넣기
//     return num_list;  // return으로 새 원소를 추가한 배열을 반환
// }  // 블록 끝

// 풀이 요약
// 마지막 값이 직전 값보다 크면 차이를, 아니면 마지막 값의 두 배를 추가
