#include <string>
#include <vector>
#include <algorithm>
#include <numeric>
#include <functional>
#include <unordered_set>
#include <unordered_map>
#include <sstream>
#include <cctype>
#include <cstdlib>
#include <cstdio>
#include <cmath>
#include <queue>
#include <set>
#include <climits>
#include <iostream>
using namespace std;

vector<int> solution(vector<int> answers) {
    vector<vector<int>> patterns = {{1,2,3,4,5}, {2,1,2,3,2,4,2,5}, {3,3,1,1,2,2,4,4,5,5}};
    int score[3] = {0,0,0};
    for (int i = 0; i < (int)answers.size(); ++i) for (int j = 0; j < 3; ++j) if (answers[i] == patterns[j][i % patterns[j].size()]) ++score[j];
    vector<int> answer;
    for (int j = 0; j < 3; ++j) if (score[j] == *max_element(score, score + 3)) answer.push_back(j + 1);
    return answer;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열 string 사용 준비
// #include <vector>  // 가변 길이 배열 vector 사용 준비
// #include <algorithm>  // 정렬·탐색·최솟값 등 표준 알고리즘 사용 준비
// #include <numeric>  // gcd·accumulate 등 수치 알고리즘 사용 준비
// #include <functional>  // 함수 래퍼와 greater 등 비교 함수 객체 사용 준비
// #include <unordered_set>  // 중복 없는 원소를 저장하는 해시 집합 사용 준비
// #include <unordered_map>  // 키로 값을 찾는 해시 맵 사용 준비
// #include <sstream>  // 문자열을 토큰으로 나눠 읽을 스트림 사용 준비
// #include <cctype>  // 숫자·대소문자 검사와 변환 함수 사용 준비
// #include <cstdlib>  // 정수 절댓값 등 표준 유틸리티 함수 사용 준비
// #include <cstdio>  // snprintf 등 형식 있는 입출력 함수 사용 준비
// #include <cmath>  // 제곱근 등 수학 함수 사용 준비
// #include <queue>  // FIFO 큐와 우선순위 큐 사용 준비
// #include <set>  // 중복 제거와 정렬을 함께 하는 집합 사용 준비
// #include <climits>  // 정수 범위 상수 사용 준비
// #include <iostream>  // cin·cout 표준 입출력 사용 준비
// using namespace std;  // 표준 이름의 std:: 접두사 생략
//
// vector<int> solution(vector<int> answers) {  // 모의고사 풀이 함수 정의
//     vector<vector<int>> patterns = {{1,2,3,4,5}, {2,1,2,3,2,4,2,5}, {3,3,1,1,2,2,4,4,5,5}};  // 세 수포자의 반복 답안 패턴 저장
//     int score[3] = {0,0,0};  // 세 사람의 맞힌 개수를 각각 0으로 초기화
//     for (int i = 0; i < (int)answers.size(); ++i) for (int j = 0; j < 3; ++j) if (answers[i] == patterns[j][i % patterns[j].size()]) ++score[j];  // 각 문항에서 패턴 길이의 나머지 위치와 정답을 비교해 점수 증가
//     vector<int> answer;  // 최고 득점자 번호를 담을 결과 배열 준비
//     for (int j = 0; j < 3; ++j) if (score[j] == *max_element(score, score + 3)) answer.push_back(j + 1);  // 각 사람의 점수가 전체 최댓값이면 1기준 번호를 결과에 추가
//     return answer;  // 공동 최고 득점자를 번호순으로 반환
// }  // 함수 끝
//

// 풀이 요약
// 세 사람의 반복 패턴과 정답을 비교해 점수 계산. 최고 점수와 같은 사람을 번호순으로 전부 선택.
