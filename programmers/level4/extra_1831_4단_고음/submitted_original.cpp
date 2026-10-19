#include <vector>
#include <map>
#include <utility>
#include <functional>
using namespace std;

int solution(int n) {
    vector<long long> powers{1};
    while (powers.back() <= n) powers.push_back(powers.back() * 3);
    map<pair<int, int>, long long> memo;
    function<long long(int, int)> search = [&](int value, int pending) -> long long {
        if (value < 3) return 0;
        if (value == 3) return pending == 2;
        int required = (pending + 1) / 2;
        if (required >= static_cast<int>(powers.size()) || value < powers[required]) return 0;
        pair<int, int> key{value, pending};
        auto found = memo.find(key);
        if (found != memo.end()) return found->second;
        long long answer = search(value - 1, pending + 1);
        if (pending >= 2 && value % 3 == 0) answer += search(value / 3, pending - 2);
        memo[key] = answer;
        return answer;
    };
    return static_cast<int>(search(n - 2, 2));
}

// 전체 코드 줄별 설명
// #include <vector>  // #include는 헤더 포함. vector는 크기를 바꿀 수 있는 배열 제공.
// #include <map>  // map은 키를 정렬하여 저장하는 연관 배열. 계산한 상태별 결과 보관.
// #include <utility>  // utility는 pair 등 두 값을 묶는 도구 제공.
// #include <functional>  // functional은 재귀 람다를 담는 function 함수 객체 제공.
// using namespace std;  // std 이름 공간의 자료형을 접두사 없이 사용.
// 
// int solution(int n) {  // 정수를 받아 정수 개수를 반환하는 함수 정의. {}는 함수 본문.
//     vector<long long> powers{1};  // long long은 큰 정수형. 3의 거듭제곱을 저장할 벡터 초기화.
//     while (powers.back() <= n) powers.push_back(powers.back() * 3);  // back은 마지막 값, push_back은 끝에 추가. n을 넘는 3의 거듭제곱까지 저장.
//     map<pair<int, int>, long long> memo;  // (현재 음높이, 남은 + 수)를 키로 계산 결과를 저장하는 메모이제이션 표.
//     function<long long(int, int)> search = [&](int value, int pending) -> long long {  // function은 두 정수 입력의 함수 객체. [&]는 바깥 변수를 참조하는 람다이며 반환형은 큰 정수.
//         if (value < 3) return 0;  // if는 조건문. 첫 * 결과인 3보다 작으면 불가능.
//         if (value == 3) return pending == 2;  // ==는 같음 비교. 첫 *와 짝인 + 두 개만 남아야 하며 참은 1, 거짓은 0으로 반환.
//         int required = (pending + 1) / 2;  // 정수 /는 정수 몫. 남은 +를 짝짓는 데 필요한 최소 * 개수.
//         if (required >= static_cast<int>(powers.size()) || value < powers[required]) return 0;  // ||는 논리 OR. 필요한 거듭제곱보다 작은 불가능한 상태는 즉시 제외.
//         pair<int, int> key{value, pending};  // 두 상태 값을 pair로 묶어 map의 키 생성.
//         auto found = memo.find(key);  // auto는 자료형 자동 추론. find는 키를 찾는 반복자 반환.
//         if (found != memo.end()) return found->second;  // end는 찾지 못했을 때 위치, ->second는 반복자가 가리키는 계산 결과 값.
//         long long answer = search(value - 1, pending + 1);  // 마지막 +를 되돌리는 경우를 재귀 계산.
//         if (pending >= 2 && value % 3 == 0) answer += search(value / 3, pending - 2);  // &&는 논리 AND, %는 나머지. + 두 개를 소비하여 *를 되돌리는 경우 합산.
//         memo[key] = answer;  // []로 map에 계산 결과를 저장하여 같은 상태 재계산 방지.
//         return answer;  // 현재 상태의 가능한 문자열 수 반환.
//     };  // 람다 본문 종료 후 함수 객체 대입 문장 마침.
//     return static_cast<int>(search(n - 2, 2));  // 반드시 끝나는 ++를 먼저 제거. static_cast는 최종 반환형 int로 명시 변환.
// }  // solution 함수 본문 종료.

// 풀이 요약
// 올바른 문자열을 뒤에서 복원합니다. +는 음높이에서 1을 빼고 대기 +를 늘리며, *는 3으로 나누고 + 두 개와 짝짓습니다.
// 대기 +에 필요한 최소 곱셈 수로 불가능한 상태를 제외하고, map에 같은 상태의 결과를 저장합니다. 예: 2147483647의 답은 1735.
// 방문 상태 수 S에 대해 map 조회를 포함한 시간 O(S*log S), 공간 O(S). Python3 학습 코드를 함께 저장합니다.
// 