// string은 문자열 자료형.
#include <string>
// vector는 가변 길이 배열.
#include <vector>
// reverse 등 알고리즘 도구 제공.
#include <algorithm>
// std 이름 공간 도구 사용.
using namespace std;

// 문자열을 받아 원문 또는 invalid를 반환하는 함수.
string solution(string sentence) {
    int n = sentence.size();
    if (n == 0) return "invalid";
    // 소문자 26개별 전체 출현 위치 목록.
    vector<vector<int>> positions(26);
    // 대문자 판별 함수.
    auto upper = [](char ch) { return 'A' <= ch && ch <= 'Z'; };
    // ++는 1 증가.
    for (int i = 0; i < n; ++i) {
        // []로 글자 조회.
        char ch = sentence[i];
        // push_back은 위치 추가.
        if ('a' <= ch && ch <= 'z') positions[ch - 'a'].push_back(i);
        // 영문 이외 글자나 공백은 거절.
        else if (!upper(ch)) return "invalid";
    }
    // 바깥 기호를 제외한 단어 내용 검사.
    auto read_word = [&](int left, int right) -> string {
        // 빈 내용이나 소문자 시작은 실패.
        if (left >= right || !upper(sentence[left])) return "";
        // 대문자만 있는지 확인.
        bool plain = true;
        // 구간의 기호 존재 여부 검사.
        for (int p = left; p < right; ++p) if (!upper(sentence[p])) plain = false;
        // 대문자만 있으면 그대로 반환.
        if (plain) return sentence.substr(left, right - left);
        // 현재 구간 길이.
        int length = right - left;
        // 규칙1이라면 둘째 글자가 삽입 기호.
        char marker = sentence[left + 1];
        // 규칙1은 홀수 길이·소문자 기호 필요.
        if (length % 2 == 0 || marker < 'a' || marker > 'z') return "";
        // 기호 전체 출현 위치를 복사 없이 조회.
        auto &found = positions[marker - 'a'];
        // 이 단어 밖에서 같은 기호가 쓰이면 실패.
        if (found.front() != left + 1 || found.back() != right - 2 || found.size() != length / 2) return "";
        // 원래 대문자를 담을 문자열.
        string word;
        // 구간 글자 순회.
        for (int p = left; p < right; ++p) {
            // 짝수 위치는 원문 글자 자리.
            if ((p - left) % 2 == 0) {
                // 대문자가 아니면 실패.
                if (!upper(sentence[p])) return "";
                // 원문 글자 수집.
                word += sentence[p];
            } else if (sentence[p] != marker) return "";
        }
        // 기호를 제거한 단어 반환.
        return word;
    };
    // -2는 앞부분 해석 불가능.
    vector<int> previous(n + 1, -2);
    // 도달 위치별 마지막 복원 단어.
    vector<string> decoded(n + 1);
    // 빈 앞부분은 해석 가능.
    previous[0] = -1;
    // 단어 하나로 끝 위치에 도달했음을 기록하는 람다.
    auto save = [&](int start, int end, string word) {
        // 아직 방문하지 않은 유효한 상태만 저장.
        if (!word.empty() && previous[end] == -2) {
            // 직전 위치 기록.
            previous[end] = start;
            // 복원 단어 기록.
            decoded[end] = word;
        }
    };
    // 시작 위치를 왼쪽부터 순회하는 DP.
    for (int start = 0; start < n; ++start) {
        // 앞부분을 해석할 수 없으면 제외.
        if (previous[start] == -2) continue;
        // 현재 글자 조회.
        char ch = sentence[start];
        // 대문자로 시작하면 일반 단어·규칙1 후보.
        if (upper(ch)) {
            // 일반 단어의 끝 후보.
            int end = start;
            // 연속한 대문자 안의 모든 단어 경계를 확인.
            while (end < n && upper(sentence[end])) {
                ++end;
                // 기호 없는 단어 후보 저장.
                if (previous[end] == -2) save(start, end, sentence.substr(start, end - start));
            }
            // 둘째 글자가 소문자면 규칙1 시도.
            if (start + 1 < n && !upper(sentence[start + 1])) {
                // 같은 기호의 마지막 출현 다음 대문자까지.
                int end = positions[sentence[start + 1] - 'a'].back() + 2;
                // 구간 전체가 유효한 규칙1이면 저장.
                if (end <= n) save(start, end, read_word(start, end));
            }
        // 소문자로 시작하면 규칙2만 가능.
        } else {
            // 바깥 기호 전체 위치 참조.
            auto &found = positions[ch - 'a'];
            // 기호가 정확히 두 번이고 첫 위치여야 함.
            if (found.size() == 2 && found.front() == start) {
                // 닫는 바깥 기호 위치.
                int close = found.back();
                // 안쪽 일반 단어 또는 다른 기호 규칙1을 검사해 저장.
                save(start, close + 1, read_word(start + 1, close));
            }
        }
    }
    // 끝까지 해석할 수 없으면 실패.
    if (previous[n] == -2) return "invalid";
    // 복원 단어를 거꾸로 담는 배열.
    vector<string> words;
    // 직전 경계를 따라 마지막 단어부터 추적.
    for (int end = n; end > 0; end = previous[end]) words.push_back(decoded[end]);
    // 배열을 제자리에서 뒤집어 실제 순서로 변경.
    reverse(words.begin(), words.end());
    string answer;
    // 단어를 순서대로 순회.
    for (string word : words) {
        // 첫 단어 이후에만 공백 하나 추가.
        if (!answer.empty()) answer += ' ';
        // 단어 이어 붙이기.
        answer += word;
    }
    // 가능한 원문 하나 반환.
    return answer;
}
