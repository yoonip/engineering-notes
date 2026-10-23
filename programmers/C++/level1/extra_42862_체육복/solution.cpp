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

int solution(int n, vector<int> lost, vector<int> reserve) {
    vector<int> clothes(n + 2, 1);
    for (int student : lost) --clothes[student]; for (int student : reserve) ++clothes[student];
    for (int i = 1; i <= n; ++i) if (clothes[i] == 2) {
        if (i > 1 && clothes[i - 1] == 0) { --clothes[i]; ++clothes[i - 1]; }
        else if (i < n && clothes[i + 1] == 0) { --clothes[i]; ++clothes[i + 1]; }
    }
    int answer = 0;
    for (int i = 1; i <= n; ++i) if (clothes[i] > 0) ++answer;
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
// int solution(int n, vector<int> lost, vector<int> reserve) {  // 체육복 풀이 함수 정의
//     vector<int> clothes(n + 2, 1);  // 학생마다 체육복 한 벌로 시작하고 양 끝 비교용 여유 칸 확보
//     for (int student : lost) --clothes[student]; for (int student : reserve) ++clothes[student];  // 분실 학생은 한 벌 빼고 여벌 학생은 한 벌 추가
//     for (int i = 1; i <= n; ++i) if (clothes[i] == 2) {  // 왼쪽 학생부터 남는 옷이 두 벌인 학생 처리
//         if (i > 1 && clothes[i - 1] == 0) { --clothes[i]; ++clothes[i - 1]; }  // 왼쪽 이웃에게 옷이 없으면 우선 한 벌 전달
//         else if (i < n && clothes[i + 1] == 0) { --clothes[i]; ++clothes[i + 1]; }  // 왼쪽에 줄 필요가 없을 때 오른쪽 이웃에게 옷이 없으면 한 벌 전달
//     }  // 블록 끝
//     int answer = 0;  // 체육 수업에 참여할 학생 수 answer를 0으로 시작
//     for (int i = 1; i <= n; ++i) if (clothes[i] > 0) ++answer;  // 실제 학생 번호에서 옷이 한 벌 이상인 학생 수 집계
//     return answer;  // 체육복을 입을 수 있는 학생 수 반환
// }  // 함수 끝
//

// 풀이 요약
// 분실·여벌을 옷 수에 함께 반영해 자기 여벌을 먼저 상쇄. 남은 여벌은 왼쪽부터 빌려주고 입을 수 있는 학생 수를 셈.
