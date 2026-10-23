#include <numeric>
#include <vector>
using namespace std;

int solution(vector<int> arr) {
    int answer = 1;
    for (int number : arr) answer = answer / gcd(answer, number) * number;
    return answer;
}

// 전체 코드 줄별 설명
// #include <numeric>  // 누적합·최대공약수 같은 수치 알고리즘
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(vector<int> arr) {  // 두 수의 최소공배수를 배열 전체에 누적
// int answer = 1;  // 최소공배수의 초기값을 1로 두기
// for (int number : arr) answer = answer / gcd(answer, number) * number;  // 최대공약수로 먼저 나눈 뒤 현재 수를 곱해 최소공배수 누적
// return answer;  // 모든 수의 최소공배수 반환
// }  // 블록 끝

// 풀이 요약
// 두 수의 최소공배수를 최대공약수로 계산하는 과정을 배열 전체에 누적
