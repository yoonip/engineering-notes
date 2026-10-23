# 키패드 누르기

[레벨 1 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/67256) · Level 1 · C++

## 풀이

양 끝 열은 정해진 손 사용. 가운데 열은 두 엄지의 맨해튼 거리를 비교하고 동점이면 주로 쓰는 손 선택.

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <string>
#include <vector>
#include <algorithm>
#include <numeric>
#include <functional>
#include <unordered_set>
#include <unordered_map>
#include <sstream>
#include <cctype>
#include <cstdlib>
#include <cstdio>
#include <cmath>
#include <queue>
#include <set>
#include <climits>
#include <iostream>
using namespace std;

string solution(vector<int> numbers, string hand) {
    int left = 10, right = 12;
    string answer;
    for (int number : numbers) {
        int key = number == 0 ? 11 : number;
        char used;
        if (key % 3 == 1) used = 'L';
        else if (key % 3 == 0) used = 'R';
        else {
            int dl = abs((left - 1) / 3 - (key - 1) / 3) + abs((left - 1) % 3 - (key - 1) % 3);
            int dr = abs((right - 1) / 3 - (key - 1) / 3) + abs((right - 1) % 3 - (key - 1) % 3);
            used = dl < dr || (dl == dr && hand == "left") ? 'L' : 'R';
        }
        if (used == 'L') left = key; else right = key;
        answer += used;
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열 string 사용 준비
// #include <vector>  // 가변 길이 배열 vector 사용 준비
// #include <algorithm>  // 정렬·탐색·최솟값 등 표준 알고리즘 사용 준비
// #include <numeric>  // gcd·accumulate 등 수치 알고리즘 사용 준비
// #include <functional>  // 함수 래퍼와 greater 등 비교 함수 객체 사용 준비
// #include <unordered_set>  // 중복 없는 원소를 저장하는 해시 집합 사용 준비
// #include <unordered_map>  // 키로 값을 찾는 해시 맵 사용 준비
// #include <sstream>  // 문자열을 토큰으로 나눠 읽을 스트림 사용 준비
// #include <cctype>  // 숫자·대소문자 검사와 변환 함수 사용 준비
// #include <cstdlib>  // 정수 절댓값 등 표준 유틸리티 함수 사용 준비
// #include <cstdio>  // snprintf 등 형식 있는 입출력 함수 사용 준비
// #include <cmath>  // 제곱근 등 수학 함수 사용 준비
// #include <queue>  // FIFO 큐와 우선순위 큐 사용 준비
// #include <set>  // 중복 제거와 정렬을 함께 하는 집합 사용 준비
// #include <climits>  // 정수 범위 상수 사용 준비
// #include <iostream>  // cin·cout 표준 입출력 사용 준비
// using namespace std;  // 표준 이름의 std:: 접두사 생략
//
// string solution(vector<int> numbers, string hand) {  // 키패드 누르기 풀이 함수 정의
//     int left = 10, right = 12;  // 왼손은 * 위치 10, 오른손은 # 위치 12에서 시작
//     string answer;  // 사용한 손 L·R을 기록할 결과 문자열 준비
//     for (int number : numbers) {  // 누를 숫자를 순서대로 처리
//         int key = number == 0 ? 11 : number;  // 0을 키패드의 11번 위치로 바꿔 행·열 계산 방식 통일
//         char used;  // 이번 숫자에 사용할 손 used 준비
//         if (key % 3 == 1) used = 'L';  // 왼쪽 열이면 왼손 선택
//         else if (key % 3 == 0) used = 'R';  // 오른쪽 열이면 오른손 선택
//         else {  // 가운데 열은 두 손의 이동 거리 비교
//             int dl = abs((left - 1) / 3 - (key - 1) / 3) + abs((left - 1) % 3 - (key - 1) % 3);  // 왼손과 목표 키의 행 차이 + 열 차이 계산
//             int dr = abs((right - 1) / 3 - (key - 1) / 3) + abs((right - 1) % 3 - (key - 1) % 3);  // 오른손과 목표 키의 행 차이 + 열 차이 계산
//             used = dl < dr || (dl == dr && hand == "left") ? 'L' : 'R';  // 왼손이 가깝거나 동점에서 왼손잡이면 L, 나머지는 R 선택
//         }  // 블록 끝
//         if (used == 'L') left = key; else right = key;  // 선택한 손의 위치를 목표 키로 갱신
//         answer += used;  // 선택한 손 문자를 결과에 추가
//     }  // 블록 끝
//     return answer;  // 전체 숫자를 누른 손의 순서 반환
// }  // 함수 끝
//

// 풀이 요약
// 양 끝 열은 정해진 손 사용. 가운데 열은 두 엄지의 맨해튼 거리를 비교하고 동점이면 주로 쓰는 손 선택.
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:15:41
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level1/extra_67256_%ED%82%A4%ED%8C%A8%EB%93%9C_%EB%88%84%EB%A5%B4%EA%B8%B0/README.md)
