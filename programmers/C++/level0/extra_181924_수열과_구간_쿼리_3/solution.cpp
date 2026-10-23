#include <algorithm>
#include <vector>
using namespace std;

vector<int> solution(vector<int> arr, vector<vector<int>> queries) {
    for (const auto& query : queries) swap(arr[query[0]], arr[query[1]]);
    return arr;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·검색·뒤집기 알고리즘
// #include <vector>  // 길이를 늘릴 수 있는 vector
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// vector<int> solution(vector<int> arr, vector<vector<int>> queries) {  // 수열과 구간 쿼리 3 풀이 시작
//     for (const auto& query : queries) swap(arr[query[0]], arr[query[1]]);  // 범위 for로 쿼리를 읽고 swap으로 지정된 두 원소를 교환
//     return arr;  // return으로 모든 쿼리를 적용한 배열을 반환
// }  // 블록 끝

// 풀이 요약
// 쿼리에 주어진 두 인덱스의 원소를 차례대로 교환
