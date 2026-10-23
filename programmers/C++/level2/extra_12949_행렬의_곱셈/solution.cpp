#include <vector>
using namespace std;

vector<vector<int>> solution(vector<vector<int>> arr1, vector<vector<int>> arr2) {
    int rows = (int)arr1.size(), middle = (int)arr2.size(), cols = (int)arr2[0].size();
    vector<vector<int>> answer(rows, vector<int>(cols, 0));
    for (int r = 0; r < rows; ++r) for (int c = 0; c < cols; ++c) for (int k = 0; k < middle; ++k) answer[r][c] += arr1[r][k] * arr2[k][c];
    return answer;
}

// 전체 코드 줄별 설명
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// vector<vector<int>> solution(vector<vector<int>> arr1, vector<vector<int>> arr2) {  // 첫 행렬의 행과 둘째 행렬의 열을 내적
// int rows = (int)arr1.size(), middle = (int)arr2.size(), cols = (int)arr2[0].size();  // 결과 행 수, 내적 길이, 결과 열 수 구하기
// vector<vector<int>> answer(rows, vector<int>(cols, 0));  // 곱셈 결과 행렬을 0으로 초기화
// for (int r = 0; r < rows; ++r) for (int c = 0; c < cols; ++c) for (int k = 0; k < middle; ++k) answer[r][c] += arr1[r][k] * arr2[k][c];  // 첫 행렬의 행과 둘째 행렬의 열을 내적
// return answer;  // 행렬 곱 반환
// }  // 블록 끝

// 풀이 요약
// 첫 행렬의 각 행과 둘째 행렬의 각 열을 내적해 결과 행렬 채우기
