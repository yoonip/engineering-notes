#include <algorithm>
#include <initializer_list>
using namespace std;

int solution(int dist_limit, int split_limit) {
    long long distance = dist_limit, split = split_limit;
    auto binary_cost = [](long long count, int depth) {
        long long total = 0;
        for (int i = 0; i < depth; ++i) {
            total += count;
            count = (count + 1) / 2;
        }
        return total;
    };
    long long answer = 1, width = 1;
    int depth = 0;
    while (width <= split) {
        answer = max(answer, min(width, distance + 1));
        long long power = 1;
        while (power <= split / width / 3) power *= 3;
        if (depth == 0) {
            answer = max(answer, 1 + 2 * min(distance, (power - 1) / 2));
        } else if (power > 1) {
            long long low = 1, high = width / 2;
            while (low < high) {
                long long mid = low + (high - low) / 2;
                long long needed = binary_cost(mid, depth) + mid * (power - 1);
                if (needed >= distance) high = mid;
                else low = mid + 1;
            }
            for (long long count : {low - 1, low}) {
                if (count == 0) continue;
                long long used = binary_cost(count, depth);
                if (used <= distance) {
                    long long ternary = min(distance - used, count * (power - 1));
                    answer = max(answer, 1 + used + 2 * ternary);
                }
            }
        }
        if (width > split / 2) break;
        width *= 2;
        ++depth;
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <initializer_list>  // 중괄호 초기화 목록 자료형
// using namespace std;  // std:: 접두사 생략
// int solution(int dist_limit, int split_limit) {  // 거리와 분기 제한 안에서 리프 수 최대화
// long long distance = dist_limit, split = split_limit;  // 입력을 넓은 정수형으로 옮겨 중간 곱셈 계산
// auto binary_cost = [](long long count, int depth) {  // 이진 분기에 필요한 거리 비용을 계산하는 람다
// long long total = 0;  // 거리 비용 합계 초기화
// for (int i = 0; i < depth; ++i) {  // 지정한 깊이만큼 상위 단계로 올라가기
// total += count;  // 현재 단계의 비용을 더하기
// count = (count + 1) / 2;  // 다음 단계의 필요한 분기 수를 올림 나눗셈으로 구하기
// }  // 블록 끝
// return total;  // 전체 이진 분기 비용 반환
// };  // 블록 끝
// long long answer = 1, width = 1;  // 최소 리프 수와 현재 이진 분기의 폭 초기화
// int depth = 0;  // 이진 분기 깊이 초기화
// while (width <= split) {  // 분기 제한 안에서 가능한 이진 깊이 검사
// answer = max(answer, min(width, distance + 1));  // 이진 분기만 사용하는 경우의 리프 수 비교
// long long power = 1;  // 가능한 삼진 분기 배율 초기화
// while (power <= split / width / 3) power *= 3;  // 곱셈 범위를 넘지 않게 최대 3의 거듭제곱 구하기
// if (depth == 0) {  // 이진 분기 없이 삼진 분기만 사용하는 경우
// answer = max(answer, 1 + 2 * min(distance, (power - 1) / 2));  // 거리와 분기 제한 안의 리프 수 비교
// } else if (power > 1) {  // 이진 분기 뒤에 삼진 분기를 붙일 수 있는 경우
// long long low = 1, high = width / 2;  // 확장할 분기 수의 이분 탐색 범위를 설정하기
// while (low < high) {  // 필요한 비용이 거리 제한에 닿는 경계 찾기
// long long mid = low + (high - low) / 2;  // 중간 후보 계산
// long long needed = binary_cost(mid, depth) + mid * (power - 1);  // 이진 및 삼진 확장의 최대 비용 구하기
// if (needed >= distance) high = mid;  // 경계가 왼쪽에 있으면 상한 줄이기
// else low = mid + 1;  // 비용이 작으면 하한 늘리기
// }  // 블록 끝
// for (long long count : {low - 1, low}) {  // 경계 양옆의 후보 확인
// if (count == 0) continue;  // 분기가 없는 후보는 건너뛰기
// long long used = binary_cost(count, depth);  // 이진 분기에 먼저 필요한 거리 계산
// if (used <= distance) {  // 이진 분기가 가능한 후보만 처리
// long long ternary = min(distance - used, count * (power - 1));  // 남은 거리와 분기 한도 안의 삼진 확장 수 구하기
// answer = max(answer, 1 + used + 2 * ternary);  // 전체 리프 수의 최댓값 갱신
// }  // 블록 끝
// }  // 블록 끝
// }  // 블록 끝
// if (width > split / 2) break;  // 다음 두 배 폭이 범위를 넘으면 반복을 끝
// width *= 2;  // 다음 이진 깊이의 폭으로 바꾸기
// ++depth;  // 이진 분기 깊이를 한 단계 늘리기
// }  // 블록 끝
// return answer;  // 최대 리프 노드 수 반환
// }  // 블록 끝

// 풀이 요약
// 이진 분기 깊이별로 가능한 삼진 분기 배율을 구하고 거리 제한에 가까운 분기 수를 이분 탐색해 최대 리프 수 비교
