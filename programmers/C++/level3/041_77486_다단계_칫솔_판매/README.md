# 다단계 칫솔 판매

[레벨 3 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/77486) · Level 3 · C++

## 풀이

판매 수익에서 정수 10퍼센트를 추천인에게 전달하며 더 전달할 금액이 없어질 때까지 수익 누적

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <string>
#include <unordered_map>
#include <vector>
using namespace std;

vector<int> solution(vector<string> enroll, vector<string> referral, vector<string> seller, vector<int> amount) {
    unordered_map<string,int> index; for (int i = 0; i < (int)enroll.size(); ++i) index[enroll[i]] = i;
    vector<int> parent(enroll.size(), -1), profit(enroll.size(), 0);
    for (int i = 0; i < (int)referral.size(); ++i) if (referral[i] != "-") parent[i] = index[referral[i]];
    for (int i = 0; i < (int)seller.size(); ++i) {
        int person = index[seller[i]], money = amount[i] * 100;
        while (person != -1 && money > 0) {
            int share = money / 10; profit[person] += money - share;
            person = parent[person]; money = share;
        }
    }
    return profit;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 담는 string
// #include <unordered_map>  // 키로 값을 찾는 해시 맵
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// vector<int> solution(vector<string> enroll, vector<string> referral, vector<string> seller, vector<int> amount) {  // 추천 관계를 따라 판매 이익의 10%씩 전달
// unordered_map<string,int> index; for (int i = 0; i < (int)enroll.size(); ++i) index[enroll[i]] = i;  // 판매원 이름을 인덱스에 연결
// vector<int> parent(enroll.size(), -1), profit(enroll.size(), 0);  // 추천인과 최종 수익 저장
// for (int i = 0; i < (int)referral.size(); ++i) if (referral[i] != "-") parent[i] = index[referral[i]];  // 추천인이 있으면 부모 인덱스 등록
// for (int i = 0; i < (int)seller.size(); ++i) {  // 각 판매 기록의 수익을 분배
// int person = index[seller[i]], money = amount[i] * 100;  // 판매원과 총 판매 수익 구하기
// while (person != -1 && money > 0) {  // 추천인이 있고 분배금이 남는 동안 위로 전달
// int share = money / 10; profit[person] += money - share;  // 정수로 버린 10퍼센트만 올리고 나머지를 보유
// person = parent[person]; money = share;  // 다음 추천인과 전달 금액으로 이동
// }  // 블록 끝
// }  // 블록 끝
// return profit;  // 등록 순서의 최종 판매 수익 반환
// }  // 블록 끝

// 풀이 요약
// 판매 수익에서 정수 10퍼센트를 추천인에게 전달하며 더 전달할 금액이 없어질 때까지 수익 누적
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:55:22
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level3/041_77486_%EB%8B%A4%EB%8B%A8%EA%B3%84_%EC%B9%AB%EC%86%94_%ED%8C%90%EB%A7%A4/README.md)
