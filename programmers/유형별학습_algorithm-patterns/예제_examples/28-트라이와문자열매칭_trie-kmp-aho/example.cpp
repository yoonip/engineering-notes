#include <iostream>  // 문자 배열의 스트림 입출력
#include <cstring>  // 문자열 길이 계산

int next_node[201][26], terminal[201], nodes = 1;  // 0번 루트와 아직 없는 간선 0
int main() {  // 트라이와 KMP 비교 시작
    int n; char word[21], query[21], text[101], pattern[21];  // 고정 문자열 상한
    std::cin >> n;  // 사전 단어 수
    for (int i = 0; i < n; ++i) {  // 단어를 하나씩 삽입
        std::cin >> word;  // 현재 사전 단어
        int node = 0;  // 트라이 루트
        for (int j = 0; word[j]; ++j) {  // 한 문자씩 접두사 확장
            int letter = word[j] - 'a';  // 26개 자식 번호
            if (!next_node[node][letter]) next_node[node][letter] = nodes++;  // 필요한 노드만 새로 생성
            node = next_node[node][letter];  // 다음 접두사로 이동
        }  // 단어 경로 처리 끝
        terminal[node] = 1;  // 자식 유무와 별개인 단어 종료 표시
    }  // 사전 구축 끝
    std::cin >> query >> text >> pattern;  // 트라이 질의와 검색 문자열
    int node = 0, exists = 1;  // 질의 경로 존재 여부
    for (int i = 0; query[i]; ++i) {  // 질의 접두사 확인
        int child = next_node[node][query[i] - 'a'];  // 다음 문자 간선
        if (!child) { exists = 0; break; }  // 없는 경로면 즉시 종료
        node = child;  // 이어지는 접두사 상태
    }  // 트라이 질의 끝
    int pi[20] = {0}, length = (int)std::strlen(pattern);  // 패턴 경계 길이
    for (int i = 1; i < length; ++i) {  // 접두사 함수를 선형으로 구축
        int j = pi[i - 1];  // 직전의 가장 긴 경계
        while (j > 0 && pattern[i] != pattern[j]) j = pi[j - 1];  // 더 짧은 경계로 복구
        if (pattern[i] == pattern[j]) ++j;  // 같은 문자는 경계를 확장
        pi[i] = j;  // 현재 접두사의 경계 기록
    }  // 패턴 전처리 끝
    int matched = 0, count = 0;  // 현재 일치 길이와 발생 수
    for (int i = 0; text[i]; ++i) {  // 텍스트는 앞으로만 이동
        while (matched > 0 && text[i] != pattern[matched]) matched = pi[matched - 1];  // 겹친 후보 보존
        if (text[i] == pattern[matched]) ++matched;  // 현재 일치 확장
        if (matched == length) { ++count; matched = pi[matched - 1]; }  // 발생 기록 뒤 겹치는 검색 유지
    }  // 텍스트 검색 끝
    std::cout << "WORD " << (exists && terminal[node] ? "YES" : "NO") << "\n";  // 완전 단어 여부
    std::cout << "PREFIX " << (exists ? "YES" : "NO") << "\n";  // 접두사 경로 여부
    std::cout << "MATCHES " << count << "\n";  // 겹침을 포함한 발생 수
    return 0;  // 정상 종료
}  // 프로그램 끝
