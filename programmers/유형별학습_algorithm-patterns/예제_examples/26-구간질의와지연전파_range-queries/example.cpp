#include <iostream>  // C++ 스트림 입력과 출력

int n, values[16], bit[17], tree[64], lazy[64];  // 두 구조가 공유하는 작은 입력 상한
void bit_add(int index, int delta) {  // Fenwick 한 점 덧셈
    for (++index; index <= n; index += index & -index) bit[index] += delta;  // 해당 점의 상위 블록 갱신
}  // Fenwick 점 갱신 끝
int prefix(int end) {  // [0,end)의 Fenwick 합
    int result = 0;  // 분리한 접두 블록의 합
    for (; end > 0; end -= end & -end) result += bit[end];  // 마지막 블록부터 제거하며 누적
    return result;  // 접두 합 반환
}  // Fenwick 질의 끝
void build(int node, int left, int right) {  // 지연 트리 초기 구축
    if (right - left == 1) { tree[node] = values[left]; return; }  // 한 원소 구간의 합
    int middle = (left + right) / 2;  // 자식 구간의 경계
    build(node * 2, left, middle);  // 왼쪽 합 구축
    build(node * 2 + 1, middle, right);  // 오른쪽 합 구축
    tree[node] = tree[node * 2] + tree[node * 2 + 1];  // 자식 합을 부모에 반영
}  // 초기 구축 끝
void apply(int node, int length, int delta) {  // 한 구간 전체의 덧셈 반영
    tree[node] += length * delta;  // 원소 수만큼 구간 합 증가
    lazy[node] += delta;  // 자손에 보낼 미전달 덧셈 누적
}  // 노드 전체 갱신 끝
void push(int node, int left, int right) {  // 내려가기 전 조상 태그 전달
    if (lazy[node] == 0 || right - left == 1) return;  // 전달할 값이나 자식이 없으면 종료
    int middle = (left + right) / 2;  // 두 자식 길이의 기준
    apply(node * 2, middle - left, lazy[node]);  // 왼쪽 자식의 합과 태그 갱신
    apply(node * 2 + 1, right - middle, lazy[node]);  // 오른쪽 자식의 합과 태그 갱신
    lazy[node] = 0;  // 부모의 전달 의무 해제
}  // 태그 전달 끝
void range_add(int node, int left, int right, int first, int last, int delta) {  // [first,last) 덧셈
    if (last <= left || right <= first) return;  // 겹치지 않는 구간 제외
    if (first <= left && right <= last) { apply(node, right - left, delta); return; }  // 완전히 포함된 구간 처리
    push(node, left, right);  // 일부 자손 갱신 전 기존 태그 전달
    int middle = (left + right) / 2;  // 자식 구간 경계
    range_add(node * 2, left, middle, first, last, delta);  // 왼쪽 교차 부분 갱신
    range_add(node * 2 + 1, middle, right, first, last, delta);  // 오른쪽 교차 부분 갱신
    tree[node] = tree[node * 2] + tree[node * 2 + 1];  // 변경 뒤 부모 합 복구
}  // 구간 덧셈 끝
int range_sum(int node, int left, int right, int first, int last) {  // [first,last)의 지연 트리 합
    if (last <= left || right <= first) return 0;  // 빈 교차의 합
    if (first <= left && right <= last) return tree[node];  // 포함 구간의 요약 사용
    push(node, left, right);  // 읽을 자손에 조상 갱신 반영
    int middle = (left + right) / 2;  // 두 교차 구간의 경계
    return range_sum(node * 2, left, middle, first, last) + range_sum(node * 2 + 1, middle, right, first, last);  // 서로소 부분 합 결합
}  // 구간 합 끝
int main() {  // 두 구현의 결과 비교 시작
    int q;  // 연산 수
    std::cin >> n >> q;  // 입력 크기
    for (int i = 0; i < n; ++i) { std::cin >> values[i]; bit_add(i, values[i]); }  // 초기 값과 Fenwick 구축
    build(1, 0, n);  // 같은 값으로 세그먼트 트리 구축
    for (int i = 0; i < q; ++i) {  // 연산을 입력 순서대로 처리
        int kind, left, right;  // 연산 종류와 반열린 구간
        std::cin >> kind >> left >> right;  // 공통 연산 정보
        if (kind == 0) {  // 구간 덧셈 연산
            int delta;  // 더할 값
            std::cin >> delta;  // 덧셈 크기
            for (int p = left; p < right; ++p) bit_add(p, delta);  // 기본 Fenwick은 각 점 갱신
            if (left < right) range_add(1, 0, n, left, right, delta);  // 지연 트리는 구간으로 갱신
        } else {  // 같은 구간의 두 합 비교
            int first = prefix(right) - prefix(left);  // Fenwick 접두 합의 차이
            int second = range_sum(1, 0, n, left, right);  // 지연 트리의 구간 합
            std::cout << first << " " << second << "\n";  // 일치해야 하는 두 결과
        }  // 연산 분기 끝
    }  // 전체 연산 끝
    return 0;  // 정상 종료
}  // 프로그램 끝
