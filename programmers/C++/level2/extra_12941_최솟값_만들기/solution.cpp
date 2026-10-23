#include <algorithm>
#include <functional>
#include <vector>
using namespace std;

int solution(vector<int> A, vector<int> B) {
    sort(A.begin(), A.end());
    sort(B.begin(), B.end(), greater<int>());
    int answer = 0;
    for (int i = 0; i < (int)A.size(); ++i) answer += A[i] * B[i];
    return answer;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <functional>  // 재귀 람다를 담는 function과 함수 객체
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(vector<int> A, vector<int> B) {  // 한쪽 작은 값과 반대쪽 큰 값을 곱해 합 최소화
// sort(A.begin(), A.end());  // 첫 배열을 작은 값부터 정렬
// sort(B.begin(), B.end(), greater<int>());  // 둘째 배열을 큰 값부터 정렬
// int answer = 0;  // 대응 원소의 곱 합계 초기화
// for (int i = 0; i < (int)A.size(); ++i) answer += A[i] * B[i];  // 작은 값과 큰 값을 짝지어 곱을 더하기
// return answer;  // 만들 수 있는 최소 곱의 합 반환
// }  // 블록 끝

// 풀이 요약
// 한 배열은 오름차순, 다른 배열은 내림차순으로 정렬해 작은 값과 큰 값을 짝지은 곱을 더하기
