# 네오의 귀걸이 — C++

[레벨 5 목록](../README.md) · [언어별 목록](../../README.md) · [문제](https://school.programmers.co.kr/learn/courses/30/lessons/1842?language=cpp)

레벨 5 · C++

## 풀이 요약

이전 점 p에서 다음 점 v로 직사각형을 만들려면 xp<xv, yp>yv이고 (xv−xp)+(yp−yv)=kv. t=x−y로 두면 tp=tv−kv인 키 조건으로 정리.

f[v]는 S→v, g[v]는 v→E 경로 수. x가 항상 커지므로 DAG이며, 삭제점 v를 지나는 경로는 f[v]g[v]개라 초기 수에서 이 곱만 빼기.

추가점도 초기점 사이에 한 번만 들어갈 수 있어 새 경로는 f_new×g_new개. 각 변화는 초기 상태에 독립적으로 적용하므로 추가점을 DP 트리에 넣지 않음.

f는 x 오름차순으로 계산. 키 tv−kv인 이전 점에서 xv−kv<xp<xv인 f값을 키별 압축 Fenwick으로 합산하면 위쪽 조건까지 만족.

g는 x 내림차순으로 계산. 후속점의 키 t−k별 y Fenwick에 g를 넣고, 현재 t와 같은 키에서 y가 엄격히 작은 후속점만 합산.

추가점의 g 조회도 같은 내림차순 스위프에 끼워 넣어 오른쪽 초기점만 활성화. f_new는 완성된 초기 f 트리에서 열린 x구간 합으로 조회.

S와 E는 최초 위치로 고정. 둘 중 하나를 삭제하면0, 그 열린 직사각형 밖에 추가한 점은 초기 경로 수 그대로.

키·좌표 경계는 long long으로 계산하고 경로 수는1,000,000,007로 나눈 나머지 유지. 시간 O((N+Q) log N), 공간 O(N+Q).

## 코드와 줄별 설명

[제출 코드](solution.cpp) · [사이트 채점 기록](grading.json) · [별도 로컬 검사](local_checks.json)

~~~cpp
#include <algorithm>
#include <utility>
#include <vector>
using namespace std;

static const int MOD = 1000000007;
using int64 = long long;

struct GroupFenwick {
    vector<int64> keys, coordinate;
    vector<int> offset, length, bit;
    explicit GroupFenwick(vector<pair<int64,int64>> entries) {
        sort(entries.begin(), entries.end());
        for (const auto& entry : entries) {
            if (keys.empty() || keys.back() != entry.first) {
                keys.push_back(entry.first);
                offset.push_back((int)coordinate.size()); length.push_back(0);
            }
            if (!length.back() || coordinate.back() != entry.second) {
                coordinate.push_back(entry.second); ++length.back();
            }
        }
        bit.assign(coordinate.size(), 0);
    }
    int group_id(int64 key) const {
        auto at = lower_bound(keys.begin(), keys.end(), key);
        return at == keys.end() || *at != key ? -1 : (int)(at - keys.begin());
    }
    int prefix(int group, int count) const {
        int result = 0, base = offset[group];
        while (count > 0) {
            result += bit[base + count - 1];
            if (result >= MOD) result -= MOD;
            count &= count - 1;
        }
        return result;
    }
    void add(int group, int64 value, int weight) {
        if (!weight) return;
        int base = offset[group], size = length[group];
        auto first = coordinate.begin() + base;
        int at = (int)(lower_bound(first, first + size, value) - first);
        while (at < size) {
            int& stored = bit[base + at];
            stored += weight; if (stored >= MOD) stored -= MOD;
            at |= at + 1;
        }
    }
    int open_sum(int64 key, int64 low, int64 high) const {
        int group = group_id(key);
        if (group < 0 || low >= high) return 0;
        auto first = coordinate.begin() + offset[group];
        auto last = first + length[group];
        int left = (int)(upper_bound(first, last, low) - first);
        int right = (int)(lower_bound(first, last, high) - first);
        int result = prefix(group, right) - prefix(group, left);
        return result < 0 ? result + MOD : result;
    }
    int less_sum(int64 key, int64 bound) const {
        int group = group_id(key);
        if (group < 0) return 0;
        auto first = coordinate.begin() + offset[group];
        int count = (int)(lower_bound(first, first + length[group], bound) - first);
        return prefix(group, count);
    }
};

struct Point {
    int64 x, y, k, diagonal, predecessor;
    int forward_group, backward_group;
};
struct Addition {
    int64 x, y, diagonal;
    int index, from_start; bool inside;
};

vector<int> solution(int n, vector<vector<int>> point, vector<vector<int>> query) {
    vector<Point> points; points.reserve(n);
    vector<pair<int64,int64>> forward_entries, backward_entries;
    forward_entries.reserve(n); backward_entries.reserve(n);
    for (const auto& item : point) {
        Point p{}; p.x = item[0]; p.y = item[1]; p.k = item[2];
        p.diagonal = p.x - p.y; p.predecessor = p.diagonal - p.k;
        forward_entries.emplace_back(p.diagonal, p.x);
        backward_entries.emplace_back(p.predecessor, p.y);
        points.push_back(p);
    }
    sort(points.begin(), points.end(), [](const Point& a, const Point& b) { return a.x < b.x; });
    GroupFenwick forward(move(forward_entries)), backward(move(backward_entries));
    for (auto& p : points) {
        p.forward_group = forward.group_id(p.diagonal);
        p.backward_group = backward.group_id(p.predecessor);
    }
    vector<int> from_start(n, 0), to_end(n, 0);
    for (int i = 0; i < n; ++i) {
        const Point& p = points[i];
        from_start[i] = i == 0 ? 1 : forward.open_sum(p.predecessor, p.x - p.k, p.x);
        forward.add(p.forward_group, p.x, from_start[i]);
    }
    int base = from_start[n - 1];
    vector<int> answer(query.size() + 1, base);
    vector<Addition> additions; additions.reserve(query.size());
    for (size_t q = 0; q < query.size(); ++q) if (query[q][0] == 0) {
        int64 x = query[q][1], y = query[q][2], k = query[q][3];
        int64 diagonal = x - y, predecessor = diagonal - k;
        bool inside = points[0].x < x && x < points[n - 1].x && points[n - 1].y < y && y < points[0].y;
        int paths = inside ? forward.open_sum(predecessor, x - k, x) : 0;
        additions.push_back({x, y, diagonal, (int)q, paths, inside});
    }
    sort(additions.begin(), additions.end(), [](const Addition& a, const Addition& b) { return a.x > b.x; });
    int next = n - 1;
    auto insert_initial = [&](int index) {
        const Point& p = points[index];
        to_end[index] = index == n - 1 ? 1 : backward.less_sum(p.diagonal, p.y);
        backward.add(p.backward_group, p.y, to_end[index]);
    };
    for (const auto& added : additions) {
        while (next >= 0 && points[next].x > added.x) insert_initial(next--);
        if (!added.inside) continue;
        int paths = backward.less_sum(added.diagonal, added.y);
        answer[added.index + 1] = (base + (int64)added.from_start * paths) % MOD;
    }
    while (next >= 0) insert_initial(next--);
    for (size_t q = 0; q < query.size(); ++q) if (query[q][0] == 1) {
        int64 x = query[q][1];
        auto at = lower_bound(points.begin(), points.end(), x, [](const Point& p, int64 value) { return p.x < value; });
        int index = (int)(at - points.begin());
        if (index == 0 || index == n - 1) {
            answer[q + 1] = 0;
        } else {
            int removed = (int)((int64)from_start[index] * to_end[index] % MOD);
            answer[q + 1] = base - removed;
            if (answer[q + 1] < 0) answer[q + 1] += MOD;
        }
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 점과 추가 쿼리 정렬, 그룹·좌표 이분 탐색
// #include <utility>  // 키·좌표 쌍과 큰 임시 배열의 move
// #include <vector>  // 점·경로 수·압축 Fenwick 배열
// using namespace std;  // 표준 vector와 정렬 함수 이름을 짧게 사용
// 
// static const int MOD = 1000000007;  // 문제에서 요구하는 경로 수의 나머지
// using int64 = long long;  // x−y와 x−y−k는 int 범위를 벗어날 수 있어 64비트 사용
// 
// struct GroupFenwick {  // 서로 다른 64비트 키마다 독립적인 좌표 합을 관리
//     vector<int64> keys, coordinate;  // 정렬된 키와 키별로 이어 붙인 압축 좌표
//     vector<int> offset, length, bit;  // 그룹 시작 칸 / 그룹 크기 / 같은 배치의 0기반 Fenwick
//     explicit GroupFenwick(vector<pair<int64,int64>> entries) {  // 초기점에서 실제로 쓰는 키·좌표만 모아 트리 구성
//         sort(entries.begin(), entries.end());  // 키가 같으면 좌표순이 되도록 정렬
//         for (const auto& entry : entries) {  // 정렬된 키·좌표를 한 번씩 확인
//             if (keys.empty() || keys.back() != entry.first) {  // 새 키를 만나면 독립된 그룹 구간 시작
//                 keys.push_back(entry.first);  // 이분 탐색할 새 키 등록
//                 offset.push_back((int)coordinate.size()); length.push_back(0);  // 이 그룹의 좌표 시작 위치와 길이 초기화
//             }  // 그룹 경계 준비 끝
//             if (!length.back() || coordinate.back() != entry.second) {  // 같은 그룹의 좌표가 중복되면 한 칸만 사용
//                 coordinate.push_back(entry.second); ++length.back();  // 좌표를 추가하고 현재 그룹 크기 증가
//             }  // 압축 좌표 등록 끝
//         }  // 모든 키별 좌표 배치 끝
//         bit.assign(coordinate.size(), 0);  // 아직 처리한 점이 없으므로 모든 경로 합을 0으로 시작
//     }  // 그룹별 Fenwick 생성 끝
//     int group_id(int64 key) const {  // 경로 조건에 맞는 키가 존재하는지 찾기
//         auto at = lower_bound(keys.begin(), keys.end(), key);  // 이 키 이상인 첫 그룹 위치
//         return at == keys.end() || *at != key ? -1 : (int)(at - keys.begin());  // 없는 키는 -1, 있으면 그룹 번호 반환
//     }  // 키의 그룹 번호 조회 끝
//     int prefix(int group, int count) const {  // 그룹의 앞 count개 압축 좌표에 저장된 경로 합
//         int result = 0, base = offset[group];  // 현재 합과 이 그룹의 배열 시작 칸
//         while (count > 0) {  // Fenwick의 서로 겹치지 않는 구간을 모아 앞부분 합산
//             result += bit[base + count - 1];  // 현재 접두 구간의 마지막 Fenwick 조각 추가
//             if (result >= MOD) result -= MOD;  // 두 나머지를 더한 뒤 정수 범위 안에서 정규화
//             count &= count - 1;  // 방금 더한 마지막 비트 구간 제거
//         }  // 접두 경로 합 계산 끝
//         return result;  // 해당 키·좌표 접두 구간의 경로 수
//     }  // Fenwick 접두 합 조회 끝
//     void add(int group, int64 value, int weight) {  // 한 초기점의 경로 수를 그 점의 키·좌표에 추가
//         if (!weight) return;  // 0인 경로 수는 트리를 바꾸지 않음
//         int base = offset[group], size = length[group];  // 이 그룹의 압축 좌표 범위
//         auto first = coordinate.begin() + base;  // 그룹 좌표의 첫 위치
//         int at = (int)(lower_bound(first, first + size, value) - first);  // 초기점 좌표의 정확한 압축 인덱스
//         while (at < size) {  // 이 좌표를 포함하는 Fenwick 상위 구간에 누적
//             int& stored = bit[base + at];  // 현재 상위 구간의 경로 합
//             stored += weight; if (stored >= MOD) stored -= MOD;  // 현재 점의 경로 수를 더하고 나머지 유지
//             at |= at + 1;  // 다음 Fenwick 상위 구간으로 이동
//         }  // 한 점의 경로 수 등록 끝
//     }  // 그룹별 점 갱신 끝
//     int open_sum(int64 key, int64 low, int64 high) const {  // 같은 키에서 low<x<high인 초기점의 경로 합
//         int group = group_id(key);  // 요청한 대각선 키의 그룹 조회
//         if (group < 0 || low >= high) return 0;  // 해당 키가 없거나 열린 구간이 비었으면 경로 없음
//         auto first = coordinate.begin() + offset[group];  // 이 그룹의 정렬된 좌표 시작
//         auto last = first + length[group];  // 이 그룹의 정렬된 좌표 끝
//         int left = (int)(upper_bound(first, last, low) - first);  // low와 같은 좌표도 제외한 첫 후보
//         int right = (int)(lower_bound(first, last, high) - first);  // high 이상인 좌표는 전부 제외
//         int result = prefix(group, right) - prefix(group, left);  // 두 접두 합의 차이로 열린 구간 합 계산
//         return result < 0 ? result + MOD : result;  // 음수 나머지를 0..MOD−1로 맞춤
//     }  // 열린 좌표 구간의 경로 합 조회 끝
//     int less_sum(int64 key, int64 bound) const {  // 같은 키에서 y<bound인 초기점의 역방향 경로 합
//         int group = group_id(key);  // 후속점의 x−y−k가 현재 x−y와 같은 그룹 선택
//         if (group < 0) return 0;  // 연결 가능한 키의 초기점이 없으면 경로 없음
//         auto first = coordinate.begin() + offset[group];  // 후속점들의 y좌표 시작
//         int count = (int)(lower_bound(first, first + length[group], bound) - first);  // 현재 y보다 엄격히 작은 후속점만 선택
//         return prefix(group, count);  // 그 후속점들에서 E로 가는 경로 합
//     }  // 역방향 y 경계 합 조회 끝
// };  // 키별 좌표 Fenwick 끝
// 
// struct Point {  // 정렬해도 유지할 초기점의 기하 정보와 그룹 번호
//     int64 x, y, k, diagonal, predecessor;  // x / y / 직사각형 반둘레 / x−y / x−y−k
//     int forward_group, backward_group;  // 정방향 x 그룹과 역방향 y 그룹의 압축 번호
// };  // 초기점 자료형 끝
// struct Addition {  // 독립적인 추가 쿼리의 임시 경로 정보
//     int64 x, y, diagonal;  // 새 점의 좌표와 x−y
//     int index, from_start; bool inside;  // 원래 쿼리 순서 / S에서 새 점까지의 경로 수 / 고정된 S·E 안쪽 여부
// };  // 추가 쿼리 자료형 끝
// 
// vector<int> solution(int n, vector<vector<int>> point, vector<vector<int>> query) {  // 초기 경로 수와 각 독립 추가·삭제 뒤의 경로 수 계산
//     vector<Point> points; points.reserve(n);  // 초기점을 64비트 기하 정보로 변환할 배열
//     vector<pair<int64,int64>> forward_entries, backward_entries;  // 정방향은 실제 x−y·x, 역방향은 x−y−k·y로 그룹 구성
//     forward_entries.reserve(n); backward_entries.reserve(n);  // 키·좌표 등록 중 임시 배열 재할당 방지
//     for (const auto& item : point) {  // 입력 순서의 초기점 정보 읽기
//         Point p{}; p.x = item[0]; p.y = item[1]; p.k = item[2];  // 그룹 번호까지 초기화한 뒤 좌표와 k를 64비트로 옮겨 차이 계산
//         p.diagonal = p.x - p.y; p.predecessor = p.diagonal - p.k;  // 직사각형 간선의 같은 대각선 조건으로 쓸 두 키
//         forward_entries.emplace_back(p.diagonal, p.x);  // 이 점이 이전 꼭짓점이 될 때 조회될 정방향 좌표
//         backward_entries.emplace_back(p.predecessor, p.y);  // 이 점이 다음 꼭짓점이 될 때 조회될 역방향 좌표
//         points.push_back(p);  // 변환한 초기점 저장
//     }  // 초기점 변환 끝
//     sort(points.begin(), points.end(), [](const Point& a, const Point& b) { return a.x < b.x; });  // x가 증가하는 방향이 DAG의 위상 순서
//     GroupFenwick forward(move(forward_entries)), backward(move(backward_entries));  // 키별 x 합과 키별 y 합을 서로 독립적인 트리로 준비
//     for (auto& p : points) {  // 초기점 갱신에 쓸 그룹 번호를 미리 찾아 둠
//         p.forward_group = forward.group_id(p.diagonal);  // 정방향에서 이 점의 f값을 넣을 그룹
//         p.backward_group = backward.group_id(p.predecessor);  // 역방향에서 이 점의 g값을 넣을 그룹
//     }  // 초기점 그룹 번호 연결 끝
//     vector<int> from_start(n, 0), to_end(n, 0);  // 초기점마다 S→점과 점→E 경로 수
//     for (int i = 0; i < n; ++i) {  // x 오름차순으로 이전 점들만 처리된 상태 유지
//         const Point& p = points[i];  // 현재 도착 꼭짓점
//         from_start[i] = i == 0 ? 1 : forward.open_sum(p.predecessor, p.x - p.k, p.x);  // S는 시작 1개, 나머지는 같은 키와 xp<x 및 yp>y를 만족하는 이전 경로 합
//         forward.add(p.forward_group, p.x, from_start[i]);  // 후속점이 현재 점을 이전 꼭짓점으로 사용할 수 있도록 f값 등록
//     }  // 초기 정방향 DP 끝
//     int base = from_start[n - 1];  // 원래 S와 E를 잇는 초기 귀걸이 수
//     vector<int> answer(query.size() + 1, base);  // 첫 답과 바뀌지 않는 추가 쿼리는 초기 경로 수로 준비
//     vector<Addition> additions; additions.reserve(query.size());  // 역방향 DP와 함께 처리할 추가점 쿼리 목록
//     for (size_t q = 0; q < query.size(); ++q) if (query[q][0] == 0) {  // 삭제는 뒤에서 곱을 빼고, 지금은 추가점만 준비
//         int64 x = query[q][1], y = query[q][2], k = query[q][3];  // 독립적으로 추가할 새 점의 64비트 기하 정보
//         int64 diagonal = x - y, predecessor = diagonal - k;  // 새 점에 들어오는 간선과 나가는 간선의 키
//         bool inside = points[0].x < x && x < points[n - 1].x && points[n - 1].y < y && y < points[0].y;  // 고정된 S·E의 열린 직사각형 밖에서는 새 S→E 경로를 만들 수 없음
//         int paths = inside ? forward.open_sum(predecessor, x - k, x) : 0;  // 완성된 초기 f 트리에서 새 점보다 왼쪽·위쪽인 이전 꼭짓점의 경로 합
//         additions.push_back({x, y, diagonal, (int)q, paths, inside});  // 초기점 트리에는 넣지 않고 쿼리 정보로만 보관
//     }  // 추가 쿼리의 정방향 경로 계산 끝
//     sort(additions.begin(), additions.end(), [](const Addition& a, const Addition& b) { return a.x > b.x; });  // 새 점 오른쪽의 초기점만 들어 있도록 x 내림차순 조회 순서
//     int next = n - 1;  // 아직 역방향 처리하지 않은 가장 오른쪽 초기점
//     auto insert_initial = [&](int index) {  // 초기점 하나의 g값을 계산하고 역방향 트리에 등록
//         const Point& p = points[index];  // 현재 출발 꼭짓점
//         to_end[index] = index == n - 1 ? 1 : backward.less_sum(p.diagonal, p.y);  // E는 도착 1개, 나머지는 오른쪽·아래쪽이면서 키가 맞는 후속 경로 합
//         backward.add(p.backward_group, p.y, to_end[index]);  // 더 왼쪽 초기점과 추가점이 현재 점을 후속 꼭짓점으로 조회하도록 등록
//     };  // 역방향 초기점 처리 동작 정의 끝
//     for (const auto& added : additions) {  // 각 추가 쿼리는 같은 초기 역방향 DP만 조회
//         while (next >= 0 && points[next].x > added.x) insert_initial(next--);  // 새 점보다 엄격히 오른쪽인 초기점까지 g값 계산·등록
//         if (!added.inside) continue;  // 고정된 S·E 밖의 추가는 이미 준비한 초기 답 유지
//         int paths = backward.less_sum(added.diagonal, added.y);  // 새 점보다 아래이며 간선 키가 맞는 후속점들의 E까지 경로 합
//         answer[added.index + 1] = (base + (int64)added.from_start * paths) % MOD;  // 새 점을 통과하는 경로 f_new×g_new만 초기 수에 추가
//     }  // 추가 쿼리의 역방향 경로 계산 끝
//     while (next >= 0) insert_initial(next--);  // 삭제 쿼리에서 쓸 나머지 초기점의 g값도 완성
//     for (size_t q = 0; q < query.size(); ++q) if (query[q][0] == 1) {  // 초기점 하나를 제거하는 독립 쿼리 처리
//         int64 x = query[q][1];  // x좌표가 모두 달라 이것만으로 삭제할 초기점 식별 가능
//         auto at = lower_bound(points.begin(), points.end(), x, [](const Point& p, int64 value) { return p.x < value; });  // 삭제점이 있는 정렬 위치 찾기
//         int index = (int)(at - points.begin());  // 정방향·역방향 경로 배열의 해당 점 인덱스
//         if (index == 0 || index == n - 1) {  // 처음 고정된 S 또는 E 자체를 삭제하는 경우
//             answer[q + 1] = 0;  // 새 끝점을 고르지 않으므로 가능한 귀걸이 없음
//         } else {  // 일반 초기점을 삭제하는 경우
//             int removed = (int)((int64)from_start[index] * to_end[index] % MOD);  // 그 점을 지나는 초기 경로 수는 S→점과 점→E의 곱
//             answer[q + 1] = base - removed;  // 사라진 경로만 초기 답에서 제외
//             if (answer[q + 1] < 0) answer[q + 1] += MOD;  // 음수 나머지를 요구 범위로 맞춤
//         }  // 삭제 쿼리 답 계산 끝
//     }  // 모든 초기점 삭제 쿼리 처리 끝
//     return answer;  // 초기 수와 입력 쿼리 순서의 독립 결과 반환
// }  // 귀걸이 경로 수 계산 끝

// 풀이 요약
// 이전 점 p에서 다음 점 v로 직사각형을 만들려면 xp<xv, yp>yv이고 (xv−xp)+(yp−yv)=kv. t=x−y로 두면 tp=tv−kv인 키 조건으로 정리.
// f[v]는 S→v, g[v]는 v→E 경로 수. x가 항상 커지므로 DAG이며, 삭제점 v를 지나는 경로는 f[v]g[v]개라 초기 수에서 이 곱만 빼기.
// 추가점도 초기점 사이에 한 번만 들어갈 수 있어 새 경로는 f_new×g_new개. 각 변화는 초기 상태에 독립적으로 적용하므로 추가점을 DP 트리에 넣지 않음.
// f는 x 오름차순으로 계산. 키 tv−kv인 이전 점에서 xv−kv<xp<xv인 f값을 키별 압축 Fenwick으로 합산하면 위쪽 조건까지 만족.
// g는 x 내림차순으로 계산. 후속점의 키 t−k별 y Fenwick에 g를 넣고, 현재 t와 같은 키에서 y가 엄격히 작은 후속점만 합산.
// 추가점의 g 조회도 같은 내림차순 스위프에 끼워 넣어 오른쪽 초기점만 활성화. f_new는 완성된 초기 f 트리에서 열린 x구간 합으로 조회.
// S와 E는 최초 위치로 고정. 둘 중 하나를 삭제하면0, 그 열린 직사각형 밖에 추가한 점은 초기 경로 수 그대로.
// 키·좌표 경계는 long long으로 계산하고 경로 수는1,000,000,007로 나눈 나머지 유지. 시간 O((N+Q) log N), 공간 O(N+Q).
~~~

## 채점 기록

2026-10-24 사이트 채점: 정답 100/100. 1번째 제출에서 통과. C++ 제출 내역에서도 같은 날짜의 정답 기록 확인.

줄별 설명과 풀이 요약을 포함한 코드를 제출. 로컬 검사 횟수와 실행 시간은 사이트 채점 기록과 별도로 보관.
