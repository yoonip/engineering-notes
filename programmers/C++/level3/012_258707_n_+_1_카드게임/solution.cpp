#include <array>
#include <unordered_set>
#include <vector>
using namespace std;

int solution(int coin, vector<int> cards) {
    int n = (int)cards.size(), target = n + 1;
    unordered_set<int> initial(cards.begin(), cards.begin() + n / 3), drawn;
    array<int, 3> available{0, 0, 0};
    for (int card : initial) if (card < target - card && initial.count(target - card)) ++available[0];
    int round_number = 1;
    for (int index = n / 3; index < n; index += 2) {
        for (int j = index; j < index + 2; ++j) {
            int card = cards[j], partner = target - card;
            if (initial.count(partner)) ++available[1];
            else if (drawn.count(partner)) ++available[2];
            drawn.insert(card);
        }
        bool continued = false;
        for (int price = 0; price <= 2; ++price) if (available[price] && coin >= price) {
            --available[price]; coin -= price; ++round_number; continued = true; break;
        }
        if (!continued) return round_number;
    }
    return round_number;
}

// 전체 코드 줄별 설명
// #include <array>  // 크기가 고정된 array
// #include <unordered_set>  // 중복을 걸러 낼 해시 집합
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(int coin, vector<int> cards) {  // 라운드마다 동전이 적게 드는 카드 쌍부터 사용
// int n = (int)cards.size(), target = n + 1;  // 전체 카드 수와 한 쌍의 목표 합 구하기
// unordered_set<int> initial(cards.begin(), cards.begin() + n / 3), drawn;  // 처음 받은 카드와 이후 나온 카드를 구분
// array<int, 3> available{0, 0, 0};  // 동전 0개, 1개, 2개로 완성할 쌍의 수 저장
// for (int card : initial) if (card < target - card && initial.count(target - card)) ++available[0];  // 처음 받은 카드끼리의 쌍을 한 번씩 세기
// int round_number = 1;  // 현재 라운드 번호를 1로 초기화
// for (int index = n / 3; index < n; index += 2) {  // 매 라운드 두 카드를 공개
// for (int j = index; j < index + 2; ++j) {  // 공개한 각 카드의 짝 확인
// int card = cards[j], partner = target - card;  // 현재 카드와 필요한 짝 구하기
// if (initial.count(partner)) ++available[1];  // 처음 카드와 만들 수 있으면 동전 하나짜리 쌍
// else if (drawn.count(partner)) ++available[2];  // 이후 카드끼리면 동전 두 개짜리 쌍
// drawn.insert(card);  // 이후 공개된 카드 집합에 현재 카드 넣기
// }  // 블록 끝
// bool continued = false;  // 이번 라운드를 통과했는지 표시
// for (int price = 0; price <= 2; ++price) if (available[price] && coin >= price) {  // 가장 저렴한 완성 쌍부터 사용
// --available[price]; coin -= price; ++round_number; continued = true; break;  // 쌍과 동전을 소비하고 다음 라운드로 가기
// }  // 블록 끝
// if (!continued) return round_number;  // 쌍을 낼 수 없으면 현재 라운드가 최댓값
// }  // 블록 끝
// return round_number;  // 모든 공개를 처리한 뒤의 라운드 반환
// }  // 블록 끝

// 풀이 요약
// 합이 n+1인 쌍을 필요한 동전 수별로 세고 매 라운드 공개된 카드로 새 쌍을 추가해 가장 저렴한 쌍부터 사용
