#include <string>
#include <vector>

using namespace std;

int func1(int humidity, int val_set){
    if(humidity < val_set)
        return 3;
    return 1;
}

int func2(int humidity){
    if(humidity >= 50)
        return 0;
    else if (humidity >= 40)
        return 1;
    else if (humidity >= 30)
        return 2;
    else if (humidity >= 20)
        return 3;
    else if (humidity >= 10)
        return 4;
    else
        return 5;
}

int func3(int humidity, int val_set){
    if(humidity < val_set)
        return 1;
    return 0;
}

int solution(string mode_type, int humidity, int val_set) {
    int answer = 0;
    if(mode_type == "auto"){
        answer = func2(humidity);
    }
    else if(mode_type == "target"){
        answer = func1(humidity, val_set);
    }
    else if(mode_type == "minimum"){
        answer = func3(humidity, val_set);
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 다룰 string
// #include <vector>  // 길이를 늘릴 수 있는 vector
//
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// int func1(int humidity, int val_set){  // 목표 모드의 가습 단계 결정
//     if(humidity < val_set)  // 목표 습도에 아직 못 미친 경우
//         return 3;  // 목표 습도 미달이니 3단계로 가습
//     return 1;  // 목표 습도에 도달하면 1단계 유지
// }  // 블록 끝
//
// int func2(int humidity){  // 현재 습도 구간에 따른 자동 모드 단계
//     if(humidity >= 50)  // 습도 50% 이상이면 가습 중지
//         return 0;  // 자동 모드에서 가습 중지
//     else if (humidity >= 40)  // 40% 이상 50% 미만
//         return 1;  // 자동 모드의 40%대 습도는 1단계
//     else if (humidity >= 30)  // 30% 이상 40% 미만
//         return 2;  // 자동 모드의 30%대 습도는 2단계
//     else if (humidity >= 20)  // 20% 이상 30% 미만
//         return 3;  // 자동 모드의 20%대 습도는 3단계
//     else if (humidity >= 10)  // 10% 이상 20% 미만
//         return 4;  // 자동 모드의 10%대 습도는 4단계
//     else  // 습도가 10%보다 낮은 경우
//         return 5;  // 가장 건조한 구간은 5단계
// }  // 블록 끝
//
// int func3(int humidity, int val_set){  // 최소 모드에서 설정 습도 미달 여부 확인
//     if(humidity < val_set)  // 최소 유지 습도보다 낮은 경우
//         return 1;  // 최소 습도보다 낮으면 1단계로 가습
//     return 0;  // 최소 습도 이상이면 가습 중지
// }  // 블록 끝
//
// int solution(string mode_type, int humidity, int val_set) {  // [PCCE 기출문제] 7번 / 가습기 풀이 시작
//     int answer = 0;  // 선택한 모드에서 사용할 가습 단계
//     if(mode_type == "auto"){  // 현재 습도 구간으로 가습 단계를 고르는 자동 모드
//         answer = func2(humidity);  // 자동 모드의 습도별 단계 적용
//     }  // 블록 끝
//     else if(mode_type == "target"){  // 목표 습도를 유지하는 모드
//         answer = func1(humidity, val_set);  // 목표 미달은 3단계, 도달하면 1단계
//     }  // 블록 끝
//     else if(mode_type == "minimum"){  // 설정 습도 미만에서만 작동하는 모드
//         answer = func3(humidity, val_set);  // 최소 습도 미달일 때만 1단계
//     }  // 블록 끝
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 자동 모드는 습도 구간에 맞는 단계를 반환. 목표·최소 모드는 설정 습도보다 낮은지 비교해 해당 단계를 반환
