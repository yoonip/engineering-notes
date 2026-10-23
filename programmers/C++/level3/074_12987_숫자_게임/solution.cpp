#include <algorithm>
#include <vector>
using namespace std;

int solution(vector<int> A, vector<int> B) {
    sort(A.begin(), A.end()); sort(B.begin(), B.end());
    int wins = 0;
    for (int number : B) if (wins < (int)A.size() && number > A[wins]) ++wins;
    return wins;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(vector<int> A, vector<int> B) {  // B의 작은 수부터 이길 수 있는 가장 작은 A와 연결
// sort(A.begin(), A.end()); sort(B.begin(), B.end());  // 두 팀의 숫자를 오름차순으로 정렬
// int wins = 0;  // 아직 이기지 못한 A의 가장 작은 숫자 위치를 나타냄
// for (int number : B) if (wins < (int)A.size() && number > A[wins]) ++wins;  // 현재 B 숫자로 이길 수 있는 가장 작은 A 숫자 처리
// return wins;  // B가 얻을 수 있는 최대 승점 반환
// }  // 블록 끝

// 풀이 요약
// 두 팀의 숫자를 정렬하고 B의 작은 숫자부터 이길 수 있는 가장 작은 A의 숫자와 짝지어 최대 승점 구하기
