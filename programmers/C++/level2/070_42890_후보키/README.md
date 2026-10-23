# 후보키

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/42890) · Level 2 · C++

## 풀이

모든 열 부분집합을 검사하고 기존 후보키를 포함하는 선택은 제외한 뒤 행별 값이 모두 다른 선택을 후보키로 등록

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <set>
#include <string>
#include <vector>
using namespace std;

int solution(vector<vector<string>> relation) {
    int columns = (int)relation[0].size();
    vector<int> keys;
    for (int mask = 1; mask < (1 << columns); ++mask) {
        bool minimal = true;
        for (int key : keys) if ((key & mask) == key) minimal = false;
        if (!minimal) continue;
        set<vector<string>> values;
        for (const auto& row : relation) {
            vector<string> tuple;
            for (int c = 0; c < columns; ++c) if (mask & (1 << c)) tuple.push_back(row[c]);
            values.insert(tuple);
        }
        if (values.size() == relation.size()) keys.push_back(mask);
    }
    return (int)keys.size();
}

// 전체 코드 줄별 설명
// #include <set>  // 정렬된 집합과 중복을 허용하는 multiset
// #include <string>  // 문자열을 담는 string
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(vector<vector<string>> relation) {  // 유일성과 최소성을 만족하는 열 집합 찾기
// int columns = (int)relation[0].size();  // 속성 열의 개수 구하기
// vector<int> keys;  // 발견한 후보키의 열 선택을 비트 마스크로 저장
// for (int mask = 1; mask < (1 << columns); ++mask) {  // 비어 있지 않은 모든 열 부분집합 검사
// bool minimal = true;  // 현재 선택이 최소성을 만족한다고 초기화
// for (int key : keys) if ((key & mask) == key) minimal = false;  // 기존 후보키를 포함하면 최소성이 없음
// if (!minimal) continue;  // 최소성을 잃은 선택은 제외
// set<vector<string>> values;  // 선택한 열들의 행별 튜플을 중복 없이 모으기
// for (const auto& row : relation) {  // 각 행에서 선택한 열만 추출
// vector<string> tuple;  // 현재 행의 선택된 속성 저장
// for (int c = 0; c < columns; ++c) if (mask & (1 << c)) tuple.push_back(row[c]);  // 비트가 켜진 열의 값 추가
// values.insert(tuple);  // 행별 튜플을 집합에 넣기
// }  // 블록 끝
// if (values.size() == relation.size()) keys.push_back(mask);  // 모든 행이 구분되면 후보키로 등록
// }  // 블록 끝
// return (int)keys.size();  // 유일성과 최소성을 만족하는 후보키 수 반환
// }  // 블록 끝

// 풀이 요약
// 모든 열 부분집합을 검사하고 기존 후보키를 포함하는 선택은 제외한 뒤 행별 값이 모두 다른 선택을 후보키로 등록
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:19:39
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level2/070_42890_%ED%9B%84%EB%B3%B4%ED%82%A4/README.md)
