#include <vector>
using namespace std;

vector<int> solution(int n, int s) {
    if (s < n) return {-1};
    int quotient = s / n, remainder = s % n;
    vector<int> answer(n, quotient);
    for (int i = n - remainder; i < n; ++i) ++answer[i];
    return answer;
}

// 전체 코드 줄별 설명
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// vector<int> solution(int n, int s) {  // 합을 최대한 고르게 나눠 원소의 곱 최대화
// if (s < n) return {-1};  // 양의 정수 n개의 최소 합보다 작으면 집합이 없음
// int quotient = s / n, remainder = s % n;  // 원소를 최대한 고르게 나눌 몫과 나머지 구하기
// vector<int> answer(n, quotient);  // 모든 원소를 몫으로 초기화
// for (int i = n - remainder; i < n; ++i) ++answer[i];  // 뒤쪽 나머지 개수만큼 1을 더해 오름차순 유지
// return answer;  // 합이 s이고 곱이 최대인 집합 반환
// }  // 블록 끝

// 풀이 요약
// 합을 n으로 나눈 몫을 기본 원소로 두고 나머지 개수만큼 1을 더해 곱이 최대가 되도록 고르게 나누기
