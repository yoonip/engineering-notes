# [PCCP 기출문제] 4번 / 수식 복원하기

[레벨 3 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/340210) · Level 3 · C++

## 풀이

알려진 수식을 모두 만족하는 진법을 추리고 지워진 결과를 각 후보 진법에서 계산해 모두 같은 문자열일 때만 확정하기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <algorithm>
#include <array>
#include <sstream>
#include <string>
#include <vector>
using namespace std;

vector<string> solution(vector<string> expressions) {
    vector<array<string, 5>> parsed; int minimum = 2;
    for (const string& expression : expressions) {
        array<string, 5> parts; istringstream input(expression); for (string& part : parts) input >> part;
        parsed.push_back(parts);
        for (char c : expression) if (c >= '0' && c <= '9') minimum = max(minimum, c - '0' + 1);
    }
    auto decode = [](const string& text, int base) { int value = 0; for (char c : text) value = value * base + c - '0'; return value; };
    auto calculate = [&](const array<string, 5>& parts, int base) { int a = decode(parts[0], base), b = decode(parts[2], base); return parts[1] == "+" ? a + b : a - b; };
    vector<int> bases;
    for (int base = minimum; base <= 9; ++base) {
        bool valid = true;
        for (const auto& parts : parsed) if (parts[4] != "X" && calculate(parts, base) != decode(parts[4], base)) valid = false;
        if (valid) bases.push_back(base);
    }
    auto encode = [](int value, int base) {
        string result; do { result += char('0' + value % base); value /= base; } while (value > 0);
        reverse(result.begin(), result.end()); return result;
    };
    vector<string> answer;
    for (const auto& parts : parsed) if (parts[4] == "X") {
        string result; bool unique = true;
        for (int base : bases) { string current = encode(calculate(parts, base), base); if (result.empty()) result = current; else if (result != current) unique = false; }
        answer.push_back(parts[0] + " " + parts[1] + " " + parts[2] + " = " + (unique ? result : "?"));
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <array>  // 크기가 고정된 array
// #include <sstream>  // 문자열에서 공백 단위로 값을 읽는 스트림
// #include <string>  // 문자열을 담는 string
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// vector<string> solution(vector<string> expressions) {  // 가능한 진법을 추려 지워진 수식 결과 복원
// vector<array<string, 5>> parsed; int minimum = 2;  // 분리한 수식과 가능한 진법의 최솟값 저장
// for (const string& expression : expressions) {  // 수식을 공백으로 나누어 읽기
// array<string, 5> parts; istringstream input(expression); for (string& part : parts) input >> part;  // 피연산자, 연산자, 등호, 결과를 분리
// parsed.push_back(parts);  // 분리한 수식 저장
// for (char c : expression) if (c >= '0' && c <= '9') minimum = max(minimum, c - '0' + 1);  // 등장한 숫자보다 큰 진법만 후보로 두기
// }  // 블록 끝
// auto decode = [](const string& text, int base) { int value = 0; for (char c : text) value = value * base + c - '0'; return value; };  // 주어진 진법의 문자열을 십진 정수로 읽기
// auto calculate = [&](const array<string, 5>& parts, int base) { int a = decode(parts[0], base), b = decode(parts[2], base); return parts[1] == "+" ? a + b : a - b; };  // 진법에 맞게 두 피연산자 계산
// vector<int> bases;  // 이미 알려진 모든 수식을 만족하는 진법 저장
// for (int base = minimum; base <= 9; ++base) {  // 가능한 진법을 차례대로 검사
// bool valid = true;  // 현재 진법이 모순 없다고 초기화
// for (const auto& parts : parsed) if (parts[4] != "X" && calculate(parts, base) != decode(parts[4], base)) valid = false;  // 알려진 결과와 다른 수식이 있는지 검사
// if (valid) bases.push_back(base);  // 모든 수식에 맞는 진법만 남기기
// }  // 블록 끝
// auto encode = [](int value, int base) {  // 계산 결과를 해당 진법 문자열로 바꾸기
// string result; do { result += char('0' + value % base); value /= base; } while (value > 0);  // 0도 한 자리로 처리해 낮은 자릿수부터 구하기
// reverse(result.begin(), result.end()); return result;  // 자릿수 순서를 바로잡아 반환
// };  // 블록 끝
// vector<string> answer;  // X를 복원한 수식들 저장
// for (const auto& parts : parsed) if (parts[4] == "X") {  // 결과가 지워진 수식만 복원
// string result; bool unique = true;  // 모든 후보 진법에서 결과가 같은지 확인
// for (int base : bases) { string current = encode(calculate(parts, base), base); if (result.empty()) result = current; else if (result != current) unique = false; }  // 진법별로 계산한 문자열 결과 비교
// answer.push_back(parts[0] + " " + parts[1] + " " + parts[2] + " = " + (unique ? result : "?"));  // 결과가 하나로 정해지지 않으면 물음표 넣기
// }  // 블록 끝
// return answer;  // 복원한 수식 목록 반환
// }  // 블록 끝

// 풀이 요약
// 알려진 수식을 모두 만족하는 진법을 추리고 지워진 결과를 각 후보 진법에서 계산해 모두 같은 문자열일 때만 확정하기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:46:01
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level3/010_340210_%5BPCCP_%EA%B8%B0%EC%B6%9C%EB%AC%B8%EC%A0%9C%5D_4%EB%B2%88___%EC%88%98%EC%8B%9D_%EB%B3%B5%EC%9B%90%ED%95%98%EA%B8%B0/README.md)
