#include <iostream>  // C++ 스트림 입력과 출력

typedef struct { long long x, y; } Point;  // 정수 평면 좌표
long long cross(Point a, Point b, Point c) {  // AB와 AC의 부호 있는 외적
    return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x);  // 방향과 넓이 두 배
}  // 외적 계산 끝
int orientation(Point a, Point b, Point c) {  // 외적을 작은 부호로 변환
    long long value = cross(a, b, c);  // 넓은 자료형의 중간 곱
    return (value > 0) - (value < 0);  // 왼쪽1, 일직선0, 오른쪽-1
}  // 방향 판정 끝
int between(long long a, long long x, long long b) {  // 순서와 무관한 닫힌 구간 포함
    return (a <= x && x <= b) || (b <= x && x <= a);  // 양끝 사이인지 확인
}  // 좌표 포함 검사 끝
int on_segment(Point a, Point b, Point p) {  // 점이 실제 선분 위인지 확인
    return orientation(a, b, p) == 0 && between(a.x, p.x, b.x) && between(a.y, p.y, b.y);  // 일직선과 경계 상자
}  // 선분 포함 검사 끝
int intersects(Point a, Point b, Point c, Point d) {  // 닫힌 두 선분 교차
    int first = orientation(a, b, c), second = orientation(a, b, d);  // AB에 대한 양끝 방향
    int third = orientation(c, d, a), fourth = orientation(c, d, b);  // CD에 대한 양끝 방향
    if (first * second < 0 && third * fourth < 0) return 1;  // 작은 부호의 곱으로 엄격 교차
    return on_segment(a, b, c) || on_segment(a, b, d) || on_segment(c, d, a) || on_segment(c, d, b);  // 일직선과 끝점 예외
}  // 교차 판정 끝
int main() {  // 네 점 입력 처리
    Point points[4];  // 두 선분의 끝점
    for (int i = 0; i < 4; ++i) std::cin >> points[i].x >> points[i].y;  // A,B,C,D 좌표 읽기
    int sign = orientation(points[0], points[1], points[2]);  // 첫 세 점의 방향
    int result = intersects(points[0], points[1], points[2], points[3]);  // 선분 교차
    std::cout << sign << " " << (result ? "YES" : "NO") << "\n";  // 방향과 교차 여부
    return 0;  // 정상 종료
}  // 프로그램 끝
