#include <vector>
using namespace std;

vector<int> solution(vector<int> arr, vector<vector<int>> queries) {
    for (const auto& query : queries) {
        int start = query[0], end = query[1], k = query[2];
        for (int i = start; i <= end; ++i) if (k ? i % k == 0 : i == 0) ++arr[i];
    }
    return arr;
}

// 전체 코드 줄별 설명
// #include <vector>  // 길이를 늘릴 수 있는 vector
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// vector<int> solution(vector<int> arr, vector<vector<int>> queries) {  // 수열과 구간 쿼리 4 풀이 시작
//     for (const auto& query : queries) {  // 범위 for와 const auto 참조로 각 쿼리를 복사 없이 읽기
//         int start = query[0], end = query[1], k = query[2];  // []로 현재 쿼리의 시작, 끝, 배수 기준 k를 읽기
//         for (int i = start; i <= end; ++i) if (k ? i % k == 0 : i == 0) ++arr[i];  // 양 끝을 포함한 구간에서 인덱스가 k의 배수인 원소만 1 증가
//     }  // 블록 끝
//     return arr;  // return으로 모든 쿼리를 적용한 배열을 반환
// }  // 블록 끝

// 풀이 요약
// 각 구간에서 인덱스가 k의 배수인 원소를 1씩 증가
