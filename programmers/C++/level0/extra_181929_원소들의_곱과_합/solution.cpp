#include <vector>
using namespace std;

int solution(vector<int> num_list) {
    long long product = 1, sum = 0;
    for (int value : num_list) {
        product *= value; sum += value;
    }
    return product < sum * sum;
}

// 전체 코드 줄별 설명
// #include <vector>  // 길이를 늘릴 수 있는 vector
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// int solution(vector<int> num_list) {  // 원소들의 곱과 합 풀이 시작
//     long long product = 1, sum = 0;  // 정수 곱과 합을 각각 1과 0으로 초기화하고 long long형으로 계산 범위를 확보
//     for (int value : num_list) {  // 범위 for로 정수 목록의 각 원소를 읽기
//         product *= value; sum += value;  // *=로 현재 원소를 누적 곱에 곱하고 +=로 누적 합에 더하기
//     }  // 블록 끝
//     return product < sum * sum;  // <로 전체 곱과 합의 제곱을 비교해 1 또는 0을 반환
// }  // 블록 끝

// 풀이 요약
// 모든 원소의 곱과 합의 제곱을 계산해 비교
