# [PCCE 기출문제] 6번 / 물 부족

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/340202) · Level 0 · C++

## 풀이

지난달 사용량에 변동률을 적용해 이번 달 사용량을 계산. 누적 사용량이 저장량보다 커지는 첫 달의 인덱스를 반환

## 코드와 줄별 설명

빈칸 채우기·한 줄 수정 문제. 사이트에는 정해진 부분만 제출했고, 이 파일은 전체 코드에 메모를 붙인 보관용.

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <string>
#include <vector>

using namespace std;

int solution(int storage, int usage, vector<int> change) {
    int total_usage = 0;
    for(int i=0; i<change.size(); i++){
        usage = usage * (100 + change[i]) / 100;
        total_usage += usage;
        if(total_usage > storage){
            return i;
        }
    }
    return -1;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 다룰 string
// #include <vector>  // 길이를 늘릴 수 있는 vector
//
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// int solution(int storage, int usage, vector<int> change) {  // [PCCE 기출문제] 6번 / 물 부족 풀이 시작
//     int total_usage = 0;  // 매달 사용한 물의 누적량
//     for(int i=0; i<change.size(); i++){  // 첫 달부터 사용량 변동률을 차례로 적용
//         usage = usage * (100 + change[i]) / 100;  // 이전 사용량에 100과 변동률의 합을 곱하고 100으로 나눠 이번 달 사용량을 구하기
//         total_usage += usage;  // 이번 달 사용량까지 저장량에서 사용한 총량에 포함
//         if(total_usage > storage){  // 누적 사용량이 저장량을 넘으면 이 달부터 물 부족
//             return i;  // 현재 인덱스 값을 반환하고 함수를 끝
//         }  // 블록 끝
//     }  // 블록 끝
//     return -1;  // 조건을 만족하는 위치가 없으므로 -1을 반환
// }  // 블록 끝

// 풀이 요약
// 지난달 사용량에 변동률을 적용해 이번 달 사용량을 계산. 누적 사용량이 저장량보다 커지는 첫 달의 인덱스를 반환
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:28:40
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_340202_%5BPCCE_%EA%B8%B0%EC%B6%9C%EB%AC%B8%EC%A0%9C%5D_6%EB%B2%88___%EB%AC%BC_%EB%B6%80%EC%A1%B1/README.md)
