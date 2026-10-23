#include <algorithm>
#include <functional>
#include <vector>
using namespace std;

int solution(vector<int> citations) {
    sort(citations.begin(), citations.end(), greater<int>());
    int answer = 0;
    for (int i = 0; i < (int)citations.size(); ++i) {
        if (citations[i] < i + 1) break;
        answer = i + 1;
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <functional>  // 재귀 람다를 담는 function과 함수 객체
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(vector<int> citations) {  // 상위 h편이 h회 이상 인용되는 최대 h 찾기
// sort(citations.begin(), citations.end(), greater<int>());  // 인용 수가 많은 논문부터 정렬
// int answer = 0;  // H-Index 후보를 0으로 초기화
// for (int i = 0; i < (int)citations.size(); ++i) {  // 상위 i+1개 논문의 조건 확인
// if (citations[i] < i + 1) break;  // 현재 논문이 필요한 인용 수보다 작으면 더 늘릴 수 없음
// answer = i + 1;  // 조건을 만족하는 논문 수 기록
// }  // 블록 끝
// return answer;  // 가능한 최대 H-Index 반환
// }  // 블록 끝

// 풀이 요약
// 인용 수를 내림차순 정렬하고 상위 h번째 논문이 h회 이상 인용된 최대 h 찾기
