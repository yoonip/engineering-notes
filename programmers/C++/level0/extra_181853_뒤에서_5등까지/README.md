# 뒤에서 5등까지

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181853) · Level 0 · C++

## 풀이

오름차순 정렬 후 앞 다섯 개를 선택

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
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

vector<int> solution(vector<int> num_list) {
    sort(num_list.begin(), num_list.end());
    return vector<int>(num_list.begin(), num_list.begin() + 5);
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
// vector<int> solution(vector<int> num_list) {  // 뒤에서 5등까지 풀이 시작
//     sort(num_list.begin(), num_list.end());  // sort로 주어진 구간을 지정한 기준에 따라 오름차순으로 정렬
//     return vector<int>(num_list.begin(), num_list.begin() + 5);  // 두 반복자가 가리키는 반열린 구간을 복사해 새 vector로 반환
// }  // 블록 끝

// 풀이 요약
// 오름차순 정렬 후 앞 다섯 개를 선택
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:18:33
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_181853_%EB%92%A4%EC%97%90%EC%84%9C_5%EB%93%B1%EA%B9%8C%EC%A7%80/README.md)
