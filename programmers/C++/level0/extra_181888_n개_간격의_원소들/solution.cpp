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

vector<int> solution(vector<int> num_list, int n) {
    vector<int> answer;
    for (int i = 0; i < (int)num_list.size(); i += n) answer.push_back(num_list[i]);
    return answer;
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
// vector<int> solution(vector<int> num_list, int n) {  // n개 간격의 원소들 풀이 시작
//     vector<int> answer;  // 첫 원소부터 n칸 간격으로 뽑은 값
//     for (int i = 0; i < (int)num_list.size(); i += n) answer.push_back(num_list[i]);  // 인덱스 0, n, 2n, …의 원소 선택
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 첫 원소에서 출발해 n칸씩 건너뛴 위치의 원소를 차례로 모으기
