#include <string>
#include <vector>
#include <algorithm>
using namespace std;

string solution(string sentence) {
    int n = sentence.size();
    if (n == 0) return "invalid";
    vector<vector<int>> positions(26);
    auto upper = [](char ch) { return 'A' <= ch && ch <= 'Z'; };
    for (int i = 0; i < n; ++i) {
        char ch = sentence[i];
        if ('a' <= ch && ch <= 'z') positions[ch - 'a'].push_back(i);
        else if (!upper(ch)) return "invalid";
    }
    auto read_word = [&](int left, int right) -> string {
        if (left >= right || !upper(sentence[left])) return "";
        bool plain = true;
        for (int p = left; p < right; ++p) if (!upper(sentence[p])) plain = false;
        if (plain) return sentence.substr(left, right - left);
        int length = right - left;
        char marker = sentence[left + 1];
        if (length % 2 == 0 || marker < 'a' || marker > 'z') return "";
        auto &found = positions[marker - 'a'];
        if (found.front() != left + 1 || found.back() != right - 2 || found.size() != length / 2) return "";
        string word;
        for (int p = left; p < right; ++p) {
            if ((p - left) % 2 == 0) {
                if (!upper(sentence[p])) return "";
                word += sentence[p];
            } else if (sentence[p] != marker) return "";
        }
        return word;
    };
    vector<int> previous(n + 1, -2);
    vector<string> decoded(n + 1);
    previous[0] = -1;
    auto save = [&](int start, int end, string word) {
        if (!word.empty() && previous[end] == -2) {
            previous[end] = start;
            decoded[end] = word;
        }
    };
    for (int start = 0; start < n; ++start) {
        if (previous[start] == -2) continue;
        char ch = sentence[start];
        if (upper(ch)) {
            int end = start;
            while (end < n && upper(sentence[end])) {
                ++end;
                save(start, end, sentence.substr(start, end - start));
            }
            if (start + 1 < n && !upper(sentence[start + 1])) {
                int end = positions[sentence[start + 1] - 'a'].back() + 2;
                if (end <= n) save(start, end, read_word(start, end));
            }
        } else {
            auto &found = positions[ch - 'a'];
            if (found.size() == 2 && found.front() == start) {
                int close = found.back();
                save(start, close + 1, read_word(start + 1, close));
            }
        }
    }
    if (previous[n] == -2) return "invalid";
    vector<string> words;
    for (int end = n; end > 0; end = previous[end]) words.push_back(decoded[end]);
    reverse(words.begin(), words.end());
    string answer;
    for (string word : words) {
        if (!answer.empty()) answer += ' ';
        answer += word;
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <string>  // #include는 헤더 가져오기. string은 문자열 자료형.
// #include <vector>  // vector는 가변 길이 배열.
// #include <algorithm>  // reverse 등 알고리즘 도구 제공.
// using namespace std;  // std 이름 공간 도구 사용.
// 
// string solution(string sentence) {  // 문자열을 받아 원문 또는 invalid를 반환하는 함수.
//     int n = sentence.size();  // size는 길이. int는 정수.
//     if (n == 0) return "invalid";  // ==는 같음. 빈 입력 거절.
//     vector<vector<int>> positions(26);  // 소문자 26개별 전체 출현 위치 목록.
//     auto upper = [](char ch) { return 'A' <= ch && ch <= 'Z'; };  // []는 캡처 없는 람다, char는 글자. &&는 모두 참. 대문자 판별 함수.
//     for (int i = 0; i < n; ++i) {  // 모든 글자 순회. ++는 1 증가.
//         char ch = sentence[i];  // []로 글자 조회.
//         if ('a' <= ch && ch <= 'z') positions[ch - 'a'].push_back(i);  // 문자 차이로 기호 인덱스 생성. push_back은 위치 추가.
//         else if (!upper(ch)) return "invalid";  // !는 부정. 영문 이외 글자나 공백은 거절.
//     }  // 위치 수집 종료.
//     auto read_word = [&](int left, int right) -> string {  // [&]는 주변 변수 참조, -> string은 반환형 명시. 바깥 기호를 제외한 단어 내용 검사.
//         if (left >= right || !upper(sentence[left])) return "";  // ||는 하나라도 참. 빈 내용이나 소문자 시작은 실패.
//         bool plain = true;  // bool은 참·거짓. 대문자만 있는지 확인.
//         for (int p = left; p < right; ++p) if (!upper(sentence[p])) plain = false;  // 구간의 기호 존재 여부 검사.
//         if (plain) return sentence.substr(left, right - left);  // substr(시작,길이)는 부분문자열. 대문자만 있으면 그대로 반환.
//         int length = right - left;  // 현재 구간 길이.
//         char marker = sentence[left + 1];  // 규칙1이라면 둘째 글자가 삽입 기호.
//         if (length % 2 == 0 || marker < 'a' || marker > 'z') return "";  // %는 나머지. 규칙1은 홀수 길이·소문자 기호 필요.
//         auto &found = positions[marker - 'a'];  // &는 참조. 기호 전체 출현 위치를 복사 없이 조회.
//         if (found.front() != left + 1 || found.back() != right - 2 || found.size() != length / 2) return "";  // front·back은 처음·마지막 원소. 이 단어 밖에서 같은 기호가 쓰이면 실패.
//         string word;  // 원래 대문자를 담을 문자열.
//         for (int p = left; p < right; ++p) {  // 구간 글자 순회.
//             if ((p - left) % 2 == 0) {  // 짝수 위치는 원문 글자 자리.
//                 if (!upper(sentence[p])) return "";  // 대문자가 아니면 실패.
//                 word += sentence[p];  // +=는 뒤에 이어 붙이기. 원문 글자 수집.
//             } else if (sentence[p] != marker) return "";  // 홀수 위치는 동일 기호여야 함. !=는 다름.
//         }  // 글자 검사 종료.
//         return word;  // 기호를 제거한 단어 반환.
//     };  // 람다 정의 끝.
//     vector<int> previous(n + 1, -2);  // 직전 단어 시작 위치. -2는 앞부분 해석 불가능.
//     vector<string> decoded(n + 1);  // 도달 위치별 마지막 복원 단어.
//     previous[0] = -1;  // 빈 앞부분은 해석 가능.
//     auto save = [&](int start, int end, string word) {  // 단어 하나로 끝 위치에 도달했음을 기록하는 람다.
//         if (!word.empty() && previous[end] == -2) {  // empty는 비었는지 검사. 아직 방문하지 않은 유효한 상태만 저장.
//             previous[end] = start;  // 직전 위치 기록.
//             decoded[end] = word;  // 복원 단어 기록.
//         }  // 저장 조건 종료.
//     };  // 람다 정의 끝.
//     for (int start = 0; start < n; ++start) {  // 시작 위치를 왼쪽부터 순회하는 DP.
//         if (previous[start] == -2) continue;  // continue는 이번 반복 건너뜀. 앞부분을 해석할 수 없으면 제외.
//         char ch = sentence[start];  // 현재 글자 조회.
//         if (upper(ch)) {  // 대문자로 시작하면 일반 단어·규칙1 후보.
//             int end = start;  // 일반 단어의 끝 후보.
//             while (end < n && upper(sentence[end])) {  // 연속한 대문자 안의 모든 단어 경계를 확인.
//                 ++end;  // 한 글자 확장.
//                 save(start, end, sentence.substr(start, end - start));  // 기호 없는 단어 후보 저장.
//             }  // 일반 단어 검사 종료.
//             if (start + 1 < n && !upper(sentence[start + 1])) {  // 둘째 글자가 소문자면 규칙1 시도.
//                 int end = positions[sentence[start + 1] - 'a'].back() + 2;  // 같은 기호의 마지막 출현 다음 대문자까지.
//                 if (end <= n) save(start, end, read_word(start, end));  // 구간 전체가 유효한 규칙1이면 저장.
//             }  // 규칙1 검사 종료.
//         } else {  // 소문자로 시작하면 규칙2만 가능.
//             auto &found = positions[ch - 'a'];  // 바깥 기호 전체 위치 참조.
//             if (found.size() == 2 && found.front() == start) {  // 기호가 정확히 두 번이고 첫 위치여야 함.
//                 int close = found.back();  // 닫는 바깥 기호 위치.
//                 save(start, close + 1, read_word(start + 1, close));  // 안쪽 일반 단어 또는 다른 기호 규칙1을 검사해 저장.
//             }  // 규칙2 검사 종료.
//         }  // 시작 글자 분기 종료.
//     }  // DP 반복 종료.
//     if (previous[n] == -2) return "invalid";  // 끝까지 해석할 수 없으면 실패.
//     vector<string> words;  // 복원 단어를 거꾸로 담는 배열.
//     for (int end = n; end > 0; end = previous[end]) words.push_back(decoded[end]);  // 직전 경계를 따라 마지막 단어부터 추적.
//     reverse(words.begin(), words.end());  // 배열을 제자리에서 뒤집어 실제 순서로 변경.
//     string answer;  // 결과 문자열.
//     for (string word : words) {  // 단어를 순서대로 순회.
//         if (!answer.empty()) answer += ' ';  // 첫 단어 이후에만 공백 하나 추가.
//         answer += word;  // 단어 이어 붙이기.
//     }  // 단어 연결 종료.
//     return answer;  // 가능한 원문 하나 반환.
// }  // 함수 종료.

// 풀이 요약
// 하나의 단어 구간은 대문자만, 규칙1(대문자·기호 번갈아), 규칙2(기호로 감싸기), 두 규칙의 결합 중 하나다. 같은 기호의 전체 출현이 한 구간 안에서만 쓰이는지 검사한다.
// previous[end]에 앞부분을 유효하게 해석한 마지막 단어를 저장하는 DP를 사용한다. 가능한 경계를 모두 확인하므로 규칙1·2로 둘 다 해석되는 경우도 처리한다.
// 기호 재사용·기호 교차·두 규칙 중복은 구간 검사에서 거절한다. 길이 L≤1000, 시간·저장 문자열을 포함한 공간 O(L²). 가능한 원문 중 하나를 반환한다.
// 