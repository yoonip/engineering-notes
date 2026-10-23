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

int solution(vector<int> mats, vector<vector<string>> park) {
    int rows = (int)park.size(), cols = (int)park[0].size();
    vector<vector<int>> blocked(rows + 1, vector<int>(cols + 1));
    for (int r = 0; r < rows; ++r)
        for (int c = 0; c < cols; ++c) blocked[r + 1][c + 1] = blocked[r][c + 1] + blocked[r + 1][c] - blocked[r][c] + (park[r][c] != "-1");
    sort(mats.rbegin(), mats.rend());
    for (int size : mats)
        for (int r = 0; r + size <= rows; ++r)
            for (int c = 0; c + size <= cols; ++c)
                if (blocked[r + size][c + size] - blocked[r][c + size] - blocked[r + size][c] + blocked[r][c] == 0) return size;
    return -1;
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
// int solution(vector<int> mats, vector<vector<string>> park) {  // [PCCE 기출문제] 10번 / 공원 풀이 함수 정의
//     int rows = (int)park.size(), cols = (int)park[0].size();  // 공원의 행 수 rows와 열 수 cols 저장
//     vector<vector<int>> blocked(rows + 1, vector<int>(cols + 1));  // 사용 중인 칸 수를 구할 2차원 누적합 blocked 준비
//     for (int r = 0; r < rows; ++r)  // 공원의 각 행 순회
//         for (int c = 0; c < cols; ++c) blocked[r + 1][c + 1] = blocked[r][c + 1] + blocked[r + 1][c] - blocked[r][c] + (park[r][c] != "-1");  // 각 칸이 사용 중인지 더하고 위·왼쪽 누적합을 합친 뒤 겹친 부분을 빼서 누적합 계산
//     sort(mats.rbegin(), mats.rend());  // 큰 돗자리부터 찾도록 내림차순 정렬
//     for (int size : mats)  // 돗자리 한 변 size를 큰 순서대로 선택
//         for (int r = 0; r + size <= rows; ++r)  // 돗자리가 행 범위를 넘지 않는 시작 행 검사
//             for (int c = 0; c + size <= cols; ++c)  // 돗자리가 열 범위를 넘지 않는 시작 열 검사
//                 if (blocked[r + size][c + size] - blocked[r][c + size] - blocked[r + size][c] + blocked[r][c] == 0) return size;  // 네 누적합으로 구한 영역의 사용 중인 칸 수가 0이면 현재 size가 최대이므로 반환
//     return -1;  // 어떤 돗자리도 놓을 수 없으면 -1 반환
// }  // 함수 끝
//

// 풀이 요약
// 사용 중인 칸의 2차원 누적합을 만든 뒤 큰 돗자리부터 검사. 해당 정사각형의 사용 중인 칸 수가 0이면 바로 선택.
