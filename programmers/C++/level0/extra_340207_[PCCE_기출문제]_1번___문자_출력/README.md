# [PCCE 기출문제] 1번 / 문자 출력

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/340207) · Level 0 · C++

## 풀이

줄바꿈 문자를 넣어 숫자를 각각 한 줄씩 출력한 뒤 저장한 문장을 출력

## 코드와 줄별 설명

빈칸 채우기·한 줄 수정 문제. 사이트에는 정해진 부분만 제출했고, 이 파일은 전체 코드에 메모를 붙인 보관용.

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <iostream>
#include <string>
using namespace std;
int main(void) {
    string message = "Let's go!";
    cout << "3\n2\n1" << endl;
    cout << message << endl;
    return 0;
}

// 전체 코드 줄별 설명
// #include <iostream>  // cin·cout 표준 입출력
// #include <string>  // 문자열을 다룰 string
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
// int main(void) {  // 입력을 읽고 답을 출력할 시작점
//     string message = "Let's go!";  // 큰따옴표 문자열 안에 작은따옴표를 포함한 출력 문장을 저장
//     cout << "3\n2\n1" << endl;  // <<로 숫자를 출력하며 문자열의 \n마다 줄을 바꾸기
//     cout << message << endl;  // 저장한 문장을 출력하고 endl로 줄을 바꾸기
//     return 0;  // 0으로 정상 종료
// }  // 블록 끝

// 풀이 요약
// 줄바꿈 문자를 넣어 숫자를 각각 한 줄씩 출력한 뒤 저장한 문장을 출력
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:47:02
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_340207_%5BPCCE_%EA%B8%B0%EC%B6%9C%EB%AC%B8%EC%A0%9C%5D_1%EB%B2%88___%EB%AC%B8%EC%9E%90_%EC%B6%9C%EB%A0%A5/README.md)
