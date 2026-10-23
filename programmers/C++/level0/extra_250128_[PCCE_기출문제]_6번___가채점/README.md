# [PCCE 기출문제] 6번 / 가채점

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/250128) · Level 0 · C++

## 풀이

문의한 학생의 번호에서 1을 뺀 위치로 실제 성적을 조회. 그 성적과 문의 순서의 가채점 성적을 비교

## 코드와 줄별 설명

빈칸 채우기·한 줄 수정 문제. 사이트에는 정해진 부분만 제출했고, 이 파일은 전체 코드에 메모를 붙인 보관용.

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <string>
#include <vector>

using namespace std;

vector<string> solution(vector<int> numbers, vector<int> our_score, vector<int> score_list) {
    int num_student = numbers.size();
    vector<string> answer(num_student);
    
    for (int i = 0; i < num_student; i++) {
        if (our_score[i] == score_list[numbers[i] - 1]) {
            answer[i] = "Same";
        }
        else {
            answer[i] = "Different";
        }
    }
    
    return answer;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 다룰 string
// #include <vector>  // 길이를 늘릴 수 있는 vector
//
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// vector<string> solution(vector<int> numbers, vector<int> our_score, vector<int> score_list) {  // [PCCE 기출문제] 6번 / 가채점 풀이 시작
//     int num_student = numbers.size();  // num_student에 numbers의 길이 저장
//     vector<string> answer(num_student);  // 문의 학생마다 성적 일치 여부를 담을 결과
//
//     for (int i = 0; i < num_student; i++) {  // 문의한 학생 순서대로 성적 비교
//         if (our_score[i] == score_list[numbers[i] - 1]) {  // 학생 번호를 0부터 세는 인덱스로 바꾸고 실제 성적과 가채점 성적을 비교
//             answer[i] = "Same";  // 가채점 점수가 실제 점수와 일치
//         }  // 블록 끝
//         else {  // 가채점 점수와 실제 점수가 다른 경우
//             answer[i] = "Different";  // 해당 학생의 점수가 다르다고 기록
//         }  // 블록 끝
//     }  // 블록 끝
//
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 문의한 학생의 번호에서 1을 뺀 위치로 실제 성적을 조회. 그 성적과 문의 순서의 가채점 성적을 비교
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:31:57
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_250128_%5BPCCE_%EA%B8%B0%EC%B6%9C%EB%AC%B8%EC%A0%9C%5D_6%EB%B2%88___%EA%B0%80%EC%B1%84%EC%A0%90/README.md)
