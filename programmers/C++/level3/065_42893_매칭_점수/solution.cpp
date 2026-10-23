#include <algorithm>
#include <cctype>
#include <cstdint>
#include <numeric>
#include <regex>
#include <string>
#include <unordered_map>
#include <vector>
using namespace std;

static unsigned matching_mod(const vector<unsigned>& value, unsigned divisor) {
    unsigned long long remainder = 0;
    for (auto it = value.rbegin(); it != value.rend(); ++it) remainder = (remainder * 1000000000ULL + *it) % divisor;
    return (unsigned)remainder;
}

static vector<unsigned> matching_multiply(vector<unsigned> value, unsigned factor) {
    unsigned long long carry = 0;
    for (unsigned& digit : value) { unsigned long long product = 1ULL * digit * factor + carry; digit = product % 1000000000ULL; carry = product / 1000000000ULL; }
    while (carry) { value.push_back(carry % 1000000000ULL); carry /= 1000000000ULL; }
    while (value.size() > 1 && value.back() == 0) value.pop_back();
    return value;
}

static vector<unsigned> matching_divide(vector<unsigned> value, unsigned divisor) {
    unsigned long long remainder = 0;
    for (int i = (int)value.size() - 1; i >= 0; --i) { unsigned long long current = remainder * 1000000000ULL + value[i]; value[i] = current / divisor; remainder = current % divisor; }
    while (value.size() > 1 && value.back() == 0) value.pop_back();
    return value;
}

static void matching_add(vector<unsigned>& first, const vector<unsigned>& second) {
    first.resize(max(first.size(), second.size()), 0); unsigned carry = 0;
    for (size_t i = 0; i < first.size(); ++i) { unsigned long long sum = 1ULL * first[i] + (i < second.size() ? second[i] : 0) + carry; first[i] = sum % 1000000000ULL; carry = sum / 1000000000ULL; }
    if (carry) first.push_back(carry);
}

