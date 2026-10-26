#include <iostream> // 표준 입출력
#include <string> // 줄 전체 문자열 저장
using namespace std; // 표준 이름 접두사 생략
int main() { // 실행 시작점
    string text; getline(cin, text); // 공백을 포함한 한 줄 읽기
    text.push_back('\0'); // 마지막 숫자 뒤 검사에 쓸 끝 표시 추가
    int position = 0, count = 0; long long total = 0; // 위치·개수·합 초기화
    while (true) { // 정수 토큰을 하나씩 처리
        while (text[position] == ' ') ++position; // 앞 공백 건너뛰기
        int sign = 1, number = 0; // 부호와 현재 값 준비
        if (text[position] == '+' || text[position] == '-') { // 선택적 부호 확인
            if (text[position] == '-') sign = -1; // 음수 부호 저장
            ++position; // 숫자가 시작되는 위치로 이동
        } // 부호 처리 끝
        while ('0' <= text[position] && text[position] <= '9') { // 연속된 숫자 순회
            number = number * 10 + text[position] - '0'; ++position; // 자리값을 누적하며 위치 전진
        } // 한 정수의 숫자 읽기 끝
        total += sign * number; ++count; // 합과 토큰 개수 갱신
        while (text[position] == ' ') ++position; // 뒤 공백 건너뛰기
        if (text[position] != ',') break; // 구분자가 없으면 줄 해석 종료
        ++position; // 다음 정수로 이동
    } // 모든 토큰 처리 끝
    cout << count << ' ' << total << '\n'; // 개수와 합 출력
    return 0; // 정상 종료
} // 제한된 콤마 문법 파싱 끝
