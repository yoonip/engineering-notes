# 봉인된 주문

[레벨 3 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/389481) · Level 3 · C++

## 풀이

주문을 0 없는 26진수의 원래 순번으로 바꾸어 금지 주문 수만큼 목표 순번을 보정한 뒤 다시 소문자 주문으로 변환

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <algorithm>
#include <string>
#include <vector>
using namespace std;

string solution(long long n, vector<string> bans) {
    vector<long long> removed;
    for (const string& word : bans) {
        long long value = 0;
        for (char c : word) value = value * 26 + c - 'a' + 1;
        removed.push_back(value);
    }
    sort(removed.begin(), removed.end());
    for (long long value : removed) { if (value <= n) ++n; else break; }
    string answer;
    while (n > 0) { --n; answer += char('a' + n % 26); n /= 26; }
    reverse(answer.begin(), answer.end());
    return answer;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <string>  // 문자열을 담는 string
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// string solution(long long n, vector<string> bans) {  // 금지된 주문을 건너뛴 n번째 주문 복원
// vector<long long> removed;  // 금지된 주문의 원래 순번 저장
// for (const string& word : bans) {  // 주문을 0 없는 26진수로 바꾸기
// long long value = 0;  // 현재 주문의 순번 누적
// for (char c : word) value = value * 26 + c - 'a' + 1;  // 각 소문자를 1부터 26까지의 자릿수로 읽기
// removed.push_back(value);  // 금지된 순번을 목록에 넣기
// }  // 블록 끝
// sort(removed.begin(), removed.end());  // 앞에서부터 삭제된 순번을 보정하도록 정렬
// for (long long value : removed) { if (value <= n) ++n; else break; }  // 목표 순번 앞의 금지 주문마다 원래 순번을 한 칸 늘리기
// string answer;  // 선택한 원래 순번의 주문 저장
// while (n > 0) { --n; answer += char('a' + n % 26); n /= 26; }  // 1을 뺀 나머지로 낮은 자릿수부터 소문자 구하기
// reverse(answer.begin(), answer.end());  // 높은 자릿수가 앞에 오도록 뒤집기
// return answer;  // 금지 주문을 제외한 n번째 주문 반환
// }  // 블록 끝

// 풀이 요약
// 주문을 0 없는 26진수의 원래 순번으로 바꾸어 금지 주문 수만큼 목표 순번을 보정한 뒤 다시 소문자 주문으로 변환
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:45:04
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level3/008_389481_%EB%B4%89%EC%9D%B8%EB%90%9C_%EC%A3%BC%EB%AC%B8/README.md)
