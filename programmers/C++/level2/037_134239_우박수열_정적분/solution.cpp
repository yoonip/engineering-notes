#include <vector>
using namespace std;

vector<double> solution(int k, vector<vector<int>> ranges) {
    vector<double> prefix{0.0};
    while (k > 1) {
        int next = k % 2 == 0 ? k / 2 : 3 * k + 1;
        prefix.push_back(prefix.back() + (k + next) / 2.0);
        k = next;
    }
    int n = (int)prefix.size() - 1;
    vector<double> answer;
    for (const auto& range : ranges) {
        int start = range[0], end = n + range[1];
        answer.push_back(start <= end ? prefix[end] - prefix[start] : -1.0);
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// vector<double> solution(int k, vector<vector<int>> ranges) {  // 사다리꼴 넓이 누적합으로 우박수열 적분 계산
// vector<double> prefix{0.0};  // 구간별 사다리꼴 넓이의 누적합을 0부터 저장
// while (k > 1) {  // 콜라츠 수열이 1이 될 때까지 생성
// int next = k % 2 == 0 ? k / 2 : 3 * k + 1;  // 홀짝에 따라 다음 수열 값 구하기
// prefix.push_back(prefix.back() + (k + next) / 2.0);  // 너비가 1인 사다리꼴 넓이 누적
// k = next;  // 다음 수열 값을 현재 값으로 바꾸기
// }  // 블록 끝
// int n = (int)prefix.size() - 1;  // 수열의 마지막 x좌표 구하기
// vector<double> answer;  // 요청별 정적분 결과 저장
// for (const auto& range : ranges) {  // 각 정적분 범위 처리
// int start = range[0], end = n + range[1];  // 상대적인 끝 오프셋을 실제 좌표로 바꾸기
// answer.push_back(start <= end ? prefix[end] - prefix[start] : -1.0);  // 유효한 범위는 누적합의 차이, 역전 범위는 -1 기록
// }  // 블록 끝
// return answer;  // 모든 범위의 정적분 값 반환
// }  // 블록 끝

// 풀이 요약
// 콜라츠 수열 인접 값 사이의 사다리꼴 넓이를 누적하고 요청 범위의 누적합 차이로 정적분 구하기
