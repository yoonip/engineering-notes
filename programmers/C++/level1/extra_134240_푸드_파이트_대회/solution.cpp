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

string solution(vector<int> food) {
    string left;
    for (int i = 1; i < (int)food.size(); ++i) left.append(food[i] / 2, char('0' + i));
    string right = left; reverse(right.begin(), right.end());
    return left + "0" + right;
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
// string solution(vector<int> food) {  // 푸드 파이트 대회 풀이 함수 정의
//     string left;  // 한 선수가 먹을 음식 순서 left 준비
//     for (int i = 1; i < (int)food.size(); ++i) left.append(food[i] / 2, char('0' + i));  // 물인 0번은 빼고 음식 번호별 절반 개수만큼 왼쪽 문자열에 추가
//     string right = left; reverse(right.begin(), right.end());  // 왼쪽 문자열을 복사한 뒤 역순으로 바꿔 오른쪽 배치 생성
//     return left + "0" + right;  // 왼쪽 음식 + 가운데 물 0 + 오른쪽 음식 반환
// }  // 함수 끝
//

// 풀이 요약
// 각 음식 개수의 절반으로 왼쪽 배치를 만듦. 왼쪽을 뒤집은 배치를 오른쪽에 놓고 가운데 물 0 추가.
