#include <numeric>
#include <sstream>
#include <string>
#include <vector>
using namespace std;

vector<string> solution(vector<string> commands) {
    vector<int> groups(2500); iota(groups.begin(), groups.end(), 0);
    vector<string> values(2500), answer;
    auto position = [](const string& r, const string& c) { return (stoi(r) - 1) * 50 + stoi(c) - 1; };
    for (const string& command : commands) {
        vector<string> parts; string token; istringstream input(command); while (input >> token) parts.push_back(token);
        string operation = parts[0];
        if (operation == "UPDATE" && parts.size() == 4) values[groups[position(parts[1], parts[2])]] = parts[3];
        else if (operation == "UPDATE") { for (string& value : values) if (value == parts[1]) value = parts[2]; }
        else if (operation == "MERGE") {
            int first = groups[position(parts[1], parts[2])], second = groups[position(parts[3], parts[4])];
            if (first == second) continue;
            string value = values[first].empty() ? values[second] : values[first];
            for (int& group : groups) if (group == second) group = first;
            values[first] = value; values[second].clear();
        } else if (operation == "UNMERGE") {
            int cell = position(parts[1], parts[2]), group = groups[cell]; string value = values[group];
            vector<int> members; for (int i = 0; i < 2500; ++i) if (groups[i] == group) members.push_back(i);
            for (int member : members) { groups[member] = member; values[member].clear(); }
            values[cell] = value;
        } else {
            const string& value = values[groups[position(parts[1], parts[2])]];
            answer.push_back(value.empty() ? "EMPTY" : value);
        }
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <numeric>  // 누적합·최대공약수 같은 수치 알고리즘
// #include <sstream>  // 문자열에서 공백 단위로 값을 읽는 스트림
// #include <string>  // 문자열을 담는 string
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// vector<string> solution(vector<string> commands) {  // 칸의 그룹과 값을 나눠 병합·분리 명령 처리
// vector<int> groups(2500); iota(groups.begin(), groups.end(), 0);  // 50×50 표의 각 칸을 독립 그룹으로 시작
// vector<string> values(2500), answer;  // 그룹별 값과 출력 결과 저장
// auto position = [](const string& r, const string& c) { return (stoi(r) - 1) * 50 + stoi(c) - 1; };  // 행과 열을 일차원 칸 번호로 바꾸기
// for (const string& command : commands) {  // 명령을 입력 순서대로 처리
// vector<string> parts; string token; istringstream input(command); while (input >> token) parts.push_back(token);  // 명령의 공백 구분 항목 읽기
// string operation = parts[0];  // 명령 종류 읽기
// if (operation == "UPDATE" && parts.size() == 4) values[groups[position(parts[1], parts[2])]] = parts[3];  // 지정 칸이 속한 그룹의 값 바꾸기
// else if (operation == "UPDATE") { for (string& value : values) if (value == parts[1]) value = parts[2]; }  // 표 전체에서 기존 값을 새 값으로 바꾸기
// else if (operation == "MERGE") {  // 두 칸이 속한 그룹 합치기
// int first = groups[position(parts[1], parts[2])], second = groups[position(parts[3], parts[4])];  // 두 그룹의 번호 찾기
// if (first == second) continue;  // 이미 같은 그룹이면 바꾸지 않음
// string value = values[first].empty() ? values[second] : values[first];  // 첫 그룹의 비어 있지 않은 값을 우선
// for (int& group : groups) if (group == second) group = first;  // 둘째 그룹의 모든 칸을 첫 그룹에 연결
// values[first] = value; values[second].clear();  // 합친 그룹의 값을 정하고 옛 대표 값 지우기
// } else if (operation == "UNMERGE") {  // 지정 칸의 그룹을 독립 칸들로 나누기
// int cell = position(parts[1], parts[2]), group = groups[cell]; string value = values[group];  // 보존할 칸, 그룹, 값 저장
// vector<int> members; for (int i = 0; i < 2500; ++i) if (groups[i] == group) members.push_back(i);  // 원래 그룹의 모든 칸을 먼저 모으기
// for (int member : members) { groups[member] = member; values[member].clear(); }  // 각 칸을 값 없는 독립 그룹으로 만들기
// values[cell] = value;  // 지정한 칸 하나에만 기존 값을 보존
// } else {  // PRINT 명령의 결과 저장
// const string& value = values[groups[position(parts[1], parts[2])]];  // 해당 칸이 속한 그룹의 값 읽기
// answer.push_back(value.empty() ? "EMPTY" : value);  // 빈 값은 EMPTY 문자열로 출력
// }  // 블록 끝
// }  // 블록 끝
// return answer;  // 모든 PRINT 결과 반환
// }  // 블록 끝

// 풀이 요약
// 각 칸의 그룹 번호와 그룹 값을 관리하고 병합은 그룹 번호를 통일하며 분리는 구성 칸을 먼저 모아 독립시키기
