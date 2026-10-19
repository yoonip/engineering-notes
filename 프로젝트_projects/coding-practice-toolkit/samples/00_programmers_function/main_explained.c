/* PDF의 함수 예제를 PC에서 실행하기 위해 main을 덧붙인 연습입니다.
   입력: N과 N개 정수. 함수는 합을 반환하고 main이 그 값을 출력합니다.
   실제 프로그래머스에는 문제의 템플릿에 맞는 함수 부분만 제출합니다. */
#include <stdio.h>
int a[100000];  // 제약 N<=100000에 맞는 고정 저장 공간. 다른 문제의 제한을 그대로 대입하지 마세요.
// C 배열 인자는 배열 길이를 자동으로 전달하지 않습니다. 그래서 n도 함께 받습니다.
// const는 이 함수가 배열 원소를 수정하지 않음을 나타냅니다.
long long solution(const int a[], int n) {
    long long ans = 0;  // 아직 아무 값도 처리하지 않은 상태의 합.
    for (int i = 0; i < n; ++i) ans += a[i];  // 0~n-1 원소를 한 번씩 더합니다.
    return ans;  // 출력하지 않고 호출한 곳으로 계산 결과를 돌려줍니다.
}
// main은 실행 진입점입니다. 입력 준비 → 함수 호출 → 반환값 출력 순서입니다.
int main(void) {
    int n;
    if (scanf("%d", &n) != 1) return 0;  // 빈 입력에서 미초기화 n 사용을 피합니다.
    if (n < 0 || n > 100000) return 1;  // ||는 둘 중 하나라도 참인 조건입니다.
    for (int i = 0; i < n; ++i) scanf("%d", &a[i]);  // &는 해당 원소의 주소입니다.
    printf("%lld\n", solution(a, n));  // long long 반환값이므로 출력 형식도 %lld.
    return 0;
}
// 함수 계산 O(N), 입력 배열 O(N). 유효한 N개 정수 입력을 전제로 합니다.
