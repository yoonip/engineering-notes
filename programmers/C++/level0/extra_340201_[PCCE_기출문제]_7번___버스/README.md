# [PCCE 기출문제] 7번 / 버스

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/340201) · Level 0 · C++

## 풀이

정거장별 On과 Off의 개수를 더하고 빼기. 좌석 수에서 승객 수를 뺀 값이 음수이면 0으로 바꾸기

## 코드와 줄별 설명

빈칸 채우기·한 줄 수정 문제. 사이트에는 정해진 부분만 제출했고, 이 파일은 전체 코드에 메모를 붙인 보관용.

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <string>
#include <vector>

using namespace std;

int func1(int num){
    if(0 > num){
        return 0;
    }
    else{
        return num;
    }
}

int func2(int num){
    if(num > 0){
        return 0;
    }
    else{
        return num;
    }
}

int func3(vector<string> station){
    int num = 0;
    for(int i=0; i<station.size(); i++){
        if(station[i] == "Off"){
            num += 1;
        }
    }
    return num;
}

int func4(vector<string> station){
    int num = 0;
    for(int i=0; i<station.size(); i++){
        if(station[i] == "On"){
            num += 1;
        }
    }
    return num;
}

int solution(int seat, vector<vector<string>> passengers) {
    int num_passenger = 0;
    for(int i=0; i<passengers.size(); i++){
        num_passenger += func4(passengers[i]);
        num_passenger -= func3(passengers[i]);
    }
    int answer = func1(seat - num_passenger);
    return answer;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 다룰 string
// #include <vector>  // 길이를 늘릴 수 있는 vector
//
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// int func1(int num){  // 남은 좌석 수가 음수이면 0으로 제한
//     if(0 > num){  // 승객 수가 좌석 수를 넘긴 경우
//         return 0;  // 남는 좌석이 없으니 0
//     }  // 블록 끝
//     else{  // 남은 좌석 수가 0 이상인 경우
//         return num;  // 음수가 아닌 남은 좌석 수
//     }  // 블록 끝
// }  // 블록 끝
//
// int func2(int num){  // 입력의 음수 부분만 남기는 보조 함수
//     if(num > 0){  // 입력이 양수인 경우
//         return 0;  // 양수 부분을 제거
//     }  // 블록 끝
//     else{  // 입력이 0 이하이면 그대로 유지
//         return num;  // 입력의 음수 부분
//     }  // 블록 끝
// }  // 블록 끝
//
// int func3(vector<string> station){  // 정거장 기록에서 Off의 개수 세기
//     int num = 0;  // 하차한 사람 수
//     for(int i=0; i<station.size(); i++){  // 정거장의 기록에서 하차 표시 찾기
//         if(station[i] == "Off"){  // 내린 사람을 나타내는 기록
//             num += 1;  // 하차 인원 하나 추가
//         }  // 블록 끝
//     }  // 블록 끝
//     return num;  // 이 정거장에서 내린 사람 수
// }  // 블록 끝
//
// int func4(vector<string> station){  // 정거장 기록에서 On의 개수 세기
//     int num = 0;  // 승차한 사람 수
//     for(int i=0; i<station.size(); i++){  // 정거장의 기록에서 승차 표시 찾기
//         if(station[i] == "On"){  // 탄 사람을 나타내는 기록
//             num += 1;  // 승차 인원 하나 추가
//         }  // 블록 끝
//     }  // 블록 끝
//     return num;  // 이 정거장에서 탄 사람 수
// }  // 블록 끝
//
// int solution(int seat, vector<vector<string>> passengers) {  // [PCCE 기출문제] 7번 / 버스 풀이 시작
//     int num_passenger = 0;  // 현재 버스에 타고 있는 승객 수
//     for(int i=0; i<passengers.size(); i++){  // 정거장 순서대로 승하차 인원 반영
//         num_passenger += func4(passengers[i]);  // 승차 인원을 세는 func4를 호출해 현재 승객 수에 더하기
//         num_passenger -= func3(passengers[i]);  // 하차 인원을 세는 func3를 호출해 현재 승객 수에서 빼기
//     }  // 블록 끝
//     int answer = func1(seat - num_passenger);  // 남은 좌석 수를 계산하고 음수이면 func1로 0을 반환
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 정거장별 On과 Off의 개수를 더하고 빼기. 좌석 수에서 승객 수를 뺀 값이 음수이면 0으로 바꾸기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:29:19
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_340201_%5BPCCE_%EA%B8%B0%EC%B6%9C%EB%AC%B8%EC%A0%9C%5D_7%EB%B2%88___%EB%B2%84%EC%8A%A4/README.md)
