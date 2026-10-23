# 신고 결과 받기

[레벨 1 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/92334) · Level 1 · C++

## 풀이

신고자별 신고 대상은 집합으로 저장해 중복 신고 제거. 대상의 총 신고 수가 k 이상이면 신고자에게 알림 하나 추가.

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

vector<int> solution(vector<string> id_list, vector<string> report, int k) {
    int n = (int)id_list.size();
    unordered_map<string, int> index;
    for (int i = 0; i < n; ++i) index[id_list[i]] = i;
    vector<unordered_set<int>> targets(n);
    vector<int> reported(n, 0), answer(n, 0);
    for (const string& record : report) {
        istringstream stream(record); string reporter, target; stream >> reporter >> target;
        int a = index[reporter], b = index[target];
        if (targets[a].insert(b).second) ++reported[b];
    }
    for (int i = 0; i < n; ++i) for (int target : targets[i]) if (reported[target] >= k) ++answer[i];
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
// vector<int> solution(vector<string> id_list, vector<string> report, int k) {  // 신고 결과 받기 풀이 함수 정의
//     int n = (int)id_list.size();  // 사용자 수 n 저장
//     unordered_map<string, int> index;  // 사용자 이름을 배열 인덱스로 바꿀 맵 준비
//     for (int i = 0; i < n; ++i) index[id_list[i]] = i;  // id_list 순서대로 이름과 인덱스 연결
//     vector<unordered_set<int>> targets(n);  // 각 신고자가 신고한 대상을 집합으로 저장
//     vector<int> reported(n, 0), answer(n, 0);  // 대상별 신고받은 수 reported와 신고자별 메일 수 answer를 0으로 초기화
//     for (const string& record : report) {  // 각 신고 문자열을 처리
//         istringstream stream(record); string reporter, target; stream >> reporter >> target;  // 공백 기준으로 신고자와 신고 대상 이름 분리
//         int a = index[reporter], b = index[target];  // 두 이름을 배열 인덱스 a·b로 변환
//         if (targets[a].insert(b).second) ++reported[b];  // 집합에 처음 추가된 신고일 때만 대상의 신고받은 횟수 증가
//     }  // 블록 끝
//     for (int i = 0; i < n; ++i) for (int target : targets[i]) if (reported[target] >= k) ++answer[i];  // 각 사용자가 신고한 대상 중 k회 이상 신고된 대상마다 메일 수 증가
//     return answer;  // id_list 순서의 메일 수 배열 반환
// }  // 함수 끝
//

// 풀이 요약
// 신고자별 신고 대상은 집합으로 저장해 중복 신고 제거. 대상의 총 신고 수가 k 이상이면 신고자에게 알림 하나 추가.
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:12:32
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level1/extra_92334_%EC%8B%A0%EA%B3%A0_%EA%B2%B0%EA%B3%BC_%EB%B0%9B%EA%B8%B0/README.md)
