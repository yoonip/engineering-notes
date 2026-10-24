#include <algorithm>
#include <cstdint>
#include <vector>
using namespace std;

struct Point { long long x, y; };
long long turn(Point a, Point b, Point c) {
    return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x);
}

int solution(int n, vector<vector<int>> triangle, vector<vector<int>> v) {
    Point a{triangle[0][0], triangle[0][1]};
    Point b{triangle[1][0], triangle[1][1]};
    Point c{triangle[2][0], triangle[2][1]};
    if (turn(a, b, c) < 0) swap(b, c);
    vector<Point> point;
    for (const auto& p : v) point.push_back({p[0], p[1]});
    sort(point.begin(), point.end(), [c](Point p, Point q) {
        return turn(c, p, q) > 0;
    });
    int words = (n + 63) / 64;
    vector<vector<uint64_t>> al(n + 1, vector<uint64_t>(words));
    vector<vector<uint64_t>> ar = al, bl = al, br = al;
    vector<vector<int>> prefix(n + 1, vector<int>(n + 2));
    for (int i = 0; i <= n; ++i) {
        Point p = i == n ? b : point[i];
        Point q = i == n ? c : point[i];
        prefix[i][1] = 1;
        for (int j = 0; j < n; ++j) {
            long long x = turn(a, p, point[j]);
            long long y = turn(b, q, point[j]);
            uint64_t bit = uint64_t{1} << (j % 64);
            if (x > 0) al[i][j / 64] |= bit;
            if (x < 0) ar[i][j / 64] |= bit;
            if (y > 0) bl[i][j / 64] |= bit;
            if (y < 0) br[i][j / 64] |= bit;
            prefix[i][j + 2] = prefix[i][j + 1] + (x > 0);
        }
    }
    int answer = 0;
    for (int i = 0; i <= n; ++i) {
        Point p = i == n ? b : point[i];
        for (int j = 0; j <= n; ++j) {
            Point q = j == n ? c : point[j];
            if (i < n && turn(b, q, p) <= 0) continue;
            int low = 0, high = n;
            for (int w = words - 1; w >= 0; --w) {
                uint64_t bits = al[i][w] & bl[j][w];
                if (bits) { low = w * 64 + 64 - __builtin_clzll(bits); break; }
            }
            for (int w = 0; w < words; ++w) {
                uint64_t bits = ar[i][w] & br[j][w];
                if (bits) { high = w * 64 + __builtin_ctzll(bits) + 1; break; }
            }
            if (j < n) high = min(high, j);
            if (low <= high) answer += prefix[i][high + 1] - prefix[i][low];
        }
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬과 두 인덱스의 최솟값·최댓값에 쓸 헤더
// #include <cstdint>  // 핀 집합을 64비트씩 묶을 정수형
// #include <vector>  // 좌표, 비트 집합, 누적 개수를 담을 벡터
// using namespace std;  // 표준 라이브러리 이름을 짧게 사용
//
// struct Point { long long x, y; };  // 좌표 차와 외적은 long long으로 계산
// long long turn(Point a, Point b, Point c) {  // a→b에서 c가 어느 쪽인지 외적으로 확인
//     return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x);  // 양수는 왼쪽, 음수는 오른쪽이고 범위는 64비트 안에 들어옴
// }  // 외적 함수 끝
//
// int solution(int n, vector<vector<int>> triangle, vector<vector<int>> v) {  // 안쪽 핀과 바깥 삼각형을 받아 가능한 모양 수를 반환
//     Point a{triangle[0][0], triangle[0][1]};  // 첫 고정 꼭짓점을 a로 둠
//     Point b{triangle[1][0], triangle[1][1]};  // 두 번째 고정 꼭짓점
//     Point c{triangle[2][0], triangle[2][1]};  // 세 번째 고정 꼭짓점
//     if (turn(a, b, c) < 0) swap(b, c);  // 바깥 삼각형 방향을 반시계로 맞춤
//     vector<Point> point;  // 안쪽 핀을 외적 계산용 좌표로 옮길 공간
//     for (const auto& p : v) point.push_back({p[0], p[1]});  // 입력 좌표를 하나씩 저장
//     sort(point.begin(), point.end(), [c](Point p, Point q) {  // c에서 본 각도순으로 핀을 정렬
//         return turn(c, p, q) > 0;  // c의 안쪽 각은 180도 미만이고 세 핀이 일직선이 아니므로 외적으로 각도 순서 결정
//     });  // 정렬 끝; 핀 i의 각도 순위는 i+1
//     int words = (n + 63) / 64;  // 핀 n개의 비트 집합에 필요한 64비트 칸 수
//     vector<vector<uint64_t>> al(n + 1, vector<uint64_t>(words));  // a의 첫 접선 왼쪽에 있는 핀 집합
//     vector<vector<uint64_t>> ar = al, bl = al, br = al;  // a 오른쪽과 b의 양쪽 집합도 같은 크기로 준비
//     vector<vector<int>> prefix(n + 1, vector<int>(n + 2));  // a 접선별로 c의 첫 핀 후보를 각도순 누적
//     for (int i = 0; i <= n; ++i) {  // 첫 핀 n개와 안 꺾인 고무줄을 모두 살펴봄
//         Point p = i == n ? b : point[i];  // a→b 고무줄의 첫 핀; b면 직선 그대로
//         Point q = i == n ? c : point[i];  // b→c 고무줄의 첫 핀; c면 직선 그대로
//         prefix[i][1] = 1;  // c→a가 직선인 각도 순위 0은 항상 후보
//         for (int j = 0; j < n; ++j) {  // 각 안쪽 핀의 위치 관계를 미리 계산
//             long long x = turn(a, p, point[j]);  // a의 첫 접선 기준으로 이 핀의 방향
//             long long y = turn(b, q, point[j]);  // b의 첫 접선 기준으로 이 핀의 방향
//             uint64_t bit = uint64_t{1} << (j % 64);  // 핀 j를 나타낼 비트 하나
//             if (x > 0) al[i][j / 64] |= bit;  // a 접선 왼쪽 집합에 추가
//             if (x < 0) ar[i][j / 64] |= bit;  // a 접선 오른쪽 집합에 추가; 접선 위 핀은 제외
//             if (y > 0) bl[i][j / 64] |= bit;  // b 접선 왼쪽 집합에 추가
//             if (y < 0) br[i][j / 64] |= bit;  // b 접선 오른쪽 집합에 추가
//             prefix[i][j + 2] = prefix[i][j + 1] + (x > 0);  // c의 첫 핀이 a 접선 왼쪽일 때만 누적 개수에 더함
//         }  // 접선 하나의 전처리 끝
//     }  // a와 b의 모든 첫 핀 전처리 끝
//     int answer = 0;  // 조건을 만족한 서로 다른 세 고무줄의 수
//     for (int i = 0; i <= n; ++i) {  // a 쪽 고무줄의 첫 핀 고정
//         Point p = i == n ? b : point[i];  // 직선 후보까지 포함한 첫 접점
//         for (int j = 0; j <= n; ++j) {  // b 쪽 고무줄의 첫 핀 고정
//             Point q = j == n ? c : point[j];  // b 쪽 직선 후보는 c
//             if (i < n && turn(b, q, p) <= 0) continue;  // a의 첫 핀이 b 접선 오른쪽이거나 공유 접점이면 제외
//             int low = 0, high = n;  // c 첫 핀의 각도 순위 범위; 0은 a
//             for (int w = words - 1; w >= 0; --w) {  // 두 왼쪽 집합의 가장 큰 각도 순위를 찾음
//                 uint64_t bits = al[i][w] & bl[j][w];  // 두 접선 모두 왼쪽에 있는 핀만 남김
//                 if (bits) { low = w * 64 + 64 - __builtin_clzll(bits); break; }  // 이 핀보다 작은 c 접선은 빈 삼각형 안에 핀을 남김
//             }  // 왼쪽 핀 때문에 생기는 하한 계산 끝
//             for (int w = 0; w < words; ++w) {  // 두 오른쪽 집합의 가장 작은 각도 순위를 찾음
//                 uint64_t bits = ar[i][w] & br[j][w];  // 세 직선이 반대로 감싼 삼각형도 비어 있어야 함
//                 if (bits) { high = w * 64 + __builtin_ctzll(bits) + 1; break; }  // 이 핀보다 큰 c 접선은 반대 삼각형에 핀을 남김
//             }  // 오른쪽 핀 때문에 생기는 상한 계산 끝
//             if (j < n) high = min(high, j);  // b의 첫 핀이 c 접선 왼쪽이어야 하므로 그 각도 직전까지만
//             if (low <= high) answer += prefix[i][high + 1] - prefix[i][low];  // 남은 각도 범위에서 c 첫 핀이 a 접선 왼쪽인 후보 수를 더함
//         }  // b 첫 핀 반복 끝
//     }  // a 첫 핀 반복 끝
//     return answer;  // 각 첫 핀 조합이 정하는 모양을 한 번씩 센 결과
// }  // 풀이 함수 끝
//

// 풀이 요약
// 세 고무줄은 각 고정 꼭짓점에서 처음 만나는 핀을 정하면 빈 모양 조건에 따라 나머지 경로도 정해짐.
// 첫 핀 세 개가 서로의 고무줄을 침범하거나 공유하지 않아야 하고, 세 첫 접선이 둘러싼 삼각형 안에도 다른 핀이 없어야 함.
// c에서 본 각도로 안쪽 핀을 정렬. a와 b 접선을 먼저 정하면 두 왼쪽 집합의 최대 각도와 두 오른쪽 집합의 최소 각도가 c 접선의 허용 범위를 만듦.
// 반대 방향으로 둘러싸는 경우도 있어 왼쪽 교집합만 확인하면 빠지는 반례가 생김. 양쪽 교집합을 함께 확인.
// c 첫 핀이 a 접선 왼쪽인 후보 수를 미리 누적해 두면 허용 각도 구간의 개수는 뺄셈 한 번으로 계산 가능.
// 비트 집합의 최상위·최하위 비트를 이용해 시간 O(n² ceil(n/64)+n log n), 공간 O(n²). 좌표 외적은 64비트 정수.
// 접선으로 모양을 정하는 관찰은 카카오 공식 본선 해설 참고: https://tech.kakao.com/posts/342
