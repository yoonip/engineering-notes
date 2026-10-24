# 문자열과 알파벳과 쿼리 — C++

[레벨 5 목록](../README.md) · [언어별 목록](../../README.md) · [문제](https://school.programmers.co.kr/learn/courses/30/lessons/389632?language=cpp)

레벨 5 · C++

## 풀이 요약

원래 알파벳과 고유 번호는 바뀌지 않으므로, 알파벳별 위치만 모아 압축한 뒤 구간 트리로 현재 토큰 색을 관리.

토큰 대표에는 현재 문자열 번호와 실제 문자 수를 저장. 문자열마다 알파벳 26개의 토큰 칸을 두고, 생성 번호가 출력 순서가 되도록 유지.

1번은 문자 위치에서 단색 토큰을 찾아 현재 소속 비교. 2번은 쿼리 시작 때 원래 소속을 고정한 뒤 선택 알파벳 토큰의 소속만 이동.

4번은 먼저 생성된 문자열을 남기고 같은 알파벳의 토큰끼리 DSU로 합침. DSU 대표의 높이와 문자열 생성 순서는 별도로 처리.

3번은 원래 번호 범위를 압축 위치 범위로 바꿔 새 토큰으로 색칠. 단색 구간은 문자 개수를 한 번에 옮기고, 혼합 구간만 내려가며 덮인 색을 지움.

색을 자식에 내려보낼 때는 개수를 바꾸지 않고, 실제 색을 교체할 때만 이전 토큰에서 빼고 새 토큰에 더하기. 두 자식의 DSU 대표가 같아지면 부모도 단색으로 합침.

범위 색칠이 새로 만드는 경계는 알파벳당 양끝 두 개뿐이고, 내부 혼합 구간 방문은 지워지는 경계에 나눠 부담시킬 수 있음. 전체는 알파벳 26배의 O((N+Q) log N) 규모, DSU 조회는 경로 압축·순위 병합 사용.

저장 공간은 위치 트리 O(N), 문자열별 알파벳 표와 새 토큰 O(26Q). 필요한 토큰 상한을 쿼리에서 미리 세어 재할당 없이 처리.

마지막에는 생성 번호·알파벳 순으로 실제 개수만 출력하고, 전부 이동해 빈 문자열은 생략. word에 같은 알파벳이 반복돼도 한 번만 이동.

## 코드와 줄별 설명

[제출 코드](solution.cpp) · [사이트 채점 기록](grading.json) · [별도 로컬 검사](local_checks.json)

~~~cpp
#include <string>
#include <vector>
using namespace std;

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    const char* letters;
    int frequency[26], offset[26];
    int* positions; int* occurrence; int* tree[26];
    int* parent; int* owner; int* count; unsigned char* rank;
    int* groups; int token_used; int group_used;
    char** answer; size_t answer_used;
} Context;

static int token_root(Context* ctx, int token) {
    while (ctx->parent[token] != token) {
        ctx->parent[token] = ctx->parent[ctx->parent[token]];
        token = ctx->parent[token];
    }
    return token;
}

static int create_token(Context* ctx, int group, int letter) {
    int token = ++ctx->token_used;
    ctx->parent[token] = token; ctx->rank[token] = 0;
    ctx->owner[token] = group; ctx->count[token] = 0;
    ctx->groups[(size_t)group * 26 + letter] = token;
    return token;
}

static int locate_group(Context* ctx, int position) {
    int letter = ctx->letters[position - 1] - 'a';
    int target = ctx->occurrence[position - 1];
    int node = 1, left = 0, right = ctx->frequency[letter] - 1;
    int* tree = ctx->tree[letter];
    while (tree[node] == -1) {
        int middle = (left + right) / 2;
        if (target <= middle) {
            node *= 2; right = middle;
        } else {
            node = node * 2 + 1; left = middle + 1;
        }
    }
    int root = token_root(ctx, tree[node]);
    return ctx->owner[root];
}

static int lower_position(const int* positions, int length, int value) {
    int left = 0, right = length;
    while (left < right) {
        int middle = left + (right - left) / 2;
        if (positions[middle] < value) left = middle + 1;
        else right = middle;
    }
    return left;
}

static void recolor(Context* ctx, int letter, int node, int left, int right, int begin, int end, int token) {
    int* tree = ctx->tree[letter];
    int old = tree[node];
    if (begin <= left && right <= end && old != -1) {
        old = token_root(ctx, old);
        int amount = right - left + 1;
        ctx->count[old] -= amount;
        if (ctx->count[old] == 0) ctx->groups[(size_t)ctx->owner[old] * 26 + letter] = 0;
        ctx->count[token] += amount;
        tree[node] = token;
        return;
    }
    if (old != -1) {
        tree[node * 2] = tree[node * 2 + 1] = token_root(ctx, old);
    }
    int middle = (left + right) / 2;
    if (begin <= middle) recolor(ctx, letter, node * 2, left, middle, begin, end, token);
    if (end > middle) recolor(ctx, letter, node * 2 + 1, middle + 1, right, begin, end, token);
    int a = tree[node * 2], b = tree[node * 2 + 1];
    if (a != -1) a = token_root(ctx, a);
    if (b != -1) b = token_root(ctx, b);
    tree[node] = a != -1 && a == b ? a : -1;
}

