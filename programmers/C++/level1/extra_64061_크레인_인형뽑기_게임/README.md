# 크레인 인형뽑기 게임

[레벨 1 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/64061) · Level 1 · C++

## 풀이

선택한 열에서 위쪽의 첫 인형을 꺼냄. 바구니 맨 위와 같으면 둘을 없애고 아니면 바구니에 추가.

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

int solution(vector<vector<int>> board, vector<int> moves) {
    vector<int> basket; int answer = 0;
    for (int move : moves) {
        int col = move - 1;
        for (int row = 0; row < (int)board.size(); ++row) if (board[row][col]) {
            int doll = board[row][col]; board[row][col] = 0;
            if (!basket.empty() && basket.back() == doll) { basket.pop_back(); answer += 2; }
            else basket.push_back(doll);
            break;
        }
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
// int solution(vector<vector<int>> board, vector<int> moves) {  // 크레인 인형뽑기 게임 풀이 함수 정의
//     vector<int> basket; int answer = 0;  // 바구니 스택과 사라진 인형 수 answer 준비
//     for (int move : moves) {  // 크레인 이동 명령을 차례로 처리
//         int col = move - 1;  // 1기준 열 번호를 0기준 인덱스로 변환
//         for (int row = 0; row < (int)board.size(); ++row) if (board[row][col]) {  // 선택한 열을 위에서 아래로 찾아 첫 인형이 있는 칸 처리
//             int doll = board[row][col]; board[row][col] = 0;  // 인형 값을 저장하고 보드의 해당 칸을 빈칸으로 변경
//             if (!basket.empty() && basket.back() == doll) { basket.pop_back(); answer += 2; }  // 바구니 꼭대기와 같으면 기존 인형을 꺼내고 사라진 수에 2 추가
//             else basket.push_back(doll);  // 다른 인형이면 바구니 맨 위에 쌓음
//             break;  // 한 번에 한 인형만 꺼내므로 이 열 탐색 종료
//         }  // 블록 끝
//     }  // 블록 끝
//     return answer;  // 전체 이동에서 사라진 인형 수 반환
// }  // 함수 끝
//

// 풀이 요약
// 선택한 열에서 위쪽의 첫 인형을 꺼냄. 바구니 맨 위와 같으면 둘을 없애고 아니면 바구니에 추가.
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:15:57
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level1/extra_64061_%ED%81%AC%EB%A0%88%EC%9D%B8_%EC%9D%B8%ED%98%95%EB%BD%91%EA%B8%B0_%EA%B2%8C%EC%9E%84/README.md)
