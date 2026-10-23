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

string solution(vector<string> cards1, vector<string> cards2, vector<string> goal) {
    size_t i = 0, j = 0;
    for (const string& word : goal) {
        if (i < cards1.size() && cards1[i] == word) ++i;
        else if (j < cards2.size() && cards2[j] == word) ++j;
        else return "No";
    }
    return "Yes";
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
// string solution(vector<string> cards1, vector<string> cards2, vector<string> goal) {  // 카드 뭉치 풀이 함수 정의
//     size_t i = 0, j = 0;  // 각 뭉치에서 아직 쓰지 않은 다음 카드 위치 i·j를 0으로 시작
//     for (const string& word : goal) {  // 목표 단어를 필요한 순서대로 검사
//         if (i < cards1.size() && cards1[i] == word) ++i;  // 첫 뭉치의 다음 카드가 맞으면 그 카드 사용
//         else if (j < cards2.size() && cards2[j] == word) ++j;  // 아니면 두 번째 뭉치의 다음 카드가 맞는지 확인해 사용
//         else return "No";  // 두 뭉치 모두에서 다음 카드를 꺼낼 수 없으면 No 반환
//     }  // 블록 끝
//     return "Yes";  // 목표 단어를 모두 순서대로 꺼냈으면 Yes 반환
// }  // 함수 끝
//

// 풀이 요약
// 두 카드 뭉치에서 다음으로 쓸 위치만 관리. 목표 단어가 어느 뭉치의 다음 카드와도 맞지 않으면 실패.
