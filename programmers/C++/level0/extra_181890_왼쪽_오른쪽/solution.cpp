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

vector<string> solution(vector<string> str_list) {
    for (int i = 0; i < (int)str_list.size(); ++i) {
        if (str_list[i] == "l") return vector<string>(str_list.begin(), str_list.begin() + i);
        if (str_list[i] == "r") return vector<string>(str_list.begin() + i + 1, str_list.end());
    }
    return {};
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
// vector<string> solution(vector<string> str_list) {  // 왼쪽 오른쪽 풀이 시작
//     for (int i = 0; i < (int)str_list.size(); ++i) {  // 처음 나오는 l 또는 r을 찾을 때까지 왼쪽부터 확인
//         if (str_list[i] == "l") return vector<string>(str_list.begin(), str_list.begin() + i);  // 첫 l의 왼쪽 원소만 반환
//         if (str_list[i] == "r") return vector<string>(str_list.begin() + i + 1, str_list.end());  // 첫 r의 오른쪽 원소만 반환
//     }  // 블록 끝
//     return {};  // 빈 vector를 반환
// }  // 블록 끝

// 풀이 요약
// 앞에서부터 보다가 l 또는 r을 처음 만나는 즉시 해당 부분을 반환
