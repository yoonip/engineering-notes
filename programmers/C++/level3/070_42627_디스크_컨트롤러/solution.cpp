#include <algorithm>
#include <functional>
#include <queue>
#include <tuple>
#include <vector>
using namespace std;

int solution(vector<vector<int>> jobs) {
    vector<tuple<int,int,int>> arrivals;
    for (int i = 0; i < (int)jobs.size(); ++i) arrivals.push_back({jobs[i][0],jobs[i][1],i});
    sort(arrivals.begin(), arrivals.end());
    priority_queue<tuple<int,int,int>,vector<tuple<int,int,int>>,greater<tuple<int,int,int>>> heap;
    int index = 0, time = 0; long long total = 0;
    while (index < (int)arrivals.size() || !heap.empty()) {
        if (heap.empty() && index < (int)arrivals.size()) time = max(time, get<0>(arrivals[index]));
        while (index < (int)arrivals.size() && get<0>(arrivals[index]) <= time) { auto [start,duration,number] = arrivals[index++]; heap.push({duration,start,number}); }
        auto [duration,start,number] = heap.top(); heap.pop(); time += duration; total += time - start;
    }
    return (int)(total / jobs.size());
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <functional>  // 재귀 람다를 담는 function과 함수 객체
// #include <queue>  // BFS 큐와 우선순위 큐
// #include <tuple>  // 여러 상태 값을 묶는 tuple
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(vector<vector<int>> jobs) {  // 대기 작업의 소요 시간 우선으로 평균 반환 시간 계산
// vector<tuple<int,int,int>> arrivals;  // 요청 시각, 소요 시간, 작업 번호 묶기
// for (int i = 0; i < (int)jobs.size(); ++i) arrivals.push_back({jobs[i][0],jobs[i][1],i});  // 입력 작업의 원래 번호를 보존
// sort(arrivals.begin(), arrivals.end());  // 도착 시각 순서로 작업 정렬
// priority_queue<tuple<int,int,int>,vector<tuple<int,int,int>>,greater<tuple<int,int,int>>> heap;  // 소요 시간, 요청 시각, 번호 순으로 대기 작업 고르기
// int index = 0, time = 0; long long total = 0;  // 다음 도착 인덱스와 현재 시각 및 반환 시간 합계 초기화
// while (index < (int)arrivals.size() || !heap.empty()) {  // 도착하지 않았거나 대기 중인 작업을 모두 처리
// if (heap.empty() && index < (int)arrivals.size()) time = max(time, get<0>(arrivals[index]));  // 대기 작업이 없으면 다음 도착 시각으로 건너뛰기
// while (index < (int)arrivals.size() && get<0>(arrivals[index]) <= time) { auto [start,duration,number] = arrivals[index++]; heap.push({duration,start,number}); }  // 현재 시각까지 도착한 작업을 우선순위 큐에 넣기
// auto [duration,start,number] = heap.top(); heap.pop(); time += duration; total += time - start;  // 선택한 작업을 끝내고 요청부터 완료까지의 시간을 더하기
// }  // 블록 끝
// return (int)(total / jobs.size());  // 평균 반환 시간의 정수 부분 반환
// }  // 블록 끝

// 풀이 요약
// 도착한 작업들을 소요 시간, 요청 시각, 작업 번호 순으로 선택해 처리하고 요청부터 완료까지의 평균 시간 구하기
