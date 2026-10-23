#include <string>
#include <vector>
#include <algorithm>
#include <numeric>
#include <functional>
#include <unordered_set>
#include <sstream>
#include <cctype>
#include <cstdlib>
using namespace std;

int solution(string binomial) {
    istringstream stream(binomial);
    int a, b;
    char op;
    stream >> a >> op >> b;
    return op == '+' ? a + b : op == '-' ? a - b : a * b;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 다룰 string
// #include <vector>  // 길이를 늘릴 수 있는 vector
// #include <algorithm>  // 정렬·검색·뒤집기 알고리즘
// #include <numeric>  // accumulate·iota 등 수치 연산
// #include <functional>  // greater·multiplies 등 함수 객체
// #include <unordered_set>  // 중복을 거를 해시 집합
// #include <sstream>  // 문자열을 항목별로 읽을 스트림
// #include <cctype>  // 문자 검사와 대소문자 변환
// #include <cstdlib>  // 정수 변환과 절댓값 등 표준 함수
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// int solution(string binomial) {  // 간단한 식 계산하기 풀이 시작
//     istringstream stream(binomial);  // binomial를 공백 단위로 읽을 스트림 stream
//     int a, b;  // 연산 기호 양쪽의 두 정수
//     char op;  // 더하기·빼기·곱하기를 구분할 기호
//     stream >> a >> op >> b;  // 추출 연산자 >>로 숫자·연산자·숫자를 순서대로 읽기
//     return op == '+' ? a + b : op == '-' ? a - b : a * b;  // 읽은 기호에 맞춰 두 정수의 연산 결과 반환
// }  // 블록 끝

// 풀이 요약
// 문자열을 세 항목으로 나눈 뒤 연산 기호에 맞는 계산을 적용
