# [PCCE 기출문제] 5번 / 심폐소생술

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/340203) · Level 0 · C++

## 풀이

각 입력 단계가 올바른 순서 목록의 몇 번째 원소인지 찾아 1을 더해 저장

## 코드와 줄별 설명

빈칸 채우기·한 줄 수정 문제. 사이트에는 정해진 부분만 제출했고, 이 파일은 전체 코드에 메모를 붙인 보관용.

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <string>
#include <vector>
using namespace std;
vector<int> solution(vector<string> cpr) {
    vector<int> answer = {0, 0, 0, 0, 0};
    vector<string> basic_order = {"check", "call", "pressure", "respiration", "repeat"};
    for(int i=0; i<cpr.size(); i++){
        for(int j=0; j<basic_order.size(); j++){
            if(cpr[i] == basic_order[j]){
                answer[i] = j + 1;
                break;
            }
        }
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 다룰 string
// #include <vector>  // 길이를 늘릴 수 있는 vector
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
// vector<int> solution(vector<string> cpr) {  // [PCCE 기출문제] 5번 / 심폐소생술 풀이 시작
//     vector<int> answer = {0, 0, 0, 0, 0};  // 입력 다섯 단계에 대응하는 결과 배열을 0으로 초기화
//     vector<string> basic_order = {"check", "call", "pressure", "respiration", "repeat"};  // 올바른 순서대로 다섯 단계 이름을 문자열 배열에 저장
//     for(int i=0; i<cpr.size(); i++){  // for문으로 입력 배열의 단계 이름을 처음부터 끝까지 확인
//         for(int j=0; j<basic_order.size(); j++){  // for문으로 올바른 순서 배열의 단계 이름을 차례로 비교
//             if(cpr[i] == basic_order[j]){  // ==로 입력 단계와 표준 단계의 문자열이 같은지 검사
//                 answer[i] = j + 1;  // 0부터 시작하는 인덱스에 1을 더해 실제 단계 번호를 저장
//                 break;  // 일치하는 단계를 찾았으므로 안쪽 반복문을 끝
//             }  // 블록 끝
//         }  // 블록 끝
//     }  // 블록 끝
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 각 입력 단계가 올바른 순서 목록의 몇 번째 원소인지 찾아 1을 더해 저장
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:50:03
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_340203_%5BPCCE_%EA%B8%B0%EC%B6%9C%EB%AC%B8%EC%A0%9C%5D_5%EB%B2%88___%EC%8B%AC%ED%8F%90%EC%86%8C%EC%83%9D%EC%88%A0/README.md)
