#include <stddef.h>
#include <stdlib.h>

static int larger(int a, int b) {
    return a > b ? a : b;
}

static void add_child(int choices[3][2], int limit, int branch_value, int line_value) {
    for (int branches = limit; branches >= 0; --branches) {
        for (int lines = 1; lines >= 0; --lines) {
            int value = choices[branches][lines];
            if (value < 0) continue;
            if (branches < limit) {
                choices[branches + 1][lines] = larger(choices[branches + 1][lines], value + branch_value);
            }
            if (lines == 0) {
                choices[branches][1] = larger(choices[branches][1], value + line_value);
            }
        }
    }
}

int solution(int** t, size_t t_rows, size_t t_cols) {
    (void)t_cols;
    int n = (int)t_rows + 1;
    size_t storage_size = (size_t)n * 6 + t_rows * 4;
    int* storage = malloc(storage_size * sizeof(*storage));
    int* head = storage;
    int* to = head + n;
    int* next = to + 2 * t_rows;
    int* parent = next + 2 * t_rows;
    int* order = parent + n;
    int* line = order + n;
    int* stem = line + n;
    int* branch = stem + n;
    for (int node = 0; node < n; ++node) {
        head[node] = -1;
        parent[node] = -1;
    }
    for (size_t edge = 0; edge < t_rows; ++edge) {
        int u = t[edge][0], v = t[edge][1];
        to[2 * edge] = v;
        next[2 * edge] = head[u];
        head[u] = (int)(2 * edge);
        to[2 * edge + 1] = u;
        next[2 * edge + 1] = head[v];
        head[v] = (int)(2 * edge + 1);
    }
    int count = 1;
    order[0] = 0;
    parent[0] = 0;
    for (int index = 0; index < count; ++index) {
        int node = order[index];
        for (int edge = head[node]; edge != -1; edge = next[edge]) {
            int child = to[edge];
            if (child == parent[node]) continue;
            parent[child] = node;
            order[count++] = child;
        }
    }
    int answer = 1;
    for (int index = n - 1; index >= 0; --index) {
        int node = order[index];
        int on_spine[3][2], off_spine[3][2];
        for (int branches = 0; branches <= 2; ++branches) {
            for (int lines = 0; lines <= 1; ++lines) {
                on_spine[branches][lines] = -1;
                off_spine[branches][lines] = -1;
            }
        }
        on_spine[0][0] = off_spine[0][0] = 0;
        line[node] = stem[node] = 1;
        int best_branch = 0;
        for (int edge = head[node]; edge != -1; edge = next[edge]) {
            int child = to[edge];
            if (child == parent[node]) continue;
            line[node] = larger(line[node], 1 + line[child]);
            best_branch = larger(best_branch, branch[child]);
            add_child(on_spine, 2, stem[child], line[child]);
            add_child(off_spine, 1, branch[child], line[child]);
        }
        branch[node] = 1 + best_branch;
        for (int branches = 0; branches <= 2; ++branches) {
            for (int lines = 0; lines <= 1; ++lines) {
                int value = on_spine[branches][lines];
                if (value >= 0) {
                    answer = larger(answer, 1 + value);
                    if (branches <= 1) stem[node] = larger(stem[node], 1 + value);
                    if (lines == 0) branch[node] = larger(branch[node], 1 + value);
                }
                if (branches <= 1 && off_spine[branches][lines] >= 0) {
                    answer = larger(answer, 1 + off_spine[branches][lines]);
                }
            }
        }
    }
    free(storage);
    return answer;
}

