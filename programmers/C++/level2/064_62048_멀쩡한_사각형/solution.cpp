#include <numeric>
using namespace std;

long long solution(int w, int h) {
    long long broken = 1LL * w + h - gcd(w, h);
    return 1LL * w * h - broken;
}

// 전체 코드 줄별 설명
// #include <numeric>  // 누적합·최대공약수 같은 수치 알고리즘
// using namespace std;  // std:: 접두사 생략
// long long solution(int w, int h) {  // 대각선이 지나는 칸 수를 전체 넓이에서 빼기
// long long broken = 1LL * w + h - gcd(w, h);  // 격자선을 지나는 대각선이 훼손하는 칸 수 구하기
// return 1LL * w * h - broken;  // 전체 칸 수에서 훼손된 칸 수 빼기
// }  // 블록 끝

// 풀이 요약
// 전체 사각형 넓이에서 대각선이 지나는 w+h-gcd(w,h)개의 칸 빼기
