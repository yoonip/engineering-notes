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

int solution(vector<string> friends, vector<string> gifts) {
    int n = (int)friends.size();
    unordered_map<string, int> index;
    for (int i = 0; i < n; ++i) index[friends[i]] = i;
    vector<vector<int>> given(n, vector<int>(n, 0));
    vector<int> score(n, 0), received(n, 0);
    for (const string& gift : gifts) {
        istringstream stream(gift); string a, b; stream >> a >> b;
        int giver = index[a], receiver = index[b];
        ++given[giver][receiver]; ++score[giver]; --score[receiver];
    }
    for (int i = 0; i < n; ++i) for (int j = i + 1; j < n; ++j) {
        if (given[i][j] > given[j][i] || (given[i][j] == given[j][i] && score[i] > score[j])) ++received[i];
        else if (given[i][j] < given[j][i] || (given[i][j] == given[j][i] && score[i] < score[j])) ++received[j];
    }
    return *max_element(received.begin(), received.end());
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
// int solution(vector<string> friends, vector<string> gifts) {  // 가장 많이 받은 선물 풀이 함수 정의
//     int n = (int)friends.size();  // 친구 수 n 저장
//     unordered_map<string, int> index;  // 친구 이름을 배열 인덱스로 바꿀 해시 맵 준비
//     for (int i = 0; i < n; ++i) index[friends[i]] = i;  // 친구 이름마다 0기준 인덱스 연결
//     vector<vector<int>> given(n, vector<int>(n, 0));  // given[a][b]에 a가 b에게 준 선물 수 저장
//     vector<int> score(n, 0), received(n, 0);  // 선물 지수 score와 다음 달 받을 수 received를 각각 0으로 초기화
//     for (const string& gift : gifts) {  // 이번 달 선물 기록을 하나씩 읽음
//         istringstream stream(gift); string a, b; stream >> a >> b;  // 기록을 공백으로 나눠 준 사람 a와 받은 사람 b를 읽음
//         int giver = index[a], receiver = index[b];  // 이름을 준 사람 giver와 받은 사람 receiver의 인덱스로 변환
//         ++given[giver][receiver]; ++score[giver]; --score[receiver];  // 방향별 선물 수를 늘리고 준 사람 지수 +1, 받은 사람 지수 -1
//     }  // 블록 끝
//     for (int i = 0; i < n; ++i) for (int j = i + 1; j < n; ++j) {  // 같은 두 사람을 중복 비교하지 않도록 i < j인 쌍만 검사
//         if (given[i][j] > given[j][i] || (given[i][j] == given[j][i] && score[i] > score[j])) ++received[i];  // i가 더 많이 주었거나, 주고받은 수가 같고 선물 지수가 높으면 i가 다음 달에 받음
//         else if (given[i][j] < given[j][i] || (given[i][j] == given[j][i] && score[i] < score[j])) ++received[j];  // 반대 조건이면 j가 다음 달에 받음. 둘 다 같으면 아무도 받지 않음
//     }  // 블록 끝
//     return *max_element(received.begin(), received.end());  // 친구별 다음 달 선물 수의 최댓값 반환
// }  // 함수 끝
//

// 풀이 요약
// 서로 주고받은 선물 수와 선물 지수를 기록. 두 사람씩 비교해 다음 달 받을 사람을 정하고 받은 개수의 최댓값 반환.