static int read_number(const char** cursor) {
    while (**cursor == ' ') ++*cursor;
    int number = 0;
    while (**cursor >= '0' && **cursor <= '9') {
        number = number * 10 + **cursor - '0';
        ++*cursor;
    }
    return number;
}

static unsigned word_mask(const char* word) {
    unsigned mask = 0;
    while (*word) {
        if (*word >= 'a' && *word <= 'z') mask |= 1u << (*word - 'a');
        ++word;
    }
    return mask;
}

static void append_answer(Context* ctx, const char* text) {
    size_t length = strlen(text) + 1;
    char* copy = (char*)malloc(length);
    memcpy(copy, text, length);
    ctx->answer[ctx->answer_used++] = copy;
}

static char** process_queries(const char* s, const char* const query[], size_t query_len) {
    Context ctx = {0};
    ctx.letters = s;
    int n = (int)strlen(s);
    for (int i = 0; i < n; ++i) ++ctx.frequency[s[i] - 'a'];
    unsigned present = 0; size_t token_capacity = 27, group_capacity = 1;
    for (int letter = 0; letter < 26; ++letter) if (ctx.frequency[letter]) present |= 1u << letter;
    for (size_t q = 0; q < query_len; ++q) {
        if (query[q][0] == '2' || query[q][0] == '3') ++group_capacity;
        if (query[q][0] == '3') {
            unsigned mask = word_mask(strrchr(query[q], ' ') + 1) & present;
            while (mask) { ++token_capacity; mask &= mask - 1; }
        }
    }
    ctx.parent = (int*)malloc(token_capacity * sizeof(int));
    ctx.owner = (int*)malloc(token_capacity * sizeof(int));
    ctx.count = (int*)malloc(token_capacity * sizeof(int));
    ctx.rank = (unsigned char*)malloc(token_capacity);
    ctx.groups = (int*)calloc(group_capacity * 26, sizeof(int));
    ctx.positions = (int*)malloc((size_t)n * sizeof(int));
    ctx.occurrence = (int*)malloc((size_t)n * sizeof(int));
    ctx.answer = (char**)calloc(query_len + (size_t)n + 1, sizeof(char*));
    int cursor[26] = {0}, offset = 0;
    for (int letter = 0; letter < 26; ++letter) {
        ctx.offset[letter] = offset; offset += ctx.frequency[letter];
    }
    for (int i = 0; i < n; ++i) {
        int letter = s[i] - 'a', at = cursor[letter]++;
        ctx.occurrence[i] = at; ctx.positions[ctx.offset[letter] + at] = i + 1;
    }
    ctx.group_used = 1;
    for (int letter = 0; letter < 26; ++letter) {
        int length = ctx.frequency[letter];
        if (!length) continue;
        int token = create_token(&ctx, 0, letter);
        ctx.count[token] = length;
        ctx.tree[letter] = (int*)malloc((size_t)(4 * length + 4) * sizeof(int));
        ctx.tree[letter][1] = token;
    }
    for (size_t q = 0; q < query_len; ++q) {
        const char* command = query[q] + 1; int kind = query[q][0] - '0';
        if (kind == 5) {
            for (int group = 0; group < ctx.group_used; ++group) {
                char text[256]; int used = 0;
                for (int letter = 0; letter < 26; ++letter) {
                    int token = ctx.groups[(size_t)group * 26 + letter];
                    if (!token) continue;
                    int amount = ctx.count[token_root(&ctx, token)];
                    if (!amount) continue;
                    if (used) text[used++] = ' ';
                    used += sprintf(text + used, "%c %d", 'a' + letter, amount);
                }
                if (used) append_answer(&ctx, text);
            }
            continue;
        }
        int x = read_number(&command);
        if (kind == 1 || kind == 4) {
            int y = read_number(&command);
            int a = locate_group(&ctx, x), b = locate_group(&ctx, y);
            if (kind == 1) {
                append_answer(&ctx, a == b ? "YES" : "NO");
                continue;
            }
            if (a == b) continue;
            if (a > b) { int swap = a; a = b; b = swap; }
            for (int letter = 0; letter < 26; ++letter) {
                size_t old_slot = (size_t)b * 26 + letter, new_slot = (size_t)a * 26 + letter;
                int token = ctx.groups[old_slot];
                if (!token) continue;
                token = token_root(&ctx, token);
                int other = ctx.groups[new_slot];
                if (other) {
                    other = token_root(&ctx, other);
                    if (ctx.rank[other] < ctx.rank[token]) { int swap = other; other = token; token = swap; }
                    ctx.parent[token] = other; ctx.count[other] += ctx.count[token];
                    if (ctx.rank[other] == ctx.rank[token]) ++ctx.rank[other];
                    token = other;
                }
                ctx.owner[token] = a;
                ctx.groups[new_slot] = token; ctx.groups[old_slot] = 0;
            }
        } else if (kind == 2) {
            int source = locate_group(&ctx, x), destination = ctx.group_used++;
            unsigned mask = word_mask(command);
            for (int letter = 0; letter < 26; ++letter) if (mask & (1u << letter)) {
                size_t source_slot = (size_t)source * 26 + letter;
                int token = ctx.groups[source_slot];
                if (!token) continue;
                token = token_root(&ctx, token);
                ctx.owner[token] = destination;
                ctx.groups[(size_t)destination * 26 + letter] = token; ctx.groups[source_slot] = 0;
            }
        } else {
            int y = read_number(&command), destination = ctx.group_used++;
            unsigned mask = word_mask(command);
            for (int letter = 0; letter < 26; ++letter) if ((mask & (1u << letter)) && ctx.frequency[letter]) {
                const int* positions = ctx.positions + ctx.offset[letter];
                int length = ctx.frequency[letter];
                int begin = lower_position(positions, length, x), end = lower_position(positions, length, y + 1);
                if (begin == end) continue;
                int token = create_token(&ctx, destination, letter);
                recolor(&ctx, letter, 1, 0, length - 1, begin, end - 1, token);
            }
        }
    }
    for (int letter = 0; letter < 26; ++letter) free(ctx.tree[letter]);
    free(ctx.parent); free(ctx.owner); free(ctx.count); free(ctx.rank);
    free(ctx.groups); free(ctx.positions); free(ctx.occurrence);
    return ctx.answer;
}

