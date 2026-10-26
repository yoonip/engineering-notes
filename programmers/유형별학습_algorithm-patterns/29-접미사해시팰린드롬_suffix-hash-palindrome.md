# 접미사 색인·문자열 해시·팰린드롬 반지름

[학습목차](README.md) · [연습문제](연습문제_problem-index.md)

## 문제의 구분과 중요성

텍스트 하나를 반복 질의하려면 접미사 구조로 본문을 색인하는 방법을 검토합니다.
부분 문자열의 같은지 여부를 빠르게 비교하려면 접두 해시가 편리하지만 충돌 조건을 확인합니다.
모든 중심의 회문 길이가 필요하면 팰린드롬 전용 알고리즘이 더 직접적입니다.
연속한 부분 문자열, 건너뛰기가 가능한 부분 수열, 문자열의 끝까지 이어지는 접미사를 구분합니다.
이 문서의 작은 문자열과 수치 계산은 직접 구성한 예제입니다.

## 접미사 배열과 LCP

접미사 배열 SA는 모든 접미사의 시작 위치를 사전순으로 나열한 배열입니다.
banana의 SA는 [5,3,1,0,4,2]이며 접미사는 a,ana,anana,banana,na,nana 순서입니다.
LCP는 사전순으로 인접한 두 접미사의 가장 긴 공통 접두사 길이입니다.
이 예제의 인접 LCP 배열은 [1,3,0,0,2]입니다.
패턴으로 시작하는 접미사들은 사전순에서 연속한 구간을 이루므로 이분 탐색으로 찾습니다.
단순한 비교에서는 패턴 길이 m의 비교가 필요해 질의 O(m log n) 시간입니다.
추가 LCP 정보를 쓰는 탐색의 복잡도와 구분합니다. [Stanford 접미사·LCP 강의](https://web.stanford.edu/class/archive/cs/cs166/cs166.1216/)

직접 접미사 문자열을 모두 복사해 정렬하면 총 길이가 O(n²)이므로 효율적인 구축이 아닙니다.
두 배 길이의 순위 쌍을 비교하는 구축은 비교 정렬을 매 단계 쓰면 O(n log²n) 시간입니다.
정수 순위의 계수 정렬을 사용하면 O(n log n) 시간, O(n) 보조 공간으로 구현할 수 있습니다.
정수 알파벳을 이용하는 다른 선형 구축도 있으며, ACL은 오버로드별로 조건과 복잡도가 다릅니다.
주어진 SA에서 LCP는 앞서 일치한 길이를 재활용해 O(n) 시간에 계산합니다. [ACL 문자열 공식 문서](https://atcoder.github.io/ac-library/production/document_en/string.html)

서로 다른 부분 문자열 수는 n(n+1)/2−ΣLCP입니다.
사전순으로 새 접미사를 더할 때 이전 접미사와 공유한 앞부분 길이만큼 중복되기 때문입니다.
banana는 21−(1+3+0+0+2)=15개입니다.
두 접미사의 공통 접두 길이는 SA 순위 사이 LCP의 최솟값이므로 구간 최솟값 구조와 연결합니다.

## 접미사 자동자: 끝 위치 집합의 압축

접미사 자동자(SAM)는 부분 문자열의 같은 끝 위치 집합을 상태로 묶는 구조입니다.
루트부터 문자를 따라간 경로는 본문의 부분 문자열을 나타냅니다.
접미사만 인식하려면 별도의 종료 상태 표시가 필요하며, 모든 경로와 종료 경로의 뜻을 구별합니다.
각 상태에는 나타내는 최대 길이 len과 더 짧은 끝 위치 상태로 가는 suffix link를 저장합니다.
문자 하나를 덧붙일 때 기존 상태를 그대로 합칠 수 없으면 clone 상태로 길이 범위를 분리합니다.
문자열 길이에 선형인 상태·간선 수로 구성할 수 있다는 결과가 이 압축의 근거입니다. [Blumer 등의 원논문](https://www.sciencedirect.com/science/article/pii/0304397585901574)

aba에서는 끝 위치가 같은 b와 ab를 한 상태로, ba와 aba를 다른 한 상태로 묶습니다.
루트 외 각 상태가 새로 나타내는 길이 수는 len[v]−len[link[v]]입니다.
이 예제에서는 a가 1개, b·ab가 2개, ba·aba가 2개를 담당해 서로 다른 부분 문자열은 5개입니다.
구축은 고정 알파벳 O(n) 시간·공간이며, 균형 트리 전이는 O(n log σ) 시간을 고려합니다.
구현이 복잡하므로 정적 패턴 탐색만 필요하다면 SA나 [KMP](28-트라이와문자열매칭_trie-kmp-aho.md)로 충분한지 먼저 확인합니다.

## 접두 해시와 충돌

문자를 정수로 바꾸고 H[i+1]=(H[i]B+s[i]) mod p로 접두 해시를 만듭니다.
H[l:r]=(H[r]−H[l]B^(r-l)) mod p이면 길이가 같은 부분 문자열의 해시를 O(1)에 비교합니다.
전처리는 O(n) 시간·공간이며, 이 시간은 고정 폭 모듈러 연산을 가정합니다.
다른 문자열이 같은 나머지가 되는 충돌이 있으므로 해시 일치가 곧 문자열 동일성의 증명은 아닙니다.
직접 구성한 a=1,b=2,c=3, B=5,p=7에서 aa는 6, bc는 13 mod 7=6으로 충돌합니다.
해시가 다르면 반드시 다른 문자열이지만 같으면 별도 검증이나 확률적 보장이 필요합니다. [CMU 지문 해시 강의](https://www.cs.cmu.edu/~15451-s25/notes/lecture05.pdf)

무작위 기저나 모듈러를 선택한 모델에서 충돌 확률을 분석하며, 고정 상수에 보편적인 1/p 보장을 붙이지 않습니다.
여러 비교의 전체 실패 확률은 비교 횟수도 고려해야 합니다.
독립적인 두 해시는 위험을 줄이지만 충돌을 없애지는 않습니다.
해시가 같을 때 원문까지 비교하면 정확성은 확보하지만 반복 비교의 최악 시간은 커질 수 있습니다.
이 해시는 변경에 민감한 문자열 비교 도구이며 암호학적 무결성 해시의 보안 보장을 대신하지 않습니다.

## Manacher 알고리즘과 회문 반지름

회문은 앞뒤로 읽은 문자열이 같은 연속 구간입니다.
홀수 중심 반지름 d[i]를 중심 문자까지 포함해 정의하면 길이는 2d[i]−1입니다.
짝수 중심은 두 문자 사이에 있으므로 별도 배열과 경계 정의가 필요합니다.
직접 구성한 abacaba의 홀수 반지름은 [1,2,1,4,1,2,1]입니다.
중심 c의 반지름 4는 전체 길이 7을 나타냅니다.

가장 오른쪽까지 도달한 회문의 범위 [L,R]를 유지합니다.
그 안의 새 중심 i는 거울 중심 L+R−i의 반지름을 경계 안에서 재사용합니다.
시작 반지름을 min(거울 반지름,R−i+1)로 정한 뒤 경계 밖 문자만 더 비교합니다.
성공한 추가 확장은 오른쪽 경계를 앞으로 이동시키므로 전체 확장 횟수는 O(n)입니다.
홀수·짝수 두 배열을 합쳐 시간 O(n), 공간 O(n)이며, 회문 구간을 모두 출력하는 비용은 별도입니다. [Crochemore·Rytter 원저자 교재 8장](https://igm.univ-mlv.fr/~mac/REC/text-algorithms.pdf)
회문은 O(n²)개일 수 있지만 중심별 최대 반지름은 O(n)개로 압축됩니다.

## 구현·활용·반례

C·C++의 모듈러 곱은 곱셈 전에 자료형을 넓히고, 음수 나머지를 [0,p)로 정규화합니다.
Python의 문자열 슬라이스는 길이에 비례해 복사하므로 해시 비교 전에 매번 s[l:r]를 만들지 않습니다.
UTF-8 바이트·코드 포인트·사용자에게 보이는 글자 중 무엇을 색인하는지 정합니다.
본문 검색 색인과 중복 구간 분석에 연결되지만, 수정이 잦은 본문에 정적 SA를 그대로 쓰면 재구축 비용이 생깁니다.
LCS라는 약자가 공통 접두사 LCP와 혼동되지 않도록 정의를 먼저 확인합니다.
해시 기반 이분 탐색은 충돌이 판정의 단조성까지 흐릴 수 있으므로 정확성 요구를 먼저 정합니다.
[구간 질의](26-구간질의와지연전파_range-queries.md)와 [확률적 알고리즘](36-무작위화와근사최적화_randomized-approximation.md)을 함께 복습합니다.

## 복습 질문과 답

- 질문: 접미사 배열에서 같은 패턴으로 시작하는 접미사는 왜 모여 있습니까? 답: 사전순 비교에서 같은 접두사를 가진 문자열 사이에 그 접두사가 없는 문자열이 끼어들 수 없기 때문입니다.
- 질문: 회문 반지름을 모두 알면 회문을 모두 출력하는 데도 O(n)입니까? 답: 압축 표현만 O(n)이며 실제 출력할 구간 수는 O(n²)일 수 있습니다.
- 질문: 이중 해시는 충돌이 없습니까? 답: 충돌 위험을 줄이는 방법이며 결정적인 무충돌 보장은 아닙니다.

<!-- multilang-examples:start -->
## C·C++·Python으로 같은 예제 실행

거울 중심의 반지름을 재사용하여 가장 긴 회문 길이와 모든 회문 발생 수를 구합니다.

이 예제에서 직접 구현하는 기법은 Manacher 홀수 반지름 · Manacher 짝수 반지름 · 반지름 합으로 발생 수 집계입니다. 같은 표준 입력에서 세 언어가 같은 결과를 출력합니다.

### 입력과 출력

소문자 a..z 문자열 한 개이며 길이는 1..100입니다.

```text
abacaba
```

MAX 최장길이, COUNT 회문발생수를 각각 한 줄에 출력합니다. 같은 내용도 위치가 다르면 별개입니다.

```text
MAX 7
COUNT 12
```

### 입력부터 결과까지

| 단계 | 중간 상태 | 수행 이유 |
| --- | --- | --- |
| 1 | abacaba, 홀수 반지름 초기값1 | 각 문자 하나도 회문입니다. |
| 2 | 가운데 c의 반지름4, 경계[0,6] | 왼쪽과 오른쪽의 문자를 확장하여 전체 길이7을 확인합니다. |
| 3 | 홀수 반지름 [1,2,1,4,1,2,1] | 거울 중심과 오른쪽 경계를 이용해 중복 비교를 줄입니다. |
| 4 | 홀수 합12, 짝수 합0, 최장7 | 각 중심에서 가능한 회문 수가 그 반지름이므로 합산합니다. |

### C 예제

[실행 가능한 C 파일](<예제_examples/29-접미사해시팰린드롬_suffix-hash-palindrome/example.c>)

```c
#include <stdio.h>  // 문자열 입력과 결과 출력
#include <string.h>  // 입력 문자열 길이

int minimum(int a, int b) { return a < b ? a : b; }  // 거울 반지름과 경계의 작은 값
int main(void) {  // 회문 반지름 계산 시작
    char text[101]; int odd[100], even[100];  // 문자열과 두 종류의 중심
    scanf("%100s", text);  // 빈 문자열은 입력 범위에서 제외
    int n = (int)strlen(text), left = 0, right = -1, best = 0, total = 0;  // 현재 경계와 결과
    for (int i = 0; i < n; ++i) {  // 문자 위의 홀수 중심
        int radius = i > right ? 1 : minimum(odd[left + right - i], right - i + 1);  // 검증된 거울 범위
        while (i - radius >= 0 && i + radius < n && text[i - radius] == text[i + radius]) ++radius;  // 경계 밖 일치 확장
        odd[i] = radius; total += radius;  // 중심별 회문 수 누적
        if (2 * radius - 1 > best) best = 2 * radius - 1;  // 홀수 최장 길이
        if (i + radius - 1 > right) { left = i - radius + 1; right = i + radius - 1; }  // 가장 먼 경계 갱신
    }  // 홀수 중심 처리 끝
    left = 0; right = -1;  // 짝수 중심의 독립 경계
    for (int i = 0; i < n; ++i) {  // i의 바로 앞을 짝수 중심으로 사용
        int radius = i > right ? 0 : minimum(even[left + right - i + 1], right - i + 1);  // 짝수 거울 중심
        while (i - radius - 1 >= 0 && i + radius < n && text[i - radius - 1] == text[i + radius]) ++radius;  // 두 문자씩 확장
        even[i] = radius; total += radius;  // 짝수 회문 발생 수 누적
        if (2 * radius > best) best = 2 * radius;  // 짝수 최장 길이
        if (i + radius - 1 > right) { left = i - radius; right = i + radius - 1; }  // 짝수 회문의 먼 경계
    }  // 짝수 중심 처리 끝
    printf("MAX %d\nCOUNT %d\n", best, total);  // 길이와 위치별 발생 수
    return 0;  // 정상 종료
}  // 프로그램 끝
```

### C++ 예제

[실행 가능한 C++ 파일](<예제_examples/29-접미사해시팰린드롬_suffix-hash-palindrome/example.cpp>)

```cpp
#include <iostream>  // 문자열 토큰의 스트림 입출력
#include <cstring>  // 문자 배열 길이 계산

int minimum(int a, int b) { return a < b ? a : b; }  // 거울 반지름과 경계의 작은 값
int main() {  // 회문 반지름 계산 시작
    char text[101]; int odd[100], even[100];  // 문자열과 두 종류의 중심
    std::cin >> text;  // 빈 문자열은 입력 범위에서 제외
    int n = (int)std::strlen(text), left = 0, right = -1, best = 0, total = 0;  // 현재 경계와 결과
    for (int i = 0; i < n; ++i) {  // 문자 위의 홀수 중심
        int radius = i > right ? 1 : minimum(odd[left + right - i], right - i + 1);  // 검증된 거울 범위
        while (i - radius >= 0 && i + radius < n && text[i - radius] == text[i + radius]) ++radius;  // 경계 밖 일치 확장
        odd[i] = radius; total += radius;  // 중심별 회문 수 누적
        if (2 * radius - 1 > best) best = 2 * radius - 1;  // 홀수 최장 길이
        if (i + radius - 1 > right) { left = i - radius + 1; right = i + radius - 1; }  // 가장 먼 경계 갱신
    }  // 홀수 중심 처리 끝
    left = 0; right = -1;  // 짝수 중심의 독립 경계
    for (int i = 0; i < n; ++i) {  // i의 바로 앞을 짝수 중심으로 사용
        int radius = i > right ? 0 : minimum(even[left + right - i + 1], right - i + 1);  // 짝수 거울 중심
        while (i - radius - 1 >= 0 && i + radius < n && text[i - radius - 1] == text[i + radius]) ++radius;  // 두 문자씩 확장
        even[i] = radius; total += radius;  // 짝수 회문 발생 수 누적
        if (2 * radius > best) best = 2 * radius;  // 짝수 최장 길이
        if (i + radius - 1 > right) { left = i - radius; right = i + radius - 1; }  // 짝수 회문의 먼 경계
    }  // 짝수 중심 처리 끝
    std::cout << "MAX " << best << "\nCOUNT " << total << "\n";  // 길이와 위치별 발생 수
    return 0;  // 정상 종료
}  // 프로그램 끝
```

### Python 예제

[실행 가능한 Python 파일](<예제_examples/29-접미사해시팰린드롬_suffix-hash-palindrome/example.py>)

```python
import sys  # 문자열 토큰 읽기
text = sys.stdin.read().split()[0]  # 허용 범위의 비어 있지 않은 문자열
n = len(text)  # 문자 수
odd, even = [0] * n, [0] * n  # 홀수와 짝수 중심 반지름
left, right, best, total = 0, -1, 0, 0  # 가장 먼 회문 경계와 결과
for i in range(n):  # 홀수 중심 순회
    radius = 1 if i > right else min(odd[left + right - i], right - i + 1)  # 거울 범위 재사용
    while i - radius >= 0 and i + radius < n and text[i - radius] == text[i + radius]:  # 새 대칭 문자 비교
        radius += 1  # 회문 확장
    odd[i] = radius  # 해당 중심 반지름
    total += radius  # 중심별 발생 수
    best = max(best, 2 * radius - 1)  # 홀수 최장 길이
    if i + radius - 1 > right:  # 더 먼 오른쪽 경계 발견
        left, right = i - radius + 1, i + radius - 1  # 검증 구간 갱신
left, right = 0, -1  # 짝수 중심 경계 초기화
for i in range(n):  # 두 문자 사이의 중심 순회
    radius = 0 if i > right else min(even[left + right - i + 1], right - i + 1)  # 짝수 거울 범위
    while i - radius - 1 >= 0 and i + radius < n and text[i - radius - 1] == text[i + radius]:  # 대칭 문자 확장
        radius += 1  # 짝수 반지름 증가
    even[i] = radius  # 짝수 중심 상태 저장
    total += radius  # 해당 중심의 회문 수
    best = max(best, 2 * radius)  # 짝수 최장 길이
    if i + radius - 1 > right:  # 기존 경계를 넘는 회문
        left, right = i - radius, i + radius - 1  # 짝수 경계 갱신
print("MAX", best)  # 가장 긴 길이
print("COUNT", total)  # 위치를 구별한 전체 회문 수
```

### 언어별 차이

| 비교할 점 | C | C++ | Python |
| --- | --- | --- | --- |
| 표준 입출력 | scanf와 printf의 서식 지정자를 자료형에 맞춥니다. | std::cin과 std::cout으로 같은 토큰과 결과를 처리합니다. | sys.stdin.read().split()으로 읽은 토큰을 필요한 자료형으로 바꿉니다. |
| 배열과 허용 범위 | 문자열101칸과 홀수·짝수 반지름 각100칸의 고정 배열입니다. | 같은 상한의 고정 배열을 사용하며 입력 범위를 지킵니다. | 상태 길이에 맞춰 리스트를 만들지만 입력의 허용 범위는 같습니다. |
| 정수 연산 | 이 예제의 입력 상한에서 int 또는 long long의 연산 범위를 지킵니다. | C와 같은 정수 상한을 사용하며 중간 계산의 자료형을 확인합니다. | 정수는 임의 정밀도이지만 같은 입력 상한에서 같은 계산을 수행합니다. |

### 예제의 비용과 실행 파일

- 시간: O(n)
- 보조 공간: O(n)

오른쪽 경계 안은 거울 반지름을 재사용하고 추가 확장은 경계를 앞으로 이동시킵니다.

[예제 입력](<예제_examples/29-접미사해시팰린드롬_suffix-hash-palindrome/input.txt>) · [예상 출력](<예제_examples/29-접미사해시팰린드롬_suffix-hash-palindrome/output.txt>) · [예제 실행 방법](<예제_examples/29-접미사해시팰린드롬_suffix-hash-palindrome/README.md>) · [세 언어 확인 기록](<예제_examples/확인기록_validation.md>)
<!-- multilang-examples:end -->

## 보관 풀이와 연결

다음은 이 유형을 사용하는 대표 보관 풀이입니다. 레벨 순서는 학습 난이도의 절대 기준이 아니며, 보조 기법으로 연결된 문제도 포함합니다.

| 레벨 | 문제 | C | C++ | Python |
| ---: | --- | --- | --- | --- |
| 3 | 12904 가장 긴 팰린드롬 | [C](<../C/level3/082_12904_가장_긴_팰린드롬/README.md>) | [C++](<../C++/level3/082_12904_가장_긴_팰린드롬/README.md>) | [Python](<../Python/level3/082_12904_가장_긴_팰린드롬/README.md>) |

[이 유형의 보관 문제 전체](<분류별문제_problems-by-type/advanced-string.md>)에서 나머지 문제와 함께 쓰는 기법을 확인할 수 있습니다.
