#include <numeric>
#include <vector>
using namespace std;

vector<int> solution(int n, long long k) {
    vector<int> available(n), answer;
    iota(available.begin(), available.end(), 1);
    --k; long long block = 1;
    for (int i = 2; i <= n; ++i) block *= i;
    for (int remaining = n; remaining > 0; --remaining) {
        block /= remaining;
        long long index = k / block; k %= block;
        answer.push_back(available[(size_t)index]);
        available.erase(available.begin() + index);
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <numeric>  // 누적합·최대공약수 같은 수치 알고리즘
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// vector<int> solution(int n, long long k) {  // 팩토리얼 묶음 크기로 k번째 순열 복원
// vector<int> available(n), answer;  // 아직 줄에 세우지 않은 사람과 최종 순서 저장
// iota(available.begin(), available.end(), 1);  // 사람 번호를 1부터 n까지 채우기
// --k; long long block = 1;  // 순번을 0부터 시작하도록 바꾸고 팩토리얼 초기화
// for (int i = 2; i <= n; ++i) block *= i;  // n!을 넓은 정수형으로 계산
// for (int remaining = n; remaining > 0; --remaining) {  // 각 자리에 올 사람을 앞에서부터 정하기
// block /= remaining;  // 한 사람을 고정했을 때 남는 순열 수 구하기
// long long index = k / block; k %= block;  // 이번 사람의 후보 인덱스와 해당 묶음 안의 순번 구하기
// answer.push_back(available[(size_t)index]);  // 선택한 사람을 줄에 추가
// available.erase(available.begin() + index);  // 선택한 사람을 남은 후보에서 제거
// }  // 블록 끝
// return answer;  // 사전순 k번째 줄 세우기 반환
// }  // 블록 끝

// 풀이 요약
// 남은 사람 수의 팩토리얼로 순열 묶음 크기를 구하고 순번의 몫으로 다음 사람 선택
