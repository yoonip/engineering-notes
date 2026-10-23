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

vector<int> solution(vector<int> arr, vector<int> query) {
    int begin = 0, end = (int)arr.size();
    for (int i = 0; i < (int)query.size(); ++i) {
        if (i % 2 == 0) end = begin + query[i] + 1;
        else begin += query[i];
    }
    return vector<int>(arr.begin() + begin, arr.begin() + end);
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
// vector<int> solution(vector<int> arr, vector<int> query) {  // 배열 조각하기 풀이 시작
//     int begin = 0, end = (int)arr.size();  // 남아 있는 구간의 시작과 끝 다음 위치
//     for (int i = 0; i < (int)query.size(); ++i) {  // 잘라낸 뒤의 구간을 기준으로 쿼리 차례대로 적용
//         if (i % 2 == 0) end = begin + query[i] + 1;  // i % 2 == 0이면 end에 begin + query[i] + 1 저장
//         else begin += query[i];  // 홀수 번째 쿼리는 남은 구간의 앞부분을 버리기
//     }  // 블록 끝
//     return vector<int>(arr.begin() + begin, arr.begin() + end);  // 두 반복자가 가리키는 반열린 구간을 복사해 새 vector로 반환
// }  // 블록 끝

// 풀이 요약
// 각 쿼리는 이전 작업 후 남은 리스트의 인덱스를 기준으로 적용
