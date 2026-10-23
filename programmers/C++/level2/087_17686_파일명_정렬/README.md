# [3차] 파일명 정렬

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/17686) · Level 2 · C++

## 풀이

파일명을 대소문자 구분 없는 HEAD와 최대 다섯 자리 NUMBER로 비교하며 동률에서는 입력 순서 유지

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <algorithm>
#include <cctype>
#include <string>
#include <vector>
using namespace std;

vector<string> solution(vector<string> files) {
    auto key = [](const string& filename) {
        size_t start = 0;
        while (start < filename.size() && !isdigit((unsigned char)filename[start])) ++start;
        size_t end = start;
        while (end < filename.size() && end < start + 5 && isdigit((unsigned char)filename[end])) ++end;
        string head = filename.substr(0, start);
        for (char& c : head) c = (char)tolower((unsigned char)c);
        return make_pair(head, stoi(filename.substr(start, end - start)));
    };
    stable_sort(files.begin(), files.end(), [&](const string& a, const string& b) { return key(a) < key(b); });
    return files;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <cctype>  // 문자 분류와 대소문자 변환
// #include <string>  // 문자열을 담는 string
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// vector<string> solution(vector<string> files) {  // HEAD·NUMBER 순으로 안정 정렬
// auto key = [](const string& filename) {  // 파일명에서 정렬에 쓰는 두 부분 구하기
// size_t start = 0;  // 숫자가 시작하는 위치 찾기
// while (start < filename.size() && !isdigit((unsigned char)filename[start])) ++start;  // 숫자 이전의 HEAD 부분을 건너뛰기
// size_t end = start;  // NUMBER 부분의 끝 찾기
// while (end < filename.size() && end < start + 5 && isdigit((unsigned char)filename[end])) ++end;  // 숫자를 최대 다섯 자리까지 읽기
// string head = filename.substr(0, start);  // HEAD 문자열을 추출
// for (char& c : head) c = (char)tolower((unsigned char)c);  // 대소문자를 구분하지 않도록 소문자로 바꾸기
// return make_pair(head, stoi(filename.substr(start, end - start)));  // HEAD와 NUMBER를 비교용 쌍으로 반환
// };  // 블록 끝
// stable_sort(files.begin(), files.end(), [&](const string& a, const string& b) { return key(a) < key(b); });  // 두 정렬 키가 같으면 원래 입력 순서 유지
// return files;  // 정렬한 파일명 목록 반환
// }  // 블록 끝

// 풀이 요약
// 파일명을 대소문자 구분 없는 HEAD와 최대 다섯 자리 NUMBER로 비교하며 동률에서는 입력 순서 유지
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:27:26
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level2/087_17686_%ED%8C%8C%EC%9D%BC%EB%AA%85_%EC%A0%95%EB%A0%AC/README.md)
