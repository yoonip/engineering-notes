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

vector<int> solution(vector<string> name, vector<int> yearning, vector<vector<string>> photo) {
    unordered_map<string, int> scores;
    for (int i = 0; i < (int)name.size(); ++i) scores[name[i]] = yearning[i];
    vector<int> answer;
    for (const auto& people : photo) {
        int total = 0;
        for (const string& person : people) total += scores[person];
        answer.push_back(total);
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
// vector<int> solution(vector<string> name, vector<int> yearning, vector<vector<string>> photo) {  // 추억 점수 풀이 함수 정의
//     unordered_map<string, int> scores;  // 이름별 추억 점수를 찾을 해시 맵 준비
//     for (int i = 0; i < (int)name.size(); ++i) scores[name[i]] = yearning[i];  // name과 yearning의 같은 인덱스를 연결해 점수 저장
//     vector<int> answer;  // 사진별 점수를 저장할 결과 배열 준비
//     for (const auto& people : photo) {  // 사진에 등장하는 사람 목록을 하나씩 처리
//         int total = 0;  // 현재 사진의 점수 합 total을 0으로 시작
//         for (const string& person : people) total += scores[person];  // 사진 속 각 사람의 점수를 합산. 없는 이름은 맵의 기본값 0 사용
//         answer.push_back(total);  // 현재 사진의 점수 합을 결과 끝에 추가
//     }  // 블록 끝
//     return answer;  // 사진 순서대로 계산한 점수 배열 반환
// }  // 함수 끝
//

// 풀이 요약
// 이름별 추억 점수를 해시 맵에 저장하고 사진마다 등장한 사람들의 점수를 합산.