// 전체 코드 줄별 설명
// #include <stddef.h>  // 2차원 입력 배열의 길이를 받을 size_t
// #include <stdlib.h>  // 선형 크기 작업 배열 할당·해제
//
// static int larger(int a, int b) {  // 두 후보 중 더 많은 정점을 남기는 값 선택
//     return a > b ? a : b;  // 조건 연산자로 큰 정수 반환
// }  // 최댓값 선택 끝
//
// static void add_child(int choices[3][2], int limit, int branch_value, int line_value) {  // 자식을 별도 상태의 가지 또는 단순 경로 중 한 역할로만 배치
//     for (int branches = limit; branches >= 0; --branches) {  // 역순 갱신으로 같은 자식을 두 가지 역할에 중복 사용하지 않기
//         for (int lines = 1; lines >= 0; --lines) {  // 단순 경로도 최대 하나만 고르며 큰 개수부터 갱신
//             int value = choices[branches][lines];  // 이번 자식을 아직 쓰지 않은 기존 조합의 정점 수
//             if (value < 0) continue;  // -1로 표시한 불가능한 조합에서는 새 선택을 만들지 않기
//             if (branches < limit) {  // 허용된 가지 개수에 여유가 있으면 자식 상태값을 추가
//                 choices[branches + 1][lines] = larger(choices[branches + 1][lines], value + branch_value);  // 별도 상태의 가지 하나를 더 쓴 최댓값 갱신
//             }  // 가지 역할로 고르는 경우 처리 끝
//             if (lines == 0) {  // 단순 경로 자식을 아직 고르지 않았으면 이번 자식을 그 역할로 사용
//                 choices[branches][1] = larger(choices[branches][1], value + line_value);  // 아래로 뻗는 한 줄을 더한 최댓값 갱신
//             }  // 단순 경로 역할로 고르는 경우 처리 끝
//         }  // 현재 가지 개수에서의 경로 선택 처리 끝
//     }  // 자식 하나를 배치하는 배낭 갱신 끝
// }  // 자식 조합 갱신 함수 끝
//
// int solution(int** t, size_t t_rows, size_t t_cols) {  // 트리에서 각 정점을 최대 두 번 방문할 수 있는 가장 큰 부분 트리 크기 반환
//     (void)t_cols;  // 열 수는 항상 2라 별도 계산에 쓰지 않음
//     int n = (int)t_rows + 1;  // 트리의 정점 수는 간선 수에 1을 더한 값
//     size_t storage_size = (size_t)n * 6 + t_rows * 4;  // 정점 배열 6개와 방향 간선 배열 2개를 한 번에 확보할 길이
//     int* storage = malloc(storage_size * sizeof(*storage));  // 연속 작업 공간을 잡아 정점 수 200000에서도 작은 할당을 반복하지 않기
//     int* head = storage;  // 각 정점의 첫 인접 간선 번호
//     int* to = head + n;  // 방향 간선마다 도착 정점 저장
//     int* next = to + 2 * t_rows;  // 같은 출발점의 다음 인접 간선 번호
//     int* parent = next + 2 * t_rows;  // 루트 기준 부모 번호
//     int* order = parent + n;  // 부모가 자식보다 먼저 나오는 방문 순서
//     int* line = order + n;  // 현재 정점에서 아래로 뻗는 가장 긴 단순 경로 크기
//     int* stem = line + n;  // 양끝을 잇는 중심 경로가 부모에서 들어오는 상태의 최댓값
//     int* branch = stem + n;  // 부모 간선은 왕복하고 중심 경로는 현재 부분 트리 안에 있는 상태의 최댓값
//     for (int node = 0; node < n; ++node) {  // 각 정점의 인접 목록과 부모 표시 초기화
//         head[node] = -1;  // 아직 연결한 인접 간선이 없다는 표시
//         parent[node] = -1;  // 부모가 아직 정해지지 않았다는 표시
//     }  // 초기화 끝
//     for (size_t edge = 0; edge < t_rows; ++edge) {  // 무방향 입력 간선을 두 방향으로 저장
//         int u = t[edge][0], v = t[edge][1];  // 이번 간선의 양 끝점
//         to[2 * edge] = v;  // u에서 v로 가는 방향 간선
//         next[2 * edge] = head[u];  // 기존 u의 인접 목록 앞에 새 간선을 붙이기
//         head[u] = (int)(2 * edge);  // u의 첫 인접 간선 번호 갱신
//         to[2 * edge + 1] = u;  // 반대쪽 v에서 u로 가는 방향 간선
//         next[2 * edge + 1] = head[v];  // 기존 v의 인접 목록 앞에 반대 방향도 붙이기
//         head[v] = (int)(2 * edge + 1);  // v의 첫 인접 간선 번호 갱신
//     }  // 양방향 인접 목록 완성
//     int count = 1;  // 현재 방문 순서에 들어간 정점 수
//     order[0] = 0;  // 정점 0을 계산용 루트로 선택
//     parent[0] = 0;  // 루트의 부모 표시는 자기 자신으로 두기
//     for (int index = 0; index < count; ++index) {  // 부모부터 자식을 뒤에 붙이는 반복 순회
//         int node = order[index];  // 이번에 자식들을 찾을 정점
//         for (int edge = head[node]; edge != -1; edge = next[edge]) {  // 현재 정점의 인접 간선을 연결 목록으로 순회
//             int child = to[edge];  // 연결된 상대 정점
//             if (child == parent[node]) continue;  // 부모로 되돌아가는 방향은 자식에서 제외
//             parent[child] = node;  // 상대 정점의 부모를 현재 정점으로 기록
//             order[count++] = child;  // 자식은 부모 뒤에서 처리하도록 순서에 추가
//         }  // 현재 정점의 자식 등록 끝
//     }  // 모든 정점의 부모와 방문 순서 결정 끝
//     int answer = 1;  // 한 정점만 남기는 부분 트리부터 시작
//     for (int index = n - 1; index >= 0; --index) {  // 방문 순서를 뒤집어 자식 상태를 먼저 계산
//         int node = order[index];  // 세 가지 DP 상태를 계산할 현재 정점
//         int on_spine[3][2], off_spine[3][2];  // 현재 점이 중심 경로 위·밖일 때 고를 자식 조합
//         for (int branches = 0; branches <= 2; ++branches) {  // 가지 역할 0~2개와 단순 경로 0~1개의 작은 조합표 초기화
//             for (int lines = 0; lines <= 1; ++lines) {  // 단순 경로를 골랐는지 여부에 따른 두 칸
//                 on_spine[branches][lines] = -1;  // 아직 만들지 못한 중심 경로 위 조합
//                 off_spine[branches][lines] = -1;  // 아직 만들지 못한 중심 경로 밖 조합
//             }  // 현재 가지 개수의 두 칸 초기화 끝
//         }  // 조합표 초기화 끝
//         on_spine[0][0] = off_spine[0][0] = 0;  // 자식을 하나도 고르지 않은 조합은 크기 0
//         line[node] = stem[node] = 1;  // 현재 정점 하나만 남기는 경로·중심 경로 상태
//         int best_branch = 0;  // 부모 쪽 왕복 경로를 자식 하나로 그대로 연장할 최댓값
//         for (int edge = head[node]; edge != -1; edge = next[edge]) {  // 이미 계산한 자식 상태들을 하나씩 조합
//             int child = to[edge];  // 이번에 고르거나 건너뛸 자식
//             if (child == parent[node]) continue;  // 부모 쪽 간선은 아래쪽 부분 트리 조합에서 제외
//             line[node] = larger(line[node], 1 + line[child]);  // 단순 경로는 가장 긴 자식 경로 하나만 이어 붙이기
//             best_branch = larger(best_branch, branch[child]);  // 왕복 접근 경로를 아래로 연장할 자식 하나 선택
//             add_child(on_spine, 2, stem[child], line[child]);  // 중심 경로 자식 최대 둘과 옆 단순 경로 하나를 서로 다른 자식에서 선택
//             add_child(off_spine, 1, branch[child], line[child]);  // 중심 경로를 포함한 자식 하나와 반대쪽 단순 경로 하나 선택
//         }  // 현재 정점의 모든 자식 조합 끝
//         branch[node] = 1 + best_branch;  // 현재 점이 중심 경로 밖이면 자식 하나로 왕복 접근 경로 연장
//         for (int branches = 0; branches <= 2; ++branches) {  // 가능한 자식 조합에서 연결 상태별 최댓값 추출
//             for (int lines = 0; lines <= 1; ++lines) {  // 옆 단순 경로가 없는 경우와 있는 경우 모두 확인
//                 int value = on_spine[branches][lines];  // 선택한 중심 경로 자식들과 옆 경로의 정점 수
//                 if (value >= 0) {  // 실제로 만들 수 있는 조합만 사용
//                     answer = larger(answer, 1 + value);  // 현재 점이 중심 경로 위인 완성 부분 트리 후보
//                     if (branches <= 1) stem[node] = larger(stem[node], 1 + value);  // 부모가 중심 경로 한 방향을 쓰면 아래쪽 중심 경로는 최대 하나
//                     if (lines == 0) branch[node] = larger(branch[node], 1 + value);  // 부모가 옆 왕복 가지를 쓰면 자식 둘을 중심 경로로 연결하고 옆 가지는 추가하지 않기
//                 }  // 중심 경로 위 조합 반영 끝
//                 if (branches <= 1 && off_spine[branches][lines] >= 0) {  // 현재 점이 중심 경로 밖일 때는 중심 경로 포함 자식이 최대 하나
//                     answer = larger(answer, 1 + off_spine[branches][lines]);  // 왕복 가지가 현재 점에서 다른 자식 경로로 꺾이는 완성 후보
//                 }  // 중심 경로 밖 조합 반영 끝
//             }  // 옆 경로 포함 여부 두 경우 처리 끝
//         }  // 현재 정점의 DP 계산 끝
//     }  // 모든 부분 트리 후보 계산 끝
//     free(storage);  // 함수가 다시 호출돼도 작업 공간이 남지 않게 해제
//     return answer;  // 방문 제한을 만족하는 최대 부분 트리 크기 반환
// }  // solution 함수 끝

// 풀이 요약
// 선택 정점이 둘 이상이면 시작·끝을 다르게 잡을 수 있음. 그 사이 단순 경로 P의 간선은 한 번, 나머지 간선은 왕복해서 모든 선택 정점 방문.
// 선택 차수를 d라 할 때 P 내부점의 방문 수는 d-1, P 양끝과 P 밖 정점은 d. 따라서 중심 경로 내부는 가지 하나를 옆에 붙일 수 있고, 옆 가지 자체는 갈라지지 않는 단순 경로여야 함.
// line은 아래로 뻗는 한 줄, stem은 부모 간선이 중심 경로인 상태, branch는 부모 간선을 왕복하고 중심 경로는 아래에 있는 상태.
// stem은 자식 stem 하나와 line 하나, branch는 자식 branch 하나 또는 stem 둘. 현재 점이 완성 트리의 맨 위이면 stem 둘+line 하나와 branch 하나+line 하나를 모두 비교.
// 각 조합을 3×2 배낭으로 역순 갱신해 같은 자식의 중복 사용 방지. 방문 순서를 뒤집어 재귀 없이 계산하므로 시간 O(N), 공간 O(N).

