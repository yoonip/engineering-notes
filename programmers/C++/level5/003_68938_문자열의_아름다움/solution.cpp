#include <string>
#include <vector>

using namespace std;

long long solution(string s) {
    int n = (int)s.size();
    int longest[26] = {0};
    for (int start = 0; start < n; ) {
        int end = start + 1;
        while (end < n && s[end] == s[start]) ++end;
        int letter = s[start] - 'a', length = end - start;
        if (length > longest[letter]) longest[letter] = length;
        start = end;
    }
    size_t offset[26], slots = 0;
    for (int letter = 0; letter < 26; ++letter) {
        offset[letter] = slots;
        slots += (size_t)longest[letter] + 1;
    }
    vector<long long> previous(slots, 0);
    long long answer = (long long)n * (n - 1) * (n + 1) / 6;
    for (int start = 0; start < n; ) {
        int end = start + 1;
        while (end < n && s[end] == s[start]) ++end;
        int letter = s[start] - 'a';
        long long length = end - start;
        answer -= length * (length - 1) * (length + 1) / 6;
        for (int need = 1; need <= length; ++need) {
            long long choices = length - need + 1;
            size_t index = offset[letter] + (size_t)need;
            answer -= choices * previous[index];
            previous[index] += choices;
        }
        start = end;
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <string>  // 입력 문자열을 받는 string
// #include <vector>  // 초깃값 0인 가변 길이 누적 배열
// 
// using namespace std;  // 표준 string과 vector 이름을 짧게 사용
// 
// long long solution(string s) {  // 영어 소문자 문자열을 받아 아름다움의 총합을 64비트 정수로 반환
//     int n = (int)s.size();  // 부분문자열 길이 합의 기준이 되는 전체 문자 수
//     int longest[26] = {0};  // 문자별 가장 긴 연속구간 길이; 필요한 누적 배열 크기만 확보
//     for (int start = 0; start < n; ) {  // 같은 문자가 이어지는 최대 연속구간을 차례로 찾기
//         int end = start + 1;  // 이번 연속구간의 오른쪽 경계 후보
//         while (end < n && s[end] == s[start]) ++end;  // 문자가 같을 때만 구간을 늘려 첫 다른 문자 직전에서 멈춤
//         int letter = s[start] - 'a', length = end - start;  // 이번 구간의 알파벳 번호와 길이
//         if (length > longest[letter]) longest[letter] = length;  // 이 문자의 누적 배열에서 사용할 최대 깊이 갱신
//         start = end;  // 방금 센 구간 다음 문자부터 다시 탐색
//     }  // 문자별 최대 연속길이 조사 끝
//     size_t offset[26], slots = 0;  // 문자별 누적 배열의 시작 위치와 전체 저장 칸 수
//     for (int letter = 0; letter < 26; ++letter) {  // 26개 문자의 배열을 한 저장 공간에 이어 배치
//         offset[letter] = slots;  // 이 문자 전용 누적 배열의 시작 칸
//         slots += (size_t)longest[letter] + 1;  // 깊이 1부터 최대 연속길이까지 사용; 0번 칸은 비워 둠
//     }  // 문자별 배열 위치 계산 끝
//     vector<long long> previous(slots, 0);  // previous[문자][k]: 이전 같은 문자 구간에서 연속 k글자를 남길 수 있는 시작점 수
//     long long answer = (long long)n * (n - 1) * (n + 1) / 6;  // 모든 부분문자열의 길이에서 1을 뺀 값의 합; 곱셈부터 64비트로 계산
//     for (int start = 0; start < n; ) {  // 이번에는 연속구간마다 실제 아름다움과의 차이를 차감
//         int end = start + 1;  // 현재 구간의 끝을 다시 찾을 준비
//         while (end < n && s[end] == s[start]) ++end;  // 현재 문자와 같은 연속구간 전체를 묶음
//         int letter = s[start] - 'a';  // 같은 문자로 시작한 이전 구간의 누적값 선택
//         long long length = end - start;  // 세제곱 규모의 구간 합을 안전하게 계산할 64비트 길이
//         answer -= length * (length - 1) * (length + 1) / 6;  // 이 한 구간 안의 부분문자열은 모두 아름다움 0이므로 기본 합 전부 차감
//         for (int need = 1; need <= length; ++need) {  // 양끝의 같은 문자 길이가 need 이상일 때 생기는 감점 1씩 합산
//             long long choices = length - need + 1;  // 현재 구간에서 끝쪽 같은 문자를 need개 이상 포함하는 끝점 수
//             size_t index = offset[letter] + (size_t)need;  // 같은 문자·같은 필요 길이의 이전 시작점 누적 칸
//             answer -= choices * previous[index];  // 이전 시작점과 현재 끝점의 모든 조합에서 감점 1씩 차감
//             previous[index] += choices;  // 현재 구간의 시작점 후보를 이후 같은 문자 구간을 위해 누적
//         }  // 구간 길이만큼만 처리하므로 전체 need 반복 횟수는 N
//         start = end;  // 다음 연속구간으로 이동
//     }  // 모든 같은 문자 양끝 조합의 감점 계산 끝
//     return answer;  // 보정이 끝난 모든 부분문자열 아름다움의 합
// }  // 풀이 함수 끝

// 풀이 요약
// 길이가 m인 부분문자열의 아름다움은 최대 m-1. 이 상한을 전부 더한 N(N-1)(N+1)/6에서 부족한 거리만 빼기.
// 양끝 문자가 다르면 상한 그대로. 양끝 문자가 같고 중간에 다른 문자가 있으면 양끝의 같은 문자 연속길이 중 작은 값만큼 줄어듦.
// 한 연속구간 안의 부분문자열은 전부 0이므로 구간 길이 L마다 L(L-1)(L+1)/6을 먼저 차감.
// 서로 떨어진 같은 문자 구간의 길이가 A, B일 때 감점은 sum(k=1..min(A,B)) (A-k+1)(B-k+1). 감점이 k 이상인 시작점·끝점 조합을 세는 방식.
// previous[문자][k]에 이전 구간들의 시작점 수를 누적해 두면, 현재 구간에서 L-k+1을 곱하고 더하는 것만으로 계산 가능.
// 모든 구간 길이의 합이 N이어서 시간 O(N). 문자별 최대 연속길이 합도 N 이하여서 공간 O(N). baby는 9, oo는 0.
