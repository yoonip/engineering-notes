#include <climits>
#include <vector>
using namespace std;

int solution(vector<int> a) {
    int answer = 0, minimum = INT_MAX;
    for (int value : a) if (value < minimum) { ++answer; minimum = value; }
    minimum = INT_MAX;
    for (auto it = a.rbegin(); it != a.rend(); ++it) if (*it < minimum) { ++answer; minimum = *it; }
    return answer - 1;
}

// 전체 코드 줄별 설명
// #include <climits>  // 정수 자료형의 최솟값·최댓값
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(vector<int> a) {  // 양쪽 최솟값으로 끝까지 남을 수 있는 풍선 판정
// int answer = 0, minimum = INT_MAX;  // 한쪽 방향의 새 최솟값 수 세기
// for (int value : a) if (value < minimum) { ++answer; minimum = value; }  // 왼쪽에서 새 최솟값이 되는 풍선은 남길 수 있음
// minimum = INT_MAX;  // 반대쪽 탐색의 최솟값 초기화
// for (auto it = a.rbegin(); it != a.rend(); ++it) if (*it < minimum) { ++answer; minimum = *it; }  // 오른쪽에서도 새 최솟값 풍선 세기
// return answer - 1;  // 양쪽에서 중복한 전체 최솟값 하나 빼기
// }  // 블록 끝

// 풀이 요약
// 왼쪽 또는 오른쪽에서 새 최솟값이 되는 풍선들을 세고 두 방향에서 중복한 전체 최솟값 하나 빼기
