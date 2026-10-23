# 표현 가능한 이진트리

[레벨 3 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/150367) · Level 3 · C++

## 풀이

이진수를 포화 이진트리 길이로 채운 뒤 중위 순회의 중앙 루트가 0이면 자손에 1이 없는지 재귀 검사

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <algorithm>
#include <functional>
#include <string>
#include <vector>
using namespace std;

vector<int> solution(vector<long long> numbers) {
    vector<int> answer;
    for (long long number : numbers) {
        string bits; do { bits += char('0' + number % 2); number /= 2; } while (number > 0);
        reverse(bits.begin(), bits.end()); int size = 1;
        while (size < (int)bits.size()) size = 2 * size + 1;
        bits = string(size - bits.size(), '0') + bits;
        function<bool(int, int)> valid = [&](int left, int right) {
            if (right - left == 1) return true;
            int middle = (left + right) / 2;
            if (bits[middle] == '0') return bits.find('1', left) >= (size_t)right;
            return valid(left, middle) && valid(middle + 1, right);
        };
        answer.push_back(valid(0, size));
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <functional>  // 재귀 람다를 담는 function과 함수 객체
// #include <string>  // 문자열을 담는 string
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// vector<int> solution(vector<long long> numbers) {  // 포화 이진트리에서 0인 부모 아래 1이 있는지 검사
// vector<int> answer;  // 각 수의 이진트리 표현 가능 여부 저장
// for (long long number : numbers) {  // 입력 정수를 하나씩 검사
// string bits; do { bits += char('0' + number % 2); number /= 2; } while (number > 0);  // 정수를 이진수로 바꾸기
// reverse(bits.begin(), bits.end()); int size = 1;  // 높은 비트가 앞으로 오도록 뒤집고 포화 트리 크기 초기화
// while (size < (int)bits.size()) size = 2 * size + 1;  // 비트 수 이상인 포화 이진트리 노드 수 구하기
// bits = string(size - bits.size(), '0') + bits;  // 앞에 가짜 노드 0 채우기
// function<bool(int, int)> valid = [&](int left, int right) {  // 중위 순회 구간이 유효한 트리인지 검사
// if (right - left == 1) return true;  // 잎 노드는 0이나 1 모두 가능
// int middle = (left + right) / 2;  // 현재 서브트리의 루트 비트 찾기
// if (bits[middle] == '0') return bits.find('1', left) >= (size_t)right;  // 가짜 루트 아래에는 실제 노드 1이 없어야 함
// return valid(left, middle) && valid(middle + 1, right);  // 실제 루트이면 양쪽 서브트리 검사
// };  // 블록 끝
// answer.push_back(valid(0, size));  // 전체 트리의 검사 결과 기록
// }  // 블록 끝
// return answer;  // 표현 가능 여부 목록 반환
// }  // 블록 끝

// 풀이 요약
// 이진수를 포화 이진트리 길이로 채운 뒤 중위 순회의 중앙 루트가 0이면 자손에 1이 없는지 재귀 검사
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:49:04
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level3/020_150367_%ED%91%9C%ED%98%84_%EA%B0%80%EB%8A%A5%ED%95%9C_%EC%9D%B4%EC%A7%84%ED%8A%B8%EB%A6%AC/README.md)
