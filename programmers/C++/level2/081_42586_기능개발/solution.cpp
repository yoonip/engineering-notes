#include <vector>
using namespace std;

vector<int> solution(vector<int> progresses, vector<int> speeds) {
    vector<int> answer; int release_day = 0;
    for (int i = 0; i < (int)progresses.size(); ++i) {
        int days = (100 - progresses[i] + speeds[i] - 1) / speeds[i];
        if (days > release_day) { answer.push_back(1); release_day = days; }
        else ++answer.back();
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// vector<int> solution(vector<int> progresses, vector<int> speeds) {  // 앞 기능의 배포일에 함께 나갈 완료 기능 묶기
// vector<int> answer; int release_day = 0;  // 배포 묶음과 현재 묶음의 배포일 초기화
// for (int i = 0; i < (int)progresses.size(); ++i) {  // 기능을 개발 순서대로 확인
// int days = (100 - progresses[i] + speeds[i] - 1) / speeds[i];  // 완료까지 남은 날을 올림 나눗셈으로 구하기
// if (days > release_day) { answer.push_back(1); release_day = days; }  // 기존 배포일보다 늦으면 새 배포 묶음을 시작
// else ++answer.back();  // 먼저 완료한 기능은 앞 기능과 같은 날 배포
// }  // 블록 끝
// return answer;  // 배포일별 기능 수 반환
// }  // 블록 끝

// 풀이 요약
// 기능별 완료일을 올림 나눗셈으로 구하고 앞 기능의 배포일 안에 완료되면 같은 묶음에 포함
