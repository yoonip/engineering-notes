#include <functional>
using namespace std;

int solution(int n) {
    int full = (1 << n) - 1;
    function<int(int, int, int)> search = [&](int columns, int left, int right) {
        if (columns == full) return 1;
        int available = full & ~(columns | left | right), count = 0;
        while (available) {
            int position = available & -available; available -= position;
            count += search(columns | position, (left | position) << 1, (right | position) >> 1);
        }
        return count;
    };
    return search(0, 0, 0);
}

// 전체 코드 줄별 설명
// #include <functional>  // 재귀 람다를 담는 function과 함수 객체
// using namespace std;  // std:: 접두사 생략
// int solution(int n) {  // 열·대각선 비트 마스크로 다음 퀸 자리 선택
// int full = (1 << n) - 1;  // n개의 열이 모두 차 있는 상태를 비트 마스크로 만들기
// function<int(int, int, int)> search = [&](int columns, int left, int right) {  // 열과 두 대각선의 공격 범위를 상태로 탐색
// if (columns == full) return 1;  // 모든 행에 퀸을 놓았으면 한 가지 배치
// int available = full & ~(columns | left | right), count = 0;  // 현재 행에서 공격받지 않는 열과 배치 수 구하기
// while (available) {  // 가능한 각 열에 퀸을 놓아 보기
// int position = available & -available; available -= position;  // 가장 낮은 가능 비트 하나 꺼내기
// count += search(columns | position, (left | position) << 1, (right | position) >> 1);  // 다음 행의 열과 대각선 공격 범위를 계산해 재귀 탐색
// }  // 블록 끝
// return count;  // 현재 상태에서 가능한 배치 수 반환
// };  // 블록 끝
// return search(0, 0, 0);  // 퀸을 놓지 않은 상태에서 시작
// }  // 블록 끝

// 풀이 요약
// 퀸이 공격하는 열과 두 대각선을 비트 마스크로 관리하며 각 행의 가능한 열을 재귀 탐색
