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

vector<int> solution(vector<int> array, vector<vector<int>> commands) {
    vector<int> answer;
    for (const auto& command : commands) { vector<int> part(array.begin() + command[0] - 1, array.begin() + command[1]); sort(part.begin(), part.end()); answer.push_back(part[command[2] - 1]); }
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
// vector<int> solution(vector<int> array, vector<vector<int>> commands) {  // K번째수 풀이 함수 정의
//     vector<int> answer;  // 명령별 선택 값을 담을 결과 배열 준비
//     for (const auto& command : commands) { vector<int> part(array.begin() + command[0] - 1, array.begin() + command[1]); sort(part.begin(), part.end()); answer.push_back(part[command[2] - 1]); }  // 구간을 잘라 정렬한 뒤 1기준 k를 인덱스 k - 1로 바꿔 해당 원소 추가
//     return answer;  // 각 명령의 k번째 수 배열 반환
// }  // 함수 끝
//

// 풀이 요약
// 명령의 1기준 시작·끝을 반복자 구간으로 바꾸어 복사. 복사한 구간을 정렬해 k번째 원소 선택.
