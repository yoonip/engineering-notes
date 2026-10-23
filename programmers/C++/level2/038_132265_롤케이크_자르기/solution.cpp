#include <unordered_map>
#include <unordered_set>
#include <vector>
using namespace std;

int solution(vector<int> topping) {
    unordered_map<int, int> right;
    for (int value : topping) ++right[value];
    unordered_set<int> left;
    int answer = 0;
    for (int value : topping) {
        left.insert(value);
        if (--right[value] == 0) right.erase(value);
        if (left.size() == right.size()) ++answer;
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <unordered_map>  // 키로 값을 찾는 해시 맵
// #include <unordered_set>  // 중복을 걸러 낼 해시 집합
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(vector<int> topping) {  // 자르는 위치 양쪽의 토핑 종류 수 비교
// unordered_map<int, int> right;  // 오른쪽 조각의 토핑별 개수 저장
// for (int value : topping) ++right[value];  // 처음에는 모든 토핑을 오른쪽에 두기
// unordered_set<int> left;  // 왼쪽 조각에 등장한 토핑 종류 저장
// int answer = 0;  // 두 조각의 종류 수가 같은 위치 세기
// for (int value : topping) {  // 자르는 위치를 오른쪽으로 한 칸씩 옮기기
// left.insert(value);  // 현재 토핑 종류를 왼쪽에 추가
// if (--right[value] == 0) right.erase(value);  // 오른쪽에서 마지막 토핑을 옮겼으면 종류 자체 제거
// if (left.size() == right.size()) ++answer;  // 양쪽 종류 수가 같으면 분할 위치 세기
// }  // 블록 끝
// return answer;  // 공평하게 나누는 위치 수 반환
// }  // 블록 끝

// 풀이 요약
// 자르는 위치를 한 칸씩 이동하며 왼쪽의 종류 집합과 오른쪽의 남은 빈도를 갱신해 종류 수 비교
