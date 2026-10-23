#include <functional>
#include <vector>
using namespace std;

long long solution(int n, long long l, long long r) {
    vector<long long> power5(n + 1, 1), power4(n + 1, 1);
    for (int i = 1; i <= n; ++i) { power5[i] = power5[i - 1] * 5; power4[i] = power4[i - 1] * 4; }
    function<long long(int, long long)> prefix = [&](int level, long long length) -> long long {
        if (level == 0) return length;
        long long block = power5[level - 1];
        long long groups = length / block, rest = length % block;
        long long full = groups - (groups > 2);
        long long total = full * power4[level - 1];
        if (groups == 2) return total;
        return total + prefix(level - 1, rest);
    };
    return prefix(n, r) - prefix(n, l - 1);
}

// 전체 코드 줄별 설명
// #include <functional>  // 재귀 람다를 담는 function과 함수 객체
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// long long solution(int n, long long l, long long r) {  // 가운데 0 블록을 건너뛰며 구간의 1 개수 계산
// vector<long long> power5(n + 1, 1), power4(n + 1, 1);  // 단계별 길이와 1의 수 저장
// for (int i = 1; i <= n; ++i) { power5[i] = power5[i - 1] * 5; power4[i] = power4[i - 1] * 4; }  // 5와 4의 거듭제곱을 미리 구하기
// function<long long(int, long long)> prefix = [&](int level, long long length) -> long long {  // 앞에서 length개까지의 1의 수를 재귀적으로 계산
// if (level == 0) return length;  // 가장 작은 비트열의 접두사 개수 반환
// long long block = power5[level - 1];  // 현재 단계를 구성하는 한 블록의 길이
// long long groups = length / block, rest = length % block;  // 완전히 포함한 블록 수와 남은 길이 구하기
// long long full = groups - (groups > 2);  // 가운데의 0 블록을 완전 블록 수에서 제외
// long long total = full * power4[level - 1];  // 완전히 포함한 유효 블록의 1 세기
// if (groups == 2) return total;  // 나머지가 가운데 0 블록에 있으면 더 셀 필요가 없음
// return total + prefix(level - 1, rest);  // 마지막 부분 블록의 1을 재귀적으로 더하기
// };  // 블록 끝
// return prefix(n, r) - prefix(n, l - 1);  // 두 접두사의 차이로 닫힌 구간의 1 세기
// }  // 블록 끝

// 풀이 요약
// 비트열의 다섯 블록 중 가운데 0 블록을 제외하고 완전 블록과 마지막 부분 블록의 1을 재귀적으로 세기
