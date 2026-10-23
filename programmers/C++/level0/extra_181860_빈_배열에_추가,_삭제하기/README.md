# 빈 배열에 추가, 삭제하기

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181860) · Level 0 · C++

## 풀이

flag가 참이면 지정 개수를 추가하고 거짓이면 끝에서 지정 개수를 삭제

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

vector<int> solution(vector<int> arr, vector<bool> flag) {
    vector<int> answer;
    for (int i = 0; i < (int)arr.size(); ++i) {
        if (flag[i]) answer.insert(answer.end(), arr[i] * 2, arr[i]);
        else answer.resize(answer.size() - arr[i]);
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
// vector<int> solution(vector<int> arr, vector<bool> flag) {  // 빈 배열에 추가, 삭제하기 풀이 시작
//     vector<int> answer;  // flag에 따라 끝에서 추가·삭제할 배열
//     for (int i = 0; i < (int)arr.size(); ++i) {  // arr의 값과 같은 위치의 flag를 함께 처리
//         if (flag[i]) answer.insert(answer.end(), arr[i] * 2, arr[i]);  // if로 추가 여부를 확인하고 insert로 지정한 값을 여러 번 붙이기
//         else answer.resize(answer.size() - arr[i]);  // flag가 거짓이면 끝에서 arr[i]개 삭제
//     }  // 블록 끝
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// flag가 참이면 지정 개수를 추가하고 거짓이면 끝에서 지정 개수를 삭제
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:15:21
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181860_%EB%B9%88_%EB%B0%B0%EC%97%B4%EC%97%90_%EC%B6%94%EA%B0%80%2C_%EC%82%AD%EC%A0%9C%ED%95%98%EA%B8%B0/README.md)
