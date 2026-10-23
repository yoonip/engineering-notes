#include <string>
#include <vector>
using namespace std;

int solution(string skill, vector<string> skill_trees) {
    int answer = 0;
    for (const string& tree : skill_trees) {
        string filtered;
        for (char c : tree) if (skill.find(c) != string::npos) filtered += c;
        if (skill.compare(0, filtered.size(), filtered) == 0) ++answer;
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 담는 string
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(string skill, vector<string> skill_trees) {  // 선행 스킬만 남긴 순서가 올바른 접두사인지 확인
// int answer = 0;  // 가능한 스킬트리 수 초기화
// for (const string& tree : skill_trees) {  // 스킬트리를 하나씩 검사
// string filtered;  // 선행 조건에 등장하는 스킬만 모으기
// for (char c : tree) if (skill.find(c) != string::npos) filtered += c;  // 관련 없는 스킬은 제외
// if (skill.compare(0, filtered.size(), filtered) == 0) ++answer;  // 남은 순서가 선행 스킬의 접두사인지 검사
// }  // 블록 끝
// return answer;  // 선행 조건을 지킨 스킬트리 수 반환
// }  // 블록 끝

// 풀이 요약
// 선행 조건에 속한 스킬만 남긴 순서가 전체 선행 스킬 문자열의 접두사인지 확인
