// 자체 창작 연습 10 · 목표 합의 부분집합 
// 핵심 상태: dfs(i,total,used)는 i번째부터 결정할 차례. total은 선택 합, used는 하나 이상 선택 여부다.
// C11: main이 실행 시작점이다. stdio.h의 scanf/printf로 표준입출력을 사용한다.
// scanf의 %d는 int, %lld는 long long이다. 정수 변수 앞 &는 저장할 주소를 전달한다.
// 문자열 배열 이름은 첫 원소의 주소로 전달된다. 문자열에는 끝의 널 문자 공간이 필요하다.

#include <stdio.h>
int n;
long long a[20], target, answer = 0;
// 함수는 다음에 결정할 위치 i, 지금까지의 합 total, 비어 있지 않음 used를 인자로 받는다.
// 이 값들은 호출마다 별도 복사된다. 부모 호출의 total을 직접 바꾸지 않아 되돌리기 코드가 필요 없다.
// n,target,a,answer는 전역 상태이며 모든 재귀 호출에서 같은 문제와 답 카운터를 공유한다.
void dfs(int i, long long total, int used) {
    // 모든 원소에 대한 선택이 끝난 재귀 종료 조건이다.
    // used가 참이고 total==target일 때만 정답 개수를 한 번 늘린다.
    // return으로 끝내야 a[n] 같은 배열 범위 밖 원소를 읽지 않는다.
    if (i == n) {
        if (used && total == target) ++answer;  // 목표 합의 비어 있지 않은 선택만 센다.
        return;
    }
    // 현재 원소를 고른 가지는 합에 a[i]를 더하고 used=1로 다음 위치에 간다.
    // 그다음 고르지 않은 가지는 합과 used를 그대로 전달한다.
    // 음수가 가능하므로 total>target이라는 이유만으로 탐색을 중단하면 안 된다.
    dfs(i + 1, total + a[i], 1);
    dfs(i + 1, total, used);
}
int main(void) {
    scanf("%d %lld", &n, &target);
    for (int i = 0; i < n; ++i) scanf("%lld", &a[i]);
    dfs(0, 0, 0);
    printf("%lld\n", answer);
    return 0;
}

// 복잡도: 시간 O(2^N), 재귀 깊이 및 배열 공간 O(N). 재귀 깊이가 20이므로 이 예제는 Python 재귀 한도 변경이 필요 없다.
// 마지막 경계 확인:
// - T=0에서 빈 집합을 세지 않는다.
// - 같은 값을 가진 서로 다른 위치를 임의로 합치지 않는다.
// - 연속 구간 개수와 부분집합 개수를 구분한다.
// - 합은 C/C++ long long으로 받는다.