int solution(string word, vector<string> pages) {
    for (char& c : word) c = (char)tolower((unsigned char)c);
    regex meta(R"rx(<meta\b[^>]*\bproperty\s*=\s*"og:url"[^>]*>)rx", regex::icase), content(R"rx(\bcontent\s*=\s*"([^"]+)")rx", regex::icase), anchor(R"rx(<a\s+href\s*=\s*"([^"]+)")rx", regex::icase), letters("[a-z]+");
    int n = (int)pages.size(); vector<string> addresses; vector<vector<string>> links(n); vector<int> basic(n,0);
    vector<unsigned> denominator{1};
    for (int i = 0; i < n; ++i) {
        smatch match; regex_search(pages[i], match, meta); string tag = match.str(); regex_search(tag, match, content); addresses.push_back(match[1].str());
        for (sregex_iterator it(pages[i].begin(), pages[i].end(), anchor), end; it != end; ++it) links[i].push_back((*it)[1].str());
        string lower = pages[i]; for (char& c : lower) c = (char)tolower((unsigned char)c);
        for (sregex_iterator it(lower.begin(), lower.end(), letters), end; it != end; ++it) basic[i] += it->str() == word;
        if (!links[i].empty()) { unsigned size = (unsigned)links[i].size(); denominator = matching_multiply(denominator, size / gcd(matching_mod(denominator,size), size)); }
    }
    unordered_map<string,int> index; for (int i = 0; i < n; ++i) index[addresses[i]] = i;
    vector<vector<unsigned>> scores; for (int score : basic) scores.push_back(matching_multiply(denominator, score));
    for (int i = 0; i < n; ++i) if (!links[i].empty()) {
        vector<unsigned> share = matching_multiply(matching_divide(denominator, (unsigned)links[i].size()), basic[i]);
        for (const string& url : links[i]) { auto found = index.find(url); if (found != index.end()) matching_add(scores[found->second], share); }
    }
    int answer = 0;
    for (int i = 1; i < n; ++i) if (scores[i].size() > scores[answer].size() || (scores[i].size() == scores[answer].size() && lexicographical_compare(scores[answer].rbegin(), scores[answer].rend(), scores[i].rbegin(), scores[i].rend()))) answer = i;
    return answer;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <cctype>  // 문자 분류와 대소문자 변환
// #include <cstdint>  // 비트 수가 정해진 정수 자료형
// #include <numeric>  // 누적합·최대공약수 같은 수치 알고리즘
// #include <regex>  // 정규식 검색
// #include <string>  // 문자열을 담는 string
// #include <unordered_map>  // 키로 값을 찾는 해시 맵
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// static unsigned matching_mod(const vector<unsigned>& value, unsigned divisor) {  // 큰 정수를 divisor로 나눈 나머지
// unsigned long long remainder = 0;  // 큰 정수의 나머지를 높은 자릿수부터 누적
// for (auto it = value.rbegin(); it != value.rend(); ++it) remainder = (remainder * 1000000000ULL + *it) % divisor;  // 밑 10억의 각 자릿수를 반영
// return (unsigned)remainder;  // 작은 정수로 나눈 나머지 반환
// }  // 블록 끝
// static vector<unsigned> matching_multiply(vector<unsigned> value, unsigned factor) {  // 큰 정수에 작은 정수 factor 곱하기
// unsigned long long carry = 0;  // 작은 정수 곱셈의 올림 저장
// for (unsigned& digit : value) { unsigned long long product = 1ULL * digit * factor + carry; digit = product % 1000000000ULL; carry = product / 1000000000ULL; }  // 각 자릿수에 곱하고 올림을 넘기기
// while (carry) { value.push_back(carry % 1000000000ULL); carry /= 1000000000ULL; }  // 남은 높은 자릿수의 올림 저장
// while (value.size() > 1 && value.back() == 0) value.pop_back();  // 불필요한 앞자리 0 제거
// return value;  // 정확한 큰 정수 곱 반환
// }  // 블록 끝
// static vector<unsigned> matching_divide(vector<unsigned> value, unsigned divisor) {  // 큰 정수를 작은 정수 divisor로 나누기
// unsigned long long remainder = 0;  // 긴 나눗셈의 나머지 저장
// for (int i = (int)value.size() - 1; i >= 0; --i) { unsigned long long current = remainder * 1000000000ULL + value[i]; value[i] = current / divisor; remainder = current % divisor; }  // 높은 자릿수부터 몫 구하기
// while (value.size() > 1 && value.back() == 0) value.pop_back();  // 몫의 앞자리 0 제거
// return value;  // 공통 분모를 작은 분모로 나눈 정확한 몫 반환
// }  // 블록 끝
// static void matching_add(vector<unsigned>& first, const vector<unsigned>& second) {  // 큰 정수 second를 first에 자리올림하며 더하기
// first.resize(max(first.size(), second.size()), 0); unsigned carry = 0;  // 두 큰 정수의 길이를 맞추기
// for (size_t i = 0; i < first.size(); ++i) { unsigned long long sum = 1ULL * first[i] + (i < second.size() ? second[i] : 0) + carry; first[i] = sum % 1000000000ULL; carry = sum / 1000000000ULL; }  // 자릿수별 덧셈과 올림 처리
// if (carry) first.push_back(carry);  // 마지막 올림이 있으면 높은 자릿수에 붙이기
// }  // 블록 끝
// int solution(string word, vector<string> pages) {  // 큰 정수 분모를 맞춰 매칭 점수를 정확히 비교
// for (char& c : word) c = (char)tolower((unsigned char)c);  // 검색 단어의 대소문자를 통일
// regex meta(R"rx(<meta\b[^>]*\bproperty\s*=\s*"og:url"[^>]*>)rx", regex::icase), content(R"rx(\bcontent\s*=\s*"([^"]+)")rx", regex::icase), anchor(R"rx(<a\s+href\s*=\s*"([^"]+)")rx", regex::icase), letters("[a-z]+");  // 페이지 주소, 링크, 영단어를 읽을 정규식 선언
// int n = (int)pages.size(); vector<string> addresses; vector<vector<string>> links(n); vector<int> basic(n,0);  // 페이지별 주소와 외부 링크 및 기본 점수 저장
// vector<unsigned> denominator{1};  // 모든 링크 점수를 정수로 비교할 공통 분모 만들기
// for (int i = 0; i < n; ++i) {  // 각 페이지의 정보를 추출
// smatch match; regex_search(pages[i], match, meta); string tag = match.str(); regex_search(tag, match, content); addresses.push_back(match[1].str());  // 메타 태그의 대표 주소 읽기
// for (sregex_iterator it(pages[i].begin(), pages[i].end(), anchor), end; it != end; ++it) links[i].push_back((*it)[1].str());  // 페이지의 모든 외부 링크 주소 읽기
// string lower = pages[i]; for (char& c : lower) c = (char)tolower((unsigned char)c);  // 기본 점수 계산용 문자열을 소문자로 바꾸기
// for (sregex_iterator it(lower.begin(), lower.end(), letters), end; it != end; ++it) basic[i] += it->str() == word;  // 연속 영문 단어가 검색어와 같은 횟수 세기
// if (!links[i].empty()) { unsigned size = (unsigned)links[i].size(); denominator = matching_multiply(denominator, size / gcd(matching_mod(denominator,size), size)); }  // 링크 수들의 최소공배수를 큰 정수로 갱신
// }  // 블록 끝
// unordered_map<string,int> index; for (int i = 0; i < n; ++i) index[addresses[i]] = i;  // 페이지 주소를 점수 배열의 인덱스로 연결
// vector<vector<unsigned>> scores; for (int score : basic) scores.push_back(matching_multiply(denominator, score));  // 기본 점수를 공통 분모 배율의 정확한 정수로 바꾸기
// for (int i = 0; i < n; ++i) if (!links[i].empty()) {  // 외부 링크가 있는 페이지의 링크 점수를 배분
// vector<unsigned> share = matching_multiply(matching_divide(denominator, (unsigned)links[i].size()), basic[i]);  // 기본 점수를 링크 수로 나눈 값을 공통 분모의 정수로 구하기
// for (const string& url : links[i]) { auto found = index.find(url); if (found != index.end()) matching_add(scores[found->second], share); }  // 실제 주어진 대상 페이지에만 링크 점수를 더하기
// }  // 블록 끝
// int answer = 0;  // 점수가 같으면 가장 작은 인덱스 유지
// for (int i = 1; i < n; ++i) if (scores[i].size() > scores[answer].size() || (scores[i].size() == scores[answer].size() && lexicographical_compare(scores[answer].rbegin(), scores[answer].rend(), scores[i].rbegin(), scores[i].rend()))) answer = i;  // 큰 정수의 자릿수와 높은 자리부터 정확히 점수 비교
// return answer;  // 가장 높은 매칭 점수의 페이지 인덱스 반환
// }  // 블록 끝

// 풀이 요약
// 기본 점수와 외부 링크를 추출하고 링크 수들의 최소공배수를 직접 구현한 큰 정수로 관리해 유리수 매칭 점수를 정확히 비교
