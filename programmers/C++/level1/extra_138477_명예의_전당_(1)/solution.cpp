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

vector<int> solution(int k, vector<int> score) {
    priority_queue<int, vector<int>, greater<int>> hall;
    vector<int> answer;
    for (int point : score) { hall.push(point); if ((int)hall.size() > k) hall.pop(); answer.push_back(hall.top()); }
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
// vector<int> solution(int k, vector<int> score) {  // 명예의 전당 (1) 풀이 함수 정의
//     priority_queue<int, vector<int>, greater<int>> hall;  // greater 비교자를 둔 최소 힙 hall에 명예의 전당 점수 저장
//     vector<int> answer;  // 날짜별 발표 점수를 담을 결과 배열 준비
//     for (int point : score) { hall.push(point); if ((int)hall.size() > k) hall.pop(); answer.push_back(hall.top()); }  // 점수를 추가하고 k개 초과 시 최솟값 제거. 남은 상위 점수 중 최솟값을 결과에 추가
//     return answer;  // 매일 발표한 점수 배열 반환
// }  // 함수 끝
//

// 풀이 요약
// 최소 힙에 상위 k개 점수만 유지. 매일 새 점수를 넣고 k개를 넘으면 최솟값을 빼며, 힙 꼭대기를 그날의 발표 점수로 기록.
