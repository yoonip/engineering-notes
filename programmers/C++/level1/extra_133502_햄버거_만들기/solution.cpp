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

int solution(vector<int> ingredient) {
    vector<int> stack;
    int answer = 0;
    for (int item : ingredient) {
        stack.push_back(item); size_t n = stack.size();
        if (n >= 4 && stack[n - 4] == 1 && stack[n - 3] == 2 && stack[n - 2] == 3 && stack[n - 1] == 1) { stack.resize(n - 4); ++answer; }
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
// int solution(vector<int> ingredient) {  // 햄버거 만들기 풀이 함수 정의
//     vector<int> stack;  // 아직 햄버거로 사용하지 않은 재료를 저장할 스택 준비
//     int answer = 0;  // 완성한 햄버거 수 answer를 0으로 시작
//     for (int item : ingredient) {  // 들어오는 재료를 순서대로 처리
//         stack.push_back(item); size_t n = stack.size();  // 현재 재료를 스택 끝에 넣고 스택 길이 n 확인
//         if (n >= 4 && stack[n - 4] == 1 && stack[n - 3] == 2 && stack[n - 2] == 3 && stack[n - 1] == 1) { stack.resize(n - 4); ++answer; }  // 끝 네 재료가 빵·야채·고기·빵이면 네 개를 제거하고 햄버거 수 증가
//     }  // 블록 끝
//     return answer;  // 완성해 꺼낸 햄버거 수 반환
// }  // 함수 끝
//

// 풀이 요약
// 재료를 스택에 넣고 끝 네 개가 1,2,3,1이면 바로 제거. 제거 뒤 이어지는 재료도 같은 방식으로 검사.
