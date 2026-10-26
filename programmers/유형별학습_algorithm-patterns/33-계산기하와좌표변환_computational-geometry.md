# 계산기하의 방향 판정과 좌표 변환

[학습목차](README.md) · [연습문제](연습문제_problem-index.md)

## 핵심 원리와 중요성

계산기하는 점·선분·다각형의 관계를 수치 판정으로 바꾸는 분야입니다.
그림으로는 분명한 왼쪽·오른쪽·경계 위의 구분도 구현에서는 오버플로와 반올림에 영향을 받습니다.
거리부터 계산하기보다 방향·정렬·포함 관계로 문제를 바꾸면 제곱근과 나눗셈을 줄일 수 있습니다.
기하 라이브러리도 방향 같은 판정과 새 교점 좌표를 만드는 구성을 구분합니다. [CGAL 판정과 구성 설명](https://doc.cgal.org/Manual/3.1/doc_html/cgal_manual/Kernel_d/Chapter_predicates_constructions_d.html)
이 문서의 좌표와 계산 예제는 직접 구성한 예제입니다.

## 방향을 나타내는 외적

평면 벡터 u=(ux,uy), v=(vx,vy)의 외적은 ux×vy−uy×vx인 스칼라입니다.
세 점 A,B,C에는 cross(B−A,C−A)를 사용합니다.
양수는 A→B에서 C가 왼쪽, 음수는 오른쪽, 0은 세 점이 한 직선 위라는 뜻입니다.
이는 삼각형의 부호 있는 넓이의 두 배이기도 합니다.
기울기를 나누어 비교하지 않으므로 수직선도 같은 식으로 처리합니다.

```python
def orientation(a, b, c):  # 세 점의 정수 좌표를 받아 방향의 부호 계산
    value = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])  # 두 차 벡터의 외적
    return (value > 0) - (value < 0)  # 왼쪽 1, 일직선 0, 오른쪽 -1 반환
```

A=(0,0), B=(4,0), C=(1,2)에서 외적은 4×2−0×1=8입니다.
C는 A→B의 왼쪽이며 삼각형 넓이는 4입니다.
C=(6,0)이면 외적은 0이지만 C는 선분 AB 밖이므로 일직선과 선분 포함을 구별합니다.

## 선분 교차의 절차와 경계

선분 AB와 CD가 각 직선의 엄격히 반대쪽에 있으면 내부에서 교차합니다.
orientation(A,B,C), orientation(A,B,D)의 부호가 반대이고 반대 선분에서도 같은 조건인지 확인합니다.
한 방향 값이 0이면 해당 점이 다른 선분의 x·y 경계 상자 안에 있는지 함께 확인합니다.
네 방향 값이 모두 0이면 일직선이므로 두 포함 구간이 겹치는지 비교합니다.
끝점 접촉도 교차로 셀지, 내부 교차만 셀지를 문제에서 먼저 정합니다.
길이 0인 선분도 허용되면 점 포함 조건으로 처리합니다.
고정 폭 정수 연산 기준 선분 쌍 하나의 판정은 O(1) 시간·공간입니다.
모든 쌍을 확인하면 O(n²)이므로 선분 수가 크면 스위프 등 별도 방법이 필요합니다.

## 볼록 껍질과 정렬 후 스택

볼록 껍질은 모든 점을 포함하는 가장 작은 볼록 집합의 경계입니다.
단조 체인 방법은 점을 (x,y)순으로 정렬한 뒤 아래·위 껍질을 각각 만듭니다.
새 점을 붙여 오른쪽으로 꺾이면 가운데 점을 제거해 왼쪽 회전 불변식을 유지합니다.
외적이 0인 일직선 점도 제거할지는 경계 점 전체를 출력할지에 따라 정합니다.
직접 구성한 점 {(0,0),(2,0),(2,2),(0,2),(1,1)}에서는 가운데 (1,1)이 최종 껍질에서 제외됩니다.
새 점 때문에 꺾임이 생길 때 중간 점은 새 경계의 내부에 들어가므로 끝 경계 후보에서 지워도 됩니다.
각 점은 스택에 한 번 들어가고 한 번 나와 구축 순회는 O(n), 정렬 포함 O(n log n) 시간·O(n) 공간입니다.
방향 판정만 필요한 구축에는 정확한 판정을 제공하는 커널을 선택할 수 있습니다. [CGAL 볼록 껍질 예제](https://doc.cgal.org/latest/Manual/tutorial_hello_world.html)

## 다각형 넓이와 부호

경계순 점 p0…p_(n-1)의 부호 있는 넓이 두 배는 Σ cross(p_i,p_(i+1))이며 마지막은 p0로 연결합니다.
직접 구성한 (0,0),(3,0),(3,2),(0,2)는 합이 12이므로 넓이 6입니다.
점 순서를 반대로 하면 부호만 바뀌므로 실제 넓이는 절댓값을 취합니다.
자기 교차 다각형에는 이 식이 부호 있는 대수적 넓이를 계산하므로 단순한 내부 넓이로 해석하지 않습니다.
정수 좌표에서는 넓이의 두 배를 정수로 유지하면 .5 단위까지 정확히 표현할 수 있습니다.

## 맨해튼 거리의 좌표 변환

U=X+Y, V=X−Y로 놓으면 max(|ΔU|,|ΔV|)=|ΔX|+|ΔY|입니다.
두 차이의 부호가 같으면 합의 절댓값이, 다르면 차의 절댓값이 두 절댓값의 합이 되기 때문입니다.
맨해튼 거리 d 이하의 마름모는 U,V에서 축에 평행한 사각형이 됩니다.
중심 (2,1), 반경 2는 U중심 3,V중심 1이므로 U∈[1,5],V∈[−1,3]입니다.
원래 좌표는 X=(U+V)/2, Y=(U−V)/2로 복원합니다.
정수 X,Y만 허용하면 U와 V의 홀짝이 같아야 합니다.
예를 들어 U=2,V=1은 변환 사각형 안이어도 X=1.5,Y=0.5라 정수 격자점이 아닙니다.
사각형 안의 모든 정수 U,V를 단순히 세는 것은 원래 정수점 개수와 다릅니다.
원래 격자 경계도 변환해서 별도로 교차해야 하며, 변환 사각형만 세지 않습니다.
이 좌표 변환과 [스위프](27-오프라인질의와스위프_offline-sweep.md)를 결합하면 많은 거리 영역의 합집합·개수를 다룰 수 있습니다.

## 수치 오차와 자료형

좌표 차이 두 개의 곱이 원래 좌표 범위의 제곱 크기까지 커집니다.
C·C++에서는 뺄셈과 곱셈 전에 충분히 넓은 자료형으로 옮기며, 가능한 값의 상한을 직접 계산합니다.
부호만 필요할 때 두 큰 외적을 다시 곱해 음수인지 확인하면 추가 오버플로가 생길 수 있습니다.
Python 정수는 정확하지만 큰 정수의 곱셈이 상수 시간인 것은 아닙니다.
부동소수점에 임의의 작은 ε를 더하는 방식은 좌표 스케일과 오차 모델을 고려해야 합니다.
ε를 넣은 비교가 추이성을 깨면 정렬 비교 함수로 사용할 수 없습니다.
정확한 방향 판정과 근사 교점 좌표는 보장이 다릅니다. [CGAL 정확 계산 원칙](https://www.cgal.org/documentation.html)

## 실전 연결과 연계 유형

도형 충돌, 지도 경계, 배치 영역 분석에서 같은 판정을 사용합니다.
지구 표면의 위·경도에는 평면 유클리드 좌표 공식을 그대로 적용하지 않으며 투영·거리 모델을 정합니다.
측정 좌표의 불확실성과 계산 반올림 오차도 다른 원인이므로 구별합니다.
회전하는 캘리퍼스 같은 후속 방법은 볼록성 조건을 사용하므로 임의 다각형에 바로 적용하지 않습니다.
[구간 질의](26-구간질의와지연전파_range-queries.md), [정수 나머지와 홀짝](30-정수론과모듈러연산_number-theory.md)과 연결합니다.

## 복습 질문과 답

- 질문: 외적 0이면 점이 선분 위입니까? 답: 같은 직선 위라는 뜻이며 선분의 경계 상자 포함 여부도 확인해야 합니다.
- 질문: U,V 사각형의 모든 정수점이 원래 정수점입니까? 답: 두 좌표의 홀짝이 같아야 정수 X,Y로 복원됩니다.
- 질문: ε를 넣으면 정렬도 항상 안전합니까? 답: 비교의 추이성을 깨뜨릴 수 있으므로 오차 판정과 정렬 순서의 조건을 따로 검토해야 합니다.

<!-- multilang-examples:start -->
## C·C++·Python으로 같은 예제 실행

기울기 나눗셈 없이 외적의 부호와 경계 포함으로 두 선분의 교차를 판정합니다.

이 예제에서 직접 구현하는 기법은 정수 외적 방향 · 반대 부호 교차 · 일직선과 끝점 포함입니다. 같은 표준 입력에서 세 언어가 같은 결과를 출력합니다.

### 입력과 출력

A,B,C,D 순서의 네 점으로 각 줄 x,y입니다. 좌표는 -10000..10000의 정수이며 길이0 선분도 허용합니다.

```text
0 0
4 0
1 2
1 -1
```

orientation(A,B,C)의 부호 -1/0/1과 선분 AB,CD의 교차 YES/NO를 한 줄에 출력합니다. 끝점 접촉과 겹침도 교차입니다.

```text
1 YES
```

### 입력부터 결과까지

| 단계 | 중간 상태 | 수행 이유 |
| --- | --- | --- |
| 1 | A=(0,0),B=(4,0),C=(1,2),D=(1,−1) | 두 선분의 끝점을 같은 좌표계에 놓습니다. |
| 2 | cross(A,B,C)=8, cross(A,B,D)=−4 | C와 D는 AB 직선의 반대편입니다. |
| 3 | cross(C,D,A)=−3, cross(C,D,B)=9 | A와 B도 CD 직선의 반대편입니다. |
| 4 | orientation=1, intersection=YES | 네 방향의 부호로 내부 교차를 확정합니다. |

### C 예제

[실행 가능한 C 파일](<예제_examples/33-계산기하와좌표변환_computational-geometry/example.c>)

```c
#include <stdio.h>  // 표준 입력과 출력 함수

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
int main(void) {  // 네 점 입력 처리
    Point points[4];  // 두 선분의 끝점
    for (int i = 0; i < 4; ++i) scanf("%lld %lld", &points[i].x, &points[i].y);  // A,B,C,D 좌표 읽기
    int sign = orientation(points[0], points[1], points[2]);  // 첫 세 점의 방향
    int result = intersects(points[0], points[1], points[2], points[3]);  // 선분 교차
    printf("%d %s\n", sign, result ? "YES" : "NO");  // 방향과 교차 여부
    return 0;  // 정상 종료
}  // 프로그램 끝
```

### C++ 예제

[실행 가능한 C++ 파일](<예제_examples/33-계산기하와좌표변환_computational-geometry/example.cpp>)

```cpp
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
```

### Python 예제

[실행 가능한 Python 파일](<예제_examples/33-계산기하와좌표변환_computational-geometry/example.py>)

```python
import sys  # 네 점의 정수 토큰 읽기
tokens = iter(map(int, sys.stdin.read().split()))  # 좌표 입력 순회
points = [(next(tokens), next(tokens)) for _ in range(4)]  # A,B,C,D
def orientation(a, b, c):  # 외적의 방향 부호
    value = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])  # AB와 AC의 외적
    return (value > 0) - (value < 0)  # 세 가지 방향
def between(a, x, b):  # 닫힌 좌표 범위
    return min(a, b) <= x <= max(a, b)  # 끝점 순서와 무관한 포함
def on_segment(a, b, p):  # 직선과 선분 구분
    return orientation(a, b, p) == 0 and between(a[0], p[0], b[0]) and between(a[1], p[1], b[1])  # 일직선과 경계 포함
a, b, c, d = points  # 두 선분 이름
first, second = orientation(a, b, c), orientation(a, b, d)  # AB 양쪽 부호
third, fourth = orientation(c, d, a), orientation(c, d, b)  # CD 양쪽 부호
result = first * second < 0 and third * fourth < 0  # 엄격한 내부 교차
result = result or on_segment(a, b, c) or on_segment(a, b, d) or on_segment(c, d, a) or on_segment(c, d, b)  # 일직선과 끝점 교차
print(first, "YES" if result else "NO")  # 방향과 최종 판정
```

### 언어별 차이

| 비교할 점 | C | C++ | Python |
| --- | --- | --- | --- |
| 표준 입출력 | scanf와 printf의 서식 지정자를 자료형에 맞춥니다. | std::cin과 std::cout으로 같은 토큰과 결과를 처리합니다. | sys.stdin.read().split()으로 읽은 토큰을 필요한 자료형으로 바꿉니다. |
| 배열과 허용 범위 | 네 Point와 고정 개수의 정수만 사용합니다. | 같은 상한의 고정 배열을 사용하며 입력 범위를 지킵니다. | 상태 길이에 맞춰 리스트를 만들지만 입력의 허용 범위는 같습니다. |
| 정수 연산 | 이 예제의 입력 상한에서 int 또는 long long의 연산 범위를 지킵니다. | C와 같은 정수 상한을 사용하며 중간 계산의 자료형을 확인합니다. | 정수는 임의 정밀도이지만 같은 입력 상한에서 같은 계산을 수행합니다. |

### 예제의 비용과 실행 파일

- 시간: O(1) 정수 연산
- 보조 공간: O(1)

네 방향과 일직선 경계 검사를 고정 횟수 수행합니다.

[예제 입력](<예제_examples/33-계산기하와좌표변환_computational-geometry/input.txt>) · [예상 출력](<예제_examples/33-계산기하와좌표변환_computational-geometry/output.txt>) · [예제 실행 방법](<예제_examples/33-계산기하와좌표변환_computational-geometry/README.md>) · [세 언어 확인 기록](<예제_examples/확인기록_validation.md>)
<!-- multilang-examples:end -->

## 보관 풀이와 연결

다음은 이 유형을 사용하는 대표 보관 풀이입니다. 레벨 순서는 학습 난이도의 절대 기준이 아니며, 보조 기법으로 연결된 문제도 포함합니다.

| 레벨 | 문제 | C | C++ | Python |
| ---: | --- | --- | --- | --- |
| 0 | 120875 평행 | [C](<../C/level0/extra_120875_평행/README.md>) | [C++](<../C++/level0/extra_120875_평행/README.md>) | [Python](<../Python/level0/extra_120875_평행/README.md>) |
| 5 | 49190 방의 개수 | [C](<../C/level5/001_49190_방의_개수/README.md>) | [C++](<../C++/level5/001_49190_방의_개수/README.md>) | [Python](<../Python/level5/revisit_20261024/001_49190_방의_개수/README.md>) |
| 5 | 214295 미로 주행 테스트 | [C](<../C/level5/019_214295_미로_주행_테스트/README.md>) | [C++](<../C++/level5/019_214295_미로_주행_테스트/README.md>) | [Python 미완료](<../Python/level5/revisit_20261024/attempts/214295/README.md>) |
| 0 | 120876 겹치는 선분의 길이 | [C](<../C/level0/extra_120876_겹치는_선분의_길이/README.md>) | [C++](<../C++/level0/extra_120876_겹치는_선분의_길이/README.md>) | [Python](<../Python/level0/extra_120876_겹치는_선분의_길이/README.md>) |
| 1 | 161990 바탕화면 정리 | [C](<../C/level1/extra_161990_바탕화면_정리/README.md>) | [C++](<../C++/level1/extra_161990_바탕화면_정리/README.md>) | [Python](<../Python/level1/extra_161990_바탕화면_정리/README.md>) |

[이 유형의 보관 문제 전체](<분류별문제_problems-by-type/geometry.md>)에서 나머지 문제와 함께 쓰는 기법을 확인할 수 있습니다.