vector<string> solution(string s, vector<string> query) {
    vector<const char*> commands(query.size());
    for (size_t q = 0; q < query.size(); ++q) commands[q] = query[q].c_str();
    char** raw = process_queries(s.c_str(), commands.data(), commands.size());
    vector<string> answer;
    for (size_t i = 0; raw[i] != NULL; ++i) {
        answer.emplace_back(raw[i]);
        free(raw[i]);
    }
    free(raw);
    return answer;
}

// 전체 코드 줄별 설명
// #include <string>  // C++ 입력과 결과를 받는 string
// #include <vector>  // C++ 쿼리와 결과를 받는 vector
// using namespace std;  // 표준 string과 vector 이름을 짧게 사용
// 
// #include <stdio.h>  // 알파벳별 개수를 최종 문자열로 만드는 sprintf
// #include <stdlib.h>  // 토큰·구간 트리·반환 문자열의 동적 메모리
// #include <string.h>  // 문자열 길이와 반환 문자열 복사
// 
// typedef struct {  // 한 번의 solution 호출에 필요한 소속·위치·출력 상태
//     const char* letters;  // 고유 번호마다 원래 알파벳은 끝까지 변하지 않음
//     int frequency[26], offset[26];  // 문자별 등장 수와 압축 위치 배열의 시작 칸
//     int* positions; int* occurrence; int* tree[26];  // 알파벳별 원래 번호 목록 / 각 번호의 압축 순번 / 단색 토큰을 저장할 트리
//     int* parent; int* owner; int* count; unsigned char* rank;  // 토큰 DSU 부모 / 현재 문자열 번호 / 살아 있는 문자 수 / 병합 순위
//     int* groups; int token_used; int group_used;  // 문자열별 26개 토큰 표와 지금까지 만든 토큰·문자열 수
//     char** answer; size_t answer_used;  // 동적 결과 문자열 배열과 실제로 채운 개수
// } Context;  // 서로 다른 호출 사이에 상태가 섞이지 않도록 묶은 문맥
// 
// static int token_root(Context* ctx, int token) {  // 트리의 오래된 색 번호를 현재 유효한 토큰 대표로 연결
//     while (ctx->parent[token] != token) {  // 자기 자신을 부모로 둔 대표 토큰까지 이동
//         ctx->parent[token] = ctx->parent[ctx->parent[token]];  // 경로를 조부모로 줄여 반복 조회 비용 절약
//         token = ctx->parent[token];  // 압축한 부모부터 계속 대표 탐색
//     }  // 대표 토큰 탐색 끝
//     return token;  // 현재 소속과 문자 개수를 읽을 대표 번호
// }  // 토큰 대표 조회 끝
// 
// static int create_token(Context* ctx, int group, int letter) {  // 새 문자열의 한 알파벳을 담당할 단독 토큰 생성
//     int token = ++ctx->token_used;  // 0은 문자열에 해당 알파벳이 없다는 표시라 1부터 사용
//     ctx->parent[token] = token; ctx->rank[token] = 0;  // 새 토큰은 혼자만 속한 높이 0의 DSU
//     ctx->owner[token] = group; ctx->count[token] = 0;  // 문자열 소속을 정하고 실제 문자는 색칠하면서 누적
//     ctx->groups[(size_t)group * 26 + letter] = token;  // 새 문자열의 알파벳 칸에 대표 후보 연결
//     return token;  // 구간 트리에 칠할 새 색 번호
// }  // 새 토큰 준비 끝
// 
// static int locate_group(Context* ctx, int position) {  // 원래 문자 번호가 지금 어느 문자열에 있는지 조회
//     int letter = ctx->letters[position - 1] - 'a';  // 고유 번호의 변하지 않는 원래 알파벳
//     int target = ctx->occurrence[position - 1];  // 그 알파벳만 모은 압축 위치에서의 순번
//     int node = 1, left = 0, right = ctx->frequency[letter] - 1;  // 해당 알파벳 트리의 루트 구간에서 시작
//     int* tree = ctx->tree[letter];  // 조회할 알파벳의 구간 색 배열
//     while (tree[node] == -1) {  // 여러 토큰이 섞인 구간이면 목표 위치 쪽으로 내려감
//         int middle = (left + right) / 2;  // 현재 압축 위치 구간의 가운데
//         if (target <= middle) {  // 조회할 문자가 왼쪽 절반에 있는 경우
//             node *= 2; right = middle;  // 왼쪽 자식의 구간으로 범위 축소
//         } else {  // 조회할 문자가 오른쪽 절반에 있는 경우
//             node = node * 2 + 1; left = middle + 1;  // 오른쪽 자식의 구간으로 범위 축소
//         }  // 목표 순번 쪽 자식 선택 끝
//     }  // 단색 구간을 찾으면 그 안의 모든 문자는 같은 토큰 소속
//     int root = token_root(ctx, tree[node]);  // 이후 병합된 토큰까지 반영한 현재 대표
//     return ctx->owner[root];  // 대표가 현재 가리키는 문자열 생성 번호
// }  // 고유 번호의 현재 소속 조회 끝
// 
// static int lower_position(const int* positions, int length, int value) {  // 정렬된 원래 번호 목록에서 value 이상인 첫 위치 찾기
//     int left = 0, right = length;  // 답 후보는 첫 칸부터 배열 끝 다음 칸까지
//     while (left < right) {  // 후보 위치가 하나가 될 때까지 이분 탐색
//         int middle = left + (right - left) / 2;  // 현재 후보 범위의 중간 인덱스
//         if (positions[middle] < value) left = middle + 1;  // value보다 작은 번호는 모두 건너뜀
//         else right = middle;  // value 이상이면 더 앞쪽의 첫 위치 탐색
//     }  // 삽입 위치 결정 끝
//     return left;  // 색칠할 원래 번호 범위의 압축 경계
// }  // 원래 문자 번호의 압축 경계 탐색 끝
// 
// static void recolor(Context* ctx, int letter, int node, int left, int right, int begin, int end, int token) {  // 압축 위치 구간 [begin,end]의 문자를 새 토큰으로 이동
//     int* tree = ctx->tree[letter];  // 이번에 옮기는 알파벳 전용 구간 트리
//     int old = tree[node];  // 양수면 단색 토큰, -1이면 소속이 섞인 구간
//     if (begin <= left && right <= end && old != -1) {  // 구간 전체가 선택됐고 이전 소속도 하나라면 한 번에 이동
//         old = token_root(ctx, old);  // 이전 색이 병합된 대표까지 찾아 개수를 차감
//         int amount = right - left + 1;  // 이번 단색 구간에 포함된 실제 문자 수
//         ctx->count[old] -= amount;  // 기존 문자열의 해당 알파벳 개수에서 이동분 제외
//         if (ctx->count[old] == 0) ctx->groups[(size_t)ctx->owner[old] * 26 + letter] = 0;  // 이 알파벳이 사라진 문자열의 토큰 칸 비우기
//         ctx->count[token] += amount;  // 새 문자열의 해당 알파벳 개수에 이동분 추가
//         tree[node] = token;  // 자식까지 내려가지 않고 구간 전체를 새 단색으로 표시
//         return;  // 통째로 이동한 구간은 더 조사하지 않음
//     }  // 단색 전체 이동을 할 수 있는 경우 처리 끝
//     if (old != -1) {  // 구간 일부만 바꿀 때는 기존 단색을 두 자식에 전달
//         tree[node * 2] = tree[node * 2 + 1] = token_root(ctx, old);  // 색 표현만 내려보내며 문자 개수는 여기서 바꾸지 않음
//     }  // 부분 색칠을 위한 기존 소속 전달 끝
//     int middle = (left + right) / 2;  // 왼쪽·오른쪽 압축 위치를 나누는 경계
//     if (begin <= middle) recolor(ctx, letter, node * 2, left, middle, begin, end, token);  // 선택 범위가 겹치는 왼쪽 자식만 이동
//     if (end > middle) recolor(ctx, letter, node * 2 + 1, middle + 1, right, begin, end, token);  // 선택 범위가 겹치는 오른쪽 자식만 이동
//     int a = tree[node * 2], b = tree[node * 2 + 1];  // 갱신 뒤 두 자식의 단색·혼합 상태 확인
//     if (a != -1) a = token_root(ctx, a);  // 이전 쿼리에서 병합된 왼쪽 토큰을 현재 대표로 정규화
//     if (b != -1) b = token_root(ctx, b);  // 이전 쿼리에서 병합된 오른쪽 토큰도 현재 대표로 정규화
//     tree[node] = a != -1 && a == b ? a : -1;  // 대표까지 같아졌으면 부모를 단색으로 합쳐 다음 이동을 단축
// }  // 선택 범위 색칠과 단색 구간 합치기 끝
// 
// static int read_number(const char** cursor) {  // 쿼리 문자열에서 다음 고유 번호를 읽고 커서 이동
//     while (**cursor == ' ') ++*cursor;  // 숫자 앞의 구분 공백 건너뛰기
//     int number = 0;  // 읽은 십진수의 누적값
//     while (**cursor >= '0' && **cursor <= '9') {  // 연속된 숫자 부분만 읽기
//         number = number * 10 + **cursor - '0';  // 기존 자릿수를 왼쪽으로 밀고 새 숫자 추가
//         ++*cursor;  // 방금 읽은 숫자 다음 문자로 이동
//     }  // 숫자가 끝나는 공백이나 문자열 끝에서 정지
//     return number;  // 쿼리에 적힌 원래 문자 번호
// }  // 쿼리 정수 읽기 끝
// 
// static unsigned word_mask(const char* word) {  // 중복 알파벳을 한 번만 처리할 26비트 집합 생성
//     unsigned mask = 0;  // 아직 선택된 알파벳 없음
//     while (*word) {  // 쿼리 뒤쪽에 남은 word와 구분 공백을 끝까지 확인
//         if (*word >= 'a' && *word <= 'z') mask |= 1u << (*word - 'a');  // 소문자가 있으면 대응 비트만 켜서 중복 제거
//         ++word;  // 다음 알파벳으로 이동
//     }  // word 읽기 끝
//     return mask;  // 선택 알파벳 집합
// }  // 쿼리 알파벳 중복 제거 끝
// 
// static void append_answer(Context* ctx, const char* text) {  // 반환 후에도 남아 있을 결과 문자열을 따로 복사
//     size_t length = strlen(text) + 1;  // 마지막 널 문자까지 포함한 저장 길이
//     char* copy = (char*)malloc(length);  // 이번 결과 한 줄의 독립 메모리
//     memcpy(copy, text, length);  // YES/NO 또는 알파벳 구성을 널 문자까지 복사
//     ctx->answer[ctx->answer_used++] = copy;  // 결과 순서대로 포인터를 추가
// }  // 결과 문자열 추가 끝
// 
// static char** process_queries(const char* s, const char* const query[], size_t query_len) {  // C와 C++에서 공통으로 쓰는 토큰·색칠 트리 처리부
//     Context ctx = {0};  // 현재 호출의 포인터와 개수를 0부터 준비
//     ctx.letters = s;  // 고유 번호의 원래 알파벳 조회에 입력 문자열 재사용
//     int n = (int)strlen(s);  // 전체 문자의 수; 고유 번호는 1부터 n
//     for (int i = 0; i < n; ++i) ++ctx.frequency[s[i] - 'a'];  // 문자별 압축 위치 목록 크기 계산
//     unsigned present = 0; size_t token_capacity = 27, group_capacity = 1;  // 등장 알파벳 집합과 초기 토큰·문자열 저장 공간의 상한
//     for (int letter = 0; letter < 26; ++letter) if (ctx.frequency[letter]) present |= 1u << letter;  // 초기 문자열에 없는 알파벳은 새 토큰도 필요 없음
//     for (size_t q = 0; q < query_len; ++q) {  // 재할당 없이 처리할 수 있도록 쿼리별 필요한 공간을 먼저 계산
//         if (query[q][0] == '2' || query[q][0] == '3') ++group_capacity;  // 2·3번은 이동할 문자가 없어도 문자열 생성 번호를 하나 소비
//         if (query[q][0] == '3') {  // 새 색이 필요한 경우는 구간을 떼는 3번뿐
//             unsigned mask = word_mask(strrchr(query[q], ' ') + 1) & present;  // 마지막 word에서 실제 존재하는 알파벳만 선택
//             while (mask) { ++token_capacity; mask &= mask - 1; }  // 선택 알파벳 하나마다 토큰 한 개를 더 쓸 수 있음
//         }  // 3번 쿼리의 새 토큰 상한 계산 끝
//     }  // 저장 공간 상한 조사 끝
//     ctx.parent = (int*)malloc(token_capacity * sizeof(int));  // 토큰 대표 연결을 위한 부모 배열
//     ctx.owner = (int*)malloc(token_capacity * sizeof(int));  // 토큰 대표가 가리키는 현재 문자열 번호
//     ctx.count = (int*)malloc(token_capacity * sizeof(int));  // 각 대표 토큰에 남은 실제 문자 수
//     ctx.rank = (unsigned char*)malloc(token_capacity);  // DSU 병합 순위는 작은 정수라 1바이트씩 저장
//     ctx.groups = (int*)calloc(group_capacity * 26, sizeof(int));  // 문자열별 알파벳 토큰 표; 0이면 해당 알파벳 없음
//     ctx.positions = (int*)malloc((size_t)n * sizeof(int));  // 모든 알파벳의 원래 번호 목록을 한 배열에 연속 배치
//     ctx.occurrence = (int*)malloc((size_t)n * sizeof(int));  // 고유 번호에서 그 알파벳의 압축 순번으로 바로 이동
//     ctx.answer = (char**)calloc(query_len + (size_t)n + 1, sizeof(char*));  // 1번 응답과 최종 문자열을 모두 담고 뒤에는 NULL 유지
//     int cursor[26] = {0}, offset = 0;  // 알파벳별 다음 저장 순번과 위치 배열의 구간 시작
//     for (int letter = 0; letter < 26; ++letter) {  // 알파벳별 압축 위치 배열의 시작 칸 확정
//         ctx.offset[letter] = offset; offset += ctx.frequency[letter];  // 이 알파벳 개수만큼 다음 알파벳의 시작 위치 이동
//     }  // 압축 위치 배열 배치 끝
//     for (int i = 0; i < n; ++i) {  // 원래 번호 순서대로 압축 위치와 역방향 순번 채우기
//         int letter = s[i] - 'a', at = cursor[letter]++;  // 현재 알파벳의 다음 압축 순번 사용
//         ctx.occurrence[i] = at; ctx.positions[ctx.offset[letter] + at] = i + 1;  // 두 방향의 위치 조회를 함께 기록
//     }  // 원래 번호와 알파벳별 압축 순번 연결 끝
//     ctx.group_used = 1;  // 초기 문자열의 생성 번호는 0
//     for (int letter = 0; letter < 26; ++letter) {  // 처음 등장한 알파벳마다 단색 토큰 하나씩 생성
//         int length = ctx.frequency[letter];  // 이 알파벳에 속한 전체 문자 수
//         if (!length) continue;  // 원래 문자열에 없는 알파벳의 트리는 만들지 않음
//         int token = create_token(&ctx, 0, letter);  // 초기 문자열이 이 알파벳 전체를 소유
//         ctx.count[token] = length;  // 단색 토큰의 실제 문자 수 초기화
//         ctx.tree[letter] = (int*)malloc((size_t)(4 * length + 4) * sizeof(int));  // 압축 위치만 대상으로 하는 구간 트리 확보
//         ctx.tree[letter][1] = token;  // 전체가 단색이므로 루트만 초기화; 자식은 내려갈 때 채움
//     }  // 초기 소속 트리 준비 끝
//     for (size_t q = 0; q < query_len; ++q) {  // 주어진 순서대로 쿼리 실행
//         const char* command = query[q] + 1; int kind = query[q][0] - '0';  // 쿼리 종류를 읽고 나머지 매개변수 앞으로 커서 이동
//         if (kind == 5) {  // 마지막 쿼리에서만 모든 문자열의 알파벳 구성 출력
//             for (int group = 0; group < ctx.group_used; ++group) {  // 문자열을 생성 번호 오름차순으로 확인
//                 char text[256]; int used = 0;  // 26개 알파벳과 최대 6자리 개수를 담을 출력 버퍼
//                 for (int letter = 0; letter < 26; ++letter) {  // 알파벳도 a부터 z 순서로 출력
//                     int token = ctx.groups[(size_t)group * 26 + letter];  // 이 문자열에 해당 알파벳이 있는지 조회
//                     if (!token) continue;  // 없는 알파벳은 결과에서 생략
//                     int amount = ctx.count[token_root(&ctx, token)];  // 병합 후 대표에 남은 실제 개수 확인
//                     if (!amount) continue;  // 모두 이동해 사라진 알파벳은 출력하지 않음
//                     if (used) text[used++] = ' ';  // 첫 항목이 아니면 앞 항목과 공백 하나로 구분
//                     used += sprintf(text + used, "%c %d", 'a' + letter, amount);  // 알파벳과 개수를 이어 붙이고 쓴 길이 누적
//                 }  // 이 문자열의 알파벳 구성 작성 끝
//                 if (used) append_answer(&ctx, text);  // 알파벳이 하나도 없어진 빈 문자열은 생략
//             }  // 최종 문자열 구성 출력 끝
//             continue;  // 5번에는 고유 번호 매개변수가 없음
//         }  // 최종 출력 쿼리 처리 끝
//         int x = read_number(&command);  // 1~4번 쿼리의 첫 고유 번호
//         if (kind == 1 || kind == 4) {  // 두 문자의 소속 비교 또는 문자열 병합
//             int y = read_number(&command);  // 두 번째 고유 번호
//             int a = locate_group(&ctx, x), b = locate_group(&ctx, y);  // 쿼리 시작 시점의 두 문자열 소속 확정
//             if (kind == 1) {  // 현재 같은 문자열인지 묻는 쿼리
//                 append_answer(&ctx, a == b ? "YES" : "NO");  // 소속 번호 비교 결과를 입력 순서대로 저장
//                 continue;  // 조회만 했으므로 소속 상태는 그대로
//             }  // 1번 쿼리 처리 끝
//             if (a == b) continue;  // 이미 같은 문자열이면 병합 작업 불필요
//             if (a > b) { int swap = a; a = b; b = swap; }  // 생성 번호가 작은 문자열을 반드시 남김
//             for (int letter = 0; letter < 26; ++letter) {  // 늦게 생성된 문자열의 알파벳별 토큰을 하나씩 병합
//                 size_t old_slot = (size_t)b * 26 + letter, new_slot = (size_t)a * 26 + letter;  // 사라질 문자열과 남길 문자열의 알파벳 칸
//                 int token = ctx.groups[old_slot];  // 늦게 생성된 문자열이 가진 알파벳 토큰
//                 if (!token) continue;  // 이 알파벳이 없으면 옮길 내용도 없음
//                 token = token_root(&ctx, token);  // 오래된 토큰 번호를 현재 대표로 정규화
//                 int other = ctx.groups[new_slot];  // 먼저 생성된 문자열에도 같은 알파벳이 있는지 확인
//                 if (other) {  // 양쪽 모두 이 알파벳이 있으면 색 번호를 DSU로 합침
//                     other = token_root(&ctx, other);  // 남길 문자열 쪽의 현재 대표
//                     if (ctx.rank[other] < ctx.rank[token]) { int swap = other; other = token; token = swap; }  // 문자열 생성 순서와 별개로 DSU의 낮은 트리를 높은 트리 아래에 붙임
//                     ctx.parent[token] = other; ctx.count[other] += ctx.count[token];  // 대표 연결 후 살아 있는 문자 수를 한 대표로 합산
//                     if (ctx.rank[other] == ctx.rank[token]) ++ctx.rank[other];  // 같은 높이를 합친 경우에만 대표 트리 높이 증가
//                     token = other;  // 병합 후 유효한 알파벳 대표로 맞춤
//                 }  // 같은 알파벳의 DSU 병합 끝
//                 ctx.owner[token] = a;  // DSU 대표가 어느 쪽이든 문자열은 먼저 생성된 번호로 통일
//                 ctx.groups[new_slot] = token; ctx.groups[old_slot] = 0;  // 남길 문자열에 대표를 연결하고 늦은 문자열 칸은 비움
//             }  // 두 문자열의 알파벳 병합 끝
//         } else if (kind == 2) {  // 한 문자열에서 선택 알파벳 전체를 새 문자열로 이동
//             int source = locate_group(&ctx, x), destination = ctx.group_used++;  // x 자체가 이동하더라도 이후 알파벳은 원래 소속에서 계속 가져오기
//             unsigned mask = word_mask(command);  // word 중복 알파벳을 제거한 선택 비트 집합
//             for (int letter = 0; letter < 26; ++letter) if (mask & (1u << letter)) {  // 선택된 알파벳만 한 번씩 처리
//                 size_t source_slot = (size_t)source * 26 + letter;  // 쿼리 시작 때 확정한 원래 문자열의 알파벳 칸
//                 int token = ctx.groups[source_slot];  // 이 문자열이 해당 알파벳을 가지고 있는지 확인
//                 if (!token) continue;  // 없는 알파벳은 새 문자열에도 추가하지 않음
//                 token = token_root(&ctx, token);  // 이동할 알파벳의 현재 대표
//                 ctx.owner[token] = destination;  // 알파벳 전체 이동은 대표의 소속만 바꾸면 됨
//                 ctx.groups[(size_t)destination * 26 + letter] = token; ctx.groups[source_slot] = 0;  // 새 문자열에 토큰을 옮겨 연결하고 원래 칸 비우기
//             }  // 알파벳 전체 이동 끝; 위치 트리는 손대지 않음
//         } else {  // 3번: 여러 문자열에 흩어진 번호 구간의 선택 알파벳을 모으기
//             int y = read_number(&command), destination = ctx.group_used++;  // 범위 끝 번호를 읽고 새 문자열 생성 순서 부여
//             unsigned mask = word_mask(command);  // 중복을 제거한 선택 알파벳 집합
//             for (int letter = 0; letter < 26; ++letter) if ((mask & (1u << letter)) && ctx.frequency[letter]) {  // 선택됐고 원래 존재하는 알파벳만 구간 조회
//                 const int* positions = ctx.positions + ctx.offset[letter];  // 이 알파벳의 고유 번호를 오름차순으로 모은 목록
//                 int length = ctx.frequency[letter];  // 해당 압축 위치 목록의 길이
//                 int begin = lower_position(positions, length, x), end = lower_position(positions, length, y + 1);  // 원래 번호 [x,y]를 압축 위치 [begin,end)로 변환
//                 if (begin == end) continue;  // 번호 구간에 이 알파벳이 없으면 새 토큰도 만들지 않음
//                 int token = create_token(&ctx, destination, letter);  // 모아 올 문자를 담을 새 문자열의 알파벳 대표
//                 recolor(&ctx, letter, 1, 0, length - 1, begin, end - 1, token);  // 선택된 압축 위치의 기존 개수를 차감하며 새 대표로 색칠
//             }  // 범위에서 알파벳 모으기 끝
//         }  // 현재 쿼리 처리 끝
//     }  // 모든 쿼리 실행 끝
//     for (int letter = 0; letter < 26; ++letter) free(ctx.tree[letter]);  // 알파벳별 위치 트리 메모리 해제; 없는 알파벳의 NULL도 안전
//     free(ctx.parent); free(ctx.owner); free(ctx.count); free(ctx.rank);  // 소속을 추적하던 토큰 배열 해제
//     free(ctx.groups); free(ctx.positions); free(ctx.occurrence);  // 문자열 토큰 표와 압축 위치 배열 해제
//     return ctx.answer;  // 결과 문자열과 포인터 배열만 호출자에게 넘김
// }  // 토큰·색칠 트리 처리 끝
// 
// vector<string> solution(string s, vector<string> query) {  // 프로그래머스 C++ 템플릿에서 문자열 배열을 받아 처리
//     vector<const char*> commands(query.size());  // 입력 문자열을 복사하지 않고 공통 처리부에 넘길 포인터 배열
//     for (size_t q = 0; q < query.size(); ++q) commands[q] = query[q].c_str();  // 쿼리 vector가 유지되는 동안 유효한 각 문자열 주소 연결
//     char** raw = process_queries(s.c_str(), commands.data(), commands.size());  // 동일한 토큰·색칠 트리로 쿼리 실행
//     vector<string> answer;  // C++ 반환 형식의 문자열 결과 배열
//     for (size_t i = 0; raw[i] != NULL; ++i) {  // 널 포인터로 끝나는 공통 처리 결과를 순서대로 변환
//         answer.emplace_back(raw[i]);  // 결과 한 줄을 C++ string으로 복사
//         free(raw[i]);  // 복사한 C 문자열의 독립 메모리는 즉시 해제
//     }  // 결과 문자열 변환 끝
//     free(raw);  // 공통 처리부의 결과 포인터 배열 해제
//     return answer;  // 조회 응답과 최종 구성을 담은 C++ 문자열 배열 반환
// }  // C++ 풀이 함수 끝

