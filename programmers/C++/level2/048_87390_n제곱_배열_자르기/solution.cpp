#include <algorithm>
#include <vector>
using namespace std;

vector<int> solution(int n, long long left, long long right) {
    vector<int> answer;
    for (long long index = left; index <= right; ++index) {
        long long row = index / n, column = index % n;
        answer.push_back((int)(max(row, column) + 1));
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// vector<int> solution(int n, long long left, long long right) {  // 필요한 일차원 인덱스만 행·열로 복원
// vector<int> answer;  // 잘라낸 구간의 원소 저장
// for (long long index = left; index <= right; ++index) {  // 일차원 인덱스의 요청 구간만 순회
// long long row = index / n, column = index % n;  // 몫과 나머지로 원래 행과 열 복원
// answer.push_back((int)(max(row, column) + 1));  // 행과 열 중 큰 값에 1을 더한 원소 저장
// }  // 블록 끝
// return answer;  // 전체 행렬을 만들지 않고 요청 구간만 반환
// }  // 블록 끝

// 풀이 요약
// 잘라낼 일차원 인덱스만 순회하며 몫과 나머지로 행과 열을 복원하고 두 값 중 큰 값에 1을 더하기
