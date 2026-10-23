#include <string>
#include <vector>
#include <algorithm>
#include <numeric>
#include <functional>
#include <unordered_set>
#include <sstream>
#include <cctype>
#include <cstdlib>
using namespace std;

int solution(vector<int> num_list) {
    for (int i = 0; i < (int)num_list.size(); ++i) if (num_list[i] < 0) return i;
    return -1;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 다룰 string
// #include <vector>  // 길이를 늘릴 수 있는 vector
// #include <algorithm>  // 정렬·검색·뒤집기 알고리즘
// #include <numeric>  // accumulate·iota 등 수치 연산
// #include <functional>  // greater·multiplies 등 함수 객체
// #include <unordered_set>  // 중복을 거를 해시 집합
// #include <sstream>  // 문자열을 항목별로 읽을 스트림
// #include <cctype>  // 문자 검사와 대소문자 변환
// #include <cstdlib>  // 정수 변환과 절댓값 등 표준 함수
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// int solution(vector<int> num_list) {  // 첫 번째로 나오는 음수 풀이 시작
//     for (int i = 0; i < (int)num_list.size(); ++i) if (num_list[i] < 0) return i;  // 왼쪽부터 검사해 처음 나온 음수의 인덱스 반환
//     return -1;  // 조건을 만족하는 위치가 없으므로 -1을 반환
// }  // 블록 끝

// 풀이 요약
// 앞에서부터 검사하면 처음 찾은 음수가 가장 먼저 등장한 음수임