// 풀이 요약
// 원래 알파벳과 고유 번호는 바뀌지 않으므로, 알파벳별 위치만 모아 압축한 뒤 구간 트리로 현재 토큰 색을 관리.
// 토큰 대표에는 현재 문자열 번호와 실제 문자 수를 저장. 문자열마다 알파벳 26개의 토큰 칸을 두고, 생성 번호가 출력 순서가 되도록 유지.
// 1번은 문자 위치에서 단색 토큰을 찾아 현재 소속 비교. 2번은 쿼리 시작 때 원래 소속을 고정한 뒤 선택 알파벳 토큰의 소속만 이동.
// 4번은 먼저 생성된 문자열을 남기고 같은 알파벳의 토큰끼리 DSU로 합침. DSU 대표의 높이와 문자열 생성 순서는 별도로 처리.
// 3번은 원래 번호 범위를 압축 위치 범위로 바꿔 새 토큰으로 색칠. 단색 구간은 문자 개수를 한 번에 옮기고, 혼합 구간만 내려가며 덮인 색을 지움.
// 색을 자식에 내려보낼 때는 개수를 바꾸지 않고, 실제 색을 교체할 때만 이전 토큰에서 빼고 새 토큰에 더하기. 두 자식의 DSU 대표가 같아지면 부모도 단색으로 합침.
// 범위 색칠이 새로 만드는 경계는 알파벳당 양끝 두 개뿐이고, 내부 혼합 구간 방문은 지워지는 경계에 나눠 부담시킬 수 있음. 전체는 알파벳 26배의 O((N+Q) log N) 규모, DSU 조회는 경로 압축·순위 병합 사용.
// 저장 공간은 위치 트리 O(N), 문자열별 알파벳 표와 새 토큰 O(26Q). 필요한 토큰 상한을 쿼리에서 미리 세어 재할당 없이 처리.
// 마지막에는 생성 번호·알파벳 순으로 실제 개수만 출력하고, 전부 이동해 빈 문자열은 생략. word에 같은 알파벳이 반복돼도 한 번만 이동.
~~~

## 채점 기록

2026-10-24 사이트 채점: 정답 100/100. 1번째 제출에서 통과. C++ 제출 내역에서도 같은 날짜의 정답 기록 확인.

줄별 설명과 풀이 요약을 포함한 코드를 제출. 로컬 검사 횟수와 실행 시간은 사이트 채점 기록과 별도로 보관.
