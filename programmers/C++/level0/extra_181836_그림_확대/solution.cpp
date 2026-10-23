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

vector<string> solution(vector<string> picture, int k) {
    vector<string> answer;
    for (const string& row : picture) {
        string expanded;
        for (char c : row) expanded.append(k, c);
        answer.insert(answer.end(), k, expanded);
    }
    return answer;
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
// vector<string> solution(vector<string> picture, int k) {  // 그림 확대 풀이 시작
//     vector<string> answer;  // 가로와 세로로 k배 늘린 그림의 행들
//     for (const string& row : picture) {  // 원본 그림의 각 행을 가로로 늘리기
//         string expanded;  // 현재 행을 가로로 k배 늘린 문자열
//         for (char c : row) expanded.append(k, c);  // 원래 문자 하나를 k번씩 반복해 가로 확대
//         answer.insert(answer.end(), k, expanded);  // insert로 필요한 값이나 구간을 결과의 끝에 추가
//     }  // 블록 끝
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 문자를 k번 반복해 가로 확대하고 완성된 행을 k번 반복해 세로 확대
