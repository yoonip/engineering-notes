#include <string>
#include <unordered_set>
#include <vector>
using namespace std;

int solution(vector<string> user_id, vector<string> banned_id) {
    unordered_set<int> states{0};
    for (const string& pattern : banned_id) {
        vector<int> candidates;
        for (int i = 0; i < (int)user_id.size(); ++i) {
            if (user_id[i].size() != pattern.size()) continue;
            bool matches = true; for (int j = 0; j < (int)pattern.size(); ++j) if (pattern[j] != '*' && pattern[j] != user_id[i][j]) matches = false;
            if (matches) candidates.push_back(1 << i);
        }
        unordered_set<int> next;
        for (int mask : states) for (int bit : candidates) if (!(mask & bit)) next.insert(mask | bit);
        states = move(next);
    }
    return (int)states.size();
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 담는 string
// #include <unordered_set>  // 중복을 걸러 낼 해시 집합
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(vector<string> user_id, vector<string> banned_id) {  // 사용자 배정을 비트 집합으로 모아 중복 제거
// unordered_set<int> states{0};  // 아직 제재 사용자를 고르지 않은 상태에서 시작
// for (const string& pattern : banned_id) {  // 불량 사용자 패턴을 하나씩 배정하기
// vector<int> candidates;  // 현재 패턴과 일치하는 사용자 비트 저장
// for (int i = 0; i < (int)user_id.size(); ++i) {  // 모든 사용자 아이디 확인
// if (user_id[i].size() != pattern.size()) continue;  // 길이가 다르면 일치할 수 없음
// bool matches = true; for (int j = 0; j < (int)pattern.size(); ++j) if (pattern[j] != '*' && pattern[j] != user_id[i][j]) matches = false;  // 별표를 제외한 각 문자가 같은지 검사
// if (matches) candidates.push_back(1 << i);  // 일치 사용자의 비트 등록
// }  // 블록 끝
// unordered_set<int> next;  // 현재 패턴까지 배정한 중복 없는 사용자 집합
// for (int mask : states) for (int bit : candidates) if (!(mask & bit)) next.insert(mask | bit);  // 기존에 고르지 않은 사용자만 새로 배정하기
// states = move(next);  // 다음 패턴을 위한 상태로 바꾸기
// }  // 블록 끝
// return (int)states.size();  // 순서를 구분하지 않는 제재 사용자 집합 수 반환
// }  // 블록 끝

// 풀이 요약
// 패턴에 맞는 미사용 사용자를 하나씩 배정하고 비트 마스크 집합으로 같은 제재 사용자 조합의 중복 합치기
