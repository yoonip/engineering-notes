#include <algorithm>
#include <string>
using namespace std;

string solution(int n, int t, int m, int p) {
    string digits = "0123456789ABCDEF", stream;
    for (int number = 0; (int)stream.size() < t * m; ++number) {
        int value = number; string converted;
        do { converted.push_back(digits[value % n]); value /= n; } while (value > 0);
        reverse(converted.begin(), converted.end()); stream += converted;
    }
    string answer;
    for (int i = 0; i < t; ++i) answer += stream[p - 1 + i * m];
    return answer;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <string>  // 문자열을 담는 string
// using namespace std;  // std:: 접두사 생략
// string solution(int n, int t, int m, int p) {  // n진수 자릿수 중 튜브의 차례만 선택
// string digits = "0123456789ABCDEF", stream;  // 진수별 숫자 문자와 전체 발화 순서 저장
// for (int number = 0; (int)stream.size() < t * m; ++number) {  // 필요한 전체 자릿수까지 정수를 순서대로 변환
// int value = number; string converted;  // 현재 수의 진수 변환 결과 초기화
// do { converted.push_back(digits[value % n]); value /= n; } while (value > 0);  // 0도 한 자리로 처리하며 낮은 자릿수부터 구하기
// reverse(converted.begin(), converted.end()); stream += converted;  // 자릿수를 뒤집어 전체 순서에 연결
// }  // 블록 끝
// string answer;  // 튜브가 말할 숫자들 저장
// for (int i = 0; i < t; ++i) answer += stream[p - 1 + i * m];  // p번째 사람의 차례를 m칸 간격으로 읽기
// return answer;  // 튜브의 t개 발화 반환
// }  // 블록 끝

// 풀이 요약
// 정수를 순서대로 n진수로 변환한 전체 자릿수에서 튜브의 차례를 m칸 간격으로 선택
