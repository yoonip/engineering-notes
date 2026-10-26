# 트라이·KMP·아호 코라식의 문자열 상태

[학습목차](README.md) · [연습문제](연습문제_problem-index.md)

## 핵심 원리와 선택 기준

문자열 탐색은 이미 읽은 문자가 다음 비교에 주는 정보를 상태로 남기는 문제입니다.
트라이는 사전의 공통 접두사를 공유하고, KMP는 한 패턴의 접두·접미 관계를 사용합니다.
아호 코라식은 여러 패턴의 트라이에 실패 링크를 붙여 텍스트를 함께 탐색합니다.
패턴 하나인지, 사전의 접두사 질의인지, 여러 패턴의 모든 발생 위치인지부터 구분합니다.
총 패턴 길이를 P, 텍스트 길이를 T, 알파벳 크기를 σ, 실제 보고할 발생 수를 Z로 표기합니다.

## 트라이: 접두사를 경로로 보관

루트에서 문자 하나씩 이동하며 단어를 나타냅니다.
직접 구성한 사전 {a,ab,ac}에서는 루트→a 경로를 세 단어가 공유합니다.
a 노드는 단어의 끝이면서 b,c 자식을 가질 수 있으므로 리프 여부로 단어 끝을 판단하지 않습니다.
길이 L인 단어는 간선 조회 O(1)을 가정하면 삽입·완전 검색·접두사 확인에 O(L) 시간이 필요합니다.
고정 배열 자식 표현은 O(Pσ) 공간, 존재하는 간선만 저장하면 간선 수는 O(P)입니다.
해시맵 자식은 기대 O(1), 균형 트리 자식은 O(log σ) 조회이므로 실제 복잡도를 구별합니다.
사전 문자열 전체를 매번 비교하는 대신 공통 접두사 비교를 공유한다는 점이 중요합니다. [Helsinki 문자열 집합 강의](https://www.cs.helsinki.fi/juha.karkkainen/teach/14-15/SPA/all-lectures.pdf)

## KMP: 불일치 뒤 남는 정보

패턴 p의 π[i]는 p[0:i+1]의 진접두사이면서 접미사인 가장 긴 문자열의 길이입니다.
진접두사는 문자열 전체 자신을 제외한 접두사입니다.
q글자까지 일치한 뒤 불일치하면 이미 일치한 문자열의 접미사 중 패턴의 접두사인 부분만 계속 사용할 수 있습니다.
따라서 q를 π[q-1]로 줄이며 텍스트를 뒤로 되돌리지 않습니다.
표준 접두사 함수 구현은 패턴 전처리 O(P), 텍스트 탐색 O(T), 보조 공간 O(P)입니다.
Princeton 구현은 DFA 표를 만드는 변형이므로 전처리 O(Pσ)와 구별합니다. [Princeton KMP 구현 문서](https://algs4.cs.princeton.edu/code/javadoc/edu/princeton/cs/algs4/KMP.html)

## 직접 구성한 접두사와 불일치 추적

패턴 ababaca의 접두사 함수는 [0,0,1,2,3,0,1]입니다.
접두사 ababa까지 일치했는데 다음 텍스트 문자가 b라고 가정합니다.
패턴의 다음 문자 c와 다르므로 q=5에서 π[4]=3으로 줄입니다.
남기는 aba는 이미 읽은 ababa의 접미사이기도 하므로 다시 읽지 않아도 일치합니다.
이제 p[3]=b와 텍스트 b가 같아 q=4로 전진합니다.
텍스트를 뒤로 되돌리지 않은 채 무조건 q=0으로 초기화하면 겹치는 후보를 잃어 일치를 놓칠 수 있습니다.
패턴 ababaca, 텍스트 abababaca에서는 위의 실패 복구로 시작 위치 2의 일치를 이어 가지만 단순 초기화는 이 후보를 버립니다.
각 시작 위치를 한 칸씩 옮겨 처음부터 비교하는 올바른 단순 탐색은 별도 방법이며 최악 O(TP) 시간이 필요합니다.

```python
def prefix_function(pattern):  # 비어 있지 않아도 되고 빈 패턴이면 빈 표 반환
    pi = [0] * len(pattern)  # 각 접두사에 남길 가장 긴 경계 길이
    for i in range(1, len(pattern)):  # 새 문자를 하나씩 접두사에 추가
        j = pi[i - 1]  # 직전 접두사에서 이어 볼 후보 길이
        while j and pattern[i] != pattern[j]:  # 현재 경계 뒤에 붙일 수 없으면 축소
            j = pi[j - 1]  # 더 짧은 접두·접미 공통 부분으로 이동
        if pattern[i] == pattern[j]:  # 다음 문자가 같으면 경계를 한 문자 확장
            j += 1  # 새로 일치한 문자의 길이 반영
        pi[i] = j  # 현재 접두사의 경계 길이 저장
    return pi  # 검색 때 재사용할 접두사 표 반환
```

j는 증가할 때 한 칸만 늘어나고, while 반복마다 감소합니다.
전체 증가량이 O(P)이므로 총 감소 횟수도 O(P)인 상환 분석으로 선형 시간을 설명합니다.
패턴이 전부 일치한 뒤에도 q=π[q-1]로 이동하면 겹치는 발생을 찾을 수 있습니다.
빈 패턴의 발생 위치 정의는 문제마다 다르므로 검색 함수에서 별도로 정합니다.

## 아호 코라식: 여러 패턴의 실패 링크

실패 링크는 현재 경로 문자열의 가장 긴 진접미사 중 트라이에 존재하는 접두사 노드를 가리킵니다.
이는 KMP의 경계 길이를 여러 패턴의 접두사 상태로 확장한 것입니다. [Tufts 실패 링크 정의](https://www.cs.tufts.edu/comp/150GEN/classpages/AhoCorasick.html)
루트부터 BFS로 링크를 만들면 짧은 접두사의 실패 전이가 먼저 결정됩니다.
문자를 읽을 때 자식으로 갈 수 없으면 실패 링크를 따라가 다음 일치를 이어 갑니다.
패턴 종료 표시와 실패 경로의 종료 표시를 함께 처리해야 한 위치에서 여러 패턴을 보고합니다.

## 직접 구성한 여러 패턴 예제

패턴은 {he,she,hers}, 텍스트는 ushers입니다.
u 뒤에는 루트이고, s→sh→she를 읽으면 she가 끝납니다.
she의 실패 링크는 he 노드를 가리키므로 같은 위치에서 he도 끝납니다.
다음 r에서는 she에서 진행할 자식이 없지만 he로 옮기면 her로 진행합니다.
마지막 s에서 hers를 보고하여 전체 발생은 she, he, hers입니다.
실패 링크의 출력까지 처리하지 않으면 he를 놓칩니다.

고정 알파벳의 완성된 전이 표는 구축 O(Pσ), 탐색 O(T+Z), 공간 O(Pσ+패턴 수)입니다.
σ가 상수이면 구축·공간을 O(P)로 줄여 적지만, 큰 문자 집합에서는 이 가정을 명시합니다.
종료 목록을 모든 실패 자손에 통째로 복사하면 메모리가 늘 수 있으므로 출력 링크나 개수 누적을 사용합니다.
발생 위치를 전부 출력한다면 Z가 매우 클 수 있어 O(T)만으로 전체 작업을 끝낸다고 쓰지 않습니다. [원저자 다중 패턴 매칭 논문](https://doi.org/10.1145/360825.360855)

## 구현·실전 연결과 한계

C·C++의 char는 UTF-8 한글의 글자 하나와 같지 않으므로 바이트 검색인지 문자 검색인지 정합니다.
Python 문자열도 사람이 보는 결합 문자 단위와 코드 포인트가 항상 같지는 않습니다.
대소문자·유니코드 정규화 규칙을 바꾸면 탐색 인덱스의 의미도 바뀔 수 있습니다.
접두사 자동완성은 트라이, 고정 키워드의 다중 탐지는 아호 코라식과 연결합니다.
패턴 사전이 자주 바뀌면 실패 링크 재구축 비용까지 고려합니다.
본문을 미리 색인하고 다양한 질의를 받는 경우는 [접미사 구조](29-접미사해시팰린드롬_suffix-hash-palindrome.md)와 비교합니다.

## 복습 질문과 답

- 질문: 트라이에서 자식이 있는 노드는 단어 끝이 아닙니까? 답: a와 ab를 함께 저장하면 a는 자식과 종료 표시를 동시에 가집니다.
- 질문: KMP는 왜 텍스트 위치를 뒤로 옮기지 않습니까? 답: 이미 확인한 접미사와 패턴 접두사의 일치를 실패 표가 보존하기 때문입니다.
- 질문: 아호 코라식이 한 글자에서 두 패턴을 찾을 수 있습니까? 답: 현재 종료 노드와 실패·출력 링크의 종료 노드가 여러 패턴을 나타낼 수 있습니다.

<!-- multilang-examples:start -->
## C·C++·Python으로 같은 예제 실행

트라이에서 단어·접두사를 구분하고 KMP의 실패 복구로 겹치는 패턴 발생을 셉니다.

이 예제에서 직접 구현하는 기법은 고정 알파벳 트라이 · 단어 종료 표시 · KMP 접두사 함수 · 겹치는 발생 복구입니다. 같은 표준 입력에서 세 언어가 같은 결과를 출력합니다.

### 입력과 출력

n(0≤n≤10), 다음 n개 사전 단어, 질의 단어, 텍스트, 패턴 순서의 공백 토큰입니다. 소문자 a..z만 허용하며 단어·질의·패턴 길이1..20, 텍스트 길이1..100입니다.

```text
3
a
ab
ac
ab
abababaca
ababaca
```

WORD YES/NO, PREFIX YES/NO, MATCHES 발생수를 각각 한 줄에 출력합니다.

```text
WORD YES
PREFIX YES
MATCHES 1
```

### 입력부터 결과까지

| 단계 | 중간 상태 | 수행 이유 |
| --- | --- | --- |
| 1 | 사전 a,ab,ac의 a경로 공유 | 단어 a는 자식이 있어도 종료 표시를 유지합니다. |
| 2 | 질의 ab: 경로와 종료 표시 모두 존재 | WORD와 PREFIX가 모두 YES입니다. |
| 3 | ababaca의 pi=[0,0,1,2,3,0,1] | 불일치 때 남길 접두·접미 길이를 계산합니다. |
| 4 | abababaca의 위치5에서 q=5→3, 이후 위치2의 일치 완성 | 텍스트를 되돌리지 않고 겹친 후보를 이어 가 MATCHES 1입니다. |

### C 예제

[실행 가능한 C 파일](<예제_examples/28-트라이와문자열매칭_trie-kmp-aho/example.c>)

```c
#include <stdio.h>  // 문자열 입력과 결과 출력
#include <string.h>  // 문자열 길이 계산

int next_node[201][26], terminal[201], nodes = 1;  // 0번 루트와 아직 없는 간선 0
int main(void) {  // 트라이와 KMP 비교 시작
    int n; char word[21], query[21], text[101], pattern[21];  // 고정 문자열 상한
    scanf("%d", &n);  // 사전 단어 수
    for (int i = 0; i < n; ++i) {  // 단어를 하나씩 삽입
        scanf("%20s", word);  // 현재 사전 단어
        int node = 0;  // 트라이 루트
        for (int j = 0; word[j]; ++j) {  // 한 문자씩 접두사 확장
            int letter = word[j] - 'a';  // 26개 자식 번호
            if (!next_node[node][letter]) next_node[node][letter] = nodes++;  // 필요한 노드만 새로 생성
            node = next_node[node][letter];  // 다음 접두사로 이동
        }  // 단어 경로 처리 끝
        terminal[node] = 1;  // 자식 유무와 별개인 단어 종료 표시
    }  // 사전 구축 끝
    scanf("%20s %100s %20s", query, text, pattern);  // 트라이 질의와 검색 문자열
    int node = 0, exists = 1;  // 질의 경로 존재 여부
    for (int i = 0; query[i]; ++i) {  // 질의 접두사 확인
        int child = next_node[node][query[i] - 'a'];  // 다음 문자 간선
        if (!child) { exists = 0; break; }  // 없는 경로면 즉시 종료
        node = child;  // 이어지는 접두사 상태
    }  // 트라이 질의 끝
    int pi[20] = {0}, length = (int)strlen(pattern);  // 패턴 경계 길이
    for (int i = 1; i < length; ++i) {  // 접두사 함수를 선형으로 구축
        int j = pi[i - 1];  // 직전의 가장 긴 경계
        while (j > 0 && pattern[i] != pattern[j]) j = pi[j - 1];  // 더 짧은 경계로 복구
        if (pattern[i] == pattern[j]) ++j;  // 같은 문자는 경계를 확장
        pi[i] = j;  // 현재 접두사의 경계 기록
    }  // 패턴 전처리 끝
    int matched = 0, count = 0;  // 현재 일치 길이와 발생 수
    for (int i = 0; text[i]; ++i) {  // 텍스트는 앞으로만 이동
        while (matched > 0 && text[i] != pattern[matched]) matched = pi[matched - 1];  // 겹친 후보 보존
        if (text[i] == pattern[matched]) ++matched;  // 현재 일치 확장
        if (matched == length) { ++count; matched = pi[matched - 1]; }  // 발생 기록 뒤 겹치는 검색 유지
    }  // 텍스트 검색 끝
    printf("WORD %s\n", exists && terminal[node] ? "YES" : "NO");  // 완전 단어 여부
    printf("PREFIX %s\n", exists ? "YES" : "NO");  // 접두사 경로 여부
    printf("MATCHES %d\n", count);  // 겹침을 포함한 발생 수
    return 0;  // 정상 종료
}  // 프로그램 끝
```

### C++ 예제

[실행 가능한 C++ 파일](<예제_examples/28-트라이와문자열매칭_trie-kmp-aho/example.cpp>)

```cpp
#include <iostream>  // 문자 배열의 스트림 입출력
#include <cstring>  // 문자열 길이 계산

int next_node[201][26], terminal[201], nodes = 1;  // 0번 루트와 아직 없는 간선 0
int main() {  // 트라이와 KMP 비교 시작
    int n; char word[21], query[21], text[101], pattern[21];  // 고정 문자열 상한
    std::cin >> n;  // 사전 단어 수
    for (int i = 0; i < n; ++i) {  // 단어를 하나씩 삽입
        std::cin >> word;  // 현재 사전 단어
        int node = 0;  // 트라이 루트
        for (int j = 0; word[j]; ++j) {  // 한 문자씩 접두사 확장
            int letter = word[j] - 'a';  // 26개 자식 번호
            if (!next_node[node][letter]) next_node[node][letter] = nodes++;  // 필요한 노드만 새로 생성
            node = next_node[node][letter];  // 다음 접두사로 이동
        }  // 단어 경로 처리 끝
        terminal[node] = 1;  // 자식 유무와 별개인 단어 종료 표시
    }  // 사전 구축 끝
    std::cin >> query >> text >> pattern;  // 트라이 질의와 검색 문자열
    int node = 0, exists = 1;  // 질의 경로 존재 여부
    for (int i = 0; query[i]; ++i) {  // 질의 접두사 확인
        int child = next_node[node][query[i] - 'a'];  // 다음 문자 간선
        if (!child) { exists = 0; break; }  // 없는 경로면 즉시 종료
        node = child;  // 이어지는 접두사 상태
    }  // 트라이 질의 끝
    int pi[20] = {0}, length = (int)std::strlen(pattern);  // 패턴 경계 길이
    for (int i = 1; i < length; ++i) {  // 접두사 함수를 선형으로 구축
        int j = pi[i - 1];  // 직전의 가장 긴 경계
        while (j > 0 && pattern[i] != pattern[j]) j = pi[j - 1];  // 더 짧은 경계로 복구
        if (pattern[i] == pattern[j]) ++j;  // 같은 문자는 경계를 확장
        pi[i] = j;  // 현재 접두사의 경계 기록
    }  // 패턴 전처리 끝
    int matched = 0, count = 0;  // 현재 일치 길이와 발생 수
    for (int i = 0; text[i]; ++i) {  // 텍스트는 앞으로만 이동
        while (matched > 0 && text[i] != pattern[matched]) matched = pi[matched - 1];  // 겹친 후보 보존
        if (text[i] == pattern[matched]) ++matched;  // 현재 일치 확장
        if (matched == length) { ++count; matched = pi[matched - 1]; }  // 발생 기록 뒤 겹치는 검색 유지
    }  // 텍스트 검색 끝
    std::cout << "WORD " << (exists && terminal[node] ? "YES" : "NO") << "\n";  // 완전 단어 여부
    std::cout << "PREFIX " << (exists ? "YES" : "NO") << "\n";  // 접두사 경로 여부
    std::cout << "MATCHES " << count << "\n";  // 겹침을 포함한 발생 수
    return 0;  // 정상 종료
}  // 프로그램 끝
```

### Python 예제

[실행 가능한 Python 파일](<예제_examples/28-트라이와문자열매칭_trie-kmp-aho/example.py>)

```python
import sys  # 소문자 문자열 토큰 읽기
tokens = iter(sys.stdin.read().split())  # 공백 토큰 순회
n = int(next(tokens))  # 사전 크기
children = [[0] * 26]  # 0번 루트의 자식 표
terminal = [False]  # 각 접두사의 단어 종료 여부
for _ in range(n):  # 사전 삽입
    node = 0  # 루트에서 시작
    for character in next(tokens):  # 단어의 문자 순회
        letter = ord(character) - ord("a")  # 자식 번호
        if children[node][letter] == 0:  # 아직 없는 간선 확인
            children[node][letter] = len(children)  # 새 노드의 번호 연결
            children.append([0] * 26)  # 자식 표 생성
            terminal.append(False)  # 초기 종료 표시
        node = children[node][letter]  # 접두사 이동
    terminal[node] = True  # 단어 끝 보관
query, text, pattern = next(tokens), next(tokens), next(tokens)  # 두 탐색의 입력
node, exists = 0, True  # 질의 경로 초기 상태
for character in query:  # 트라이 접두사 확인
    child = children[node][ord(character) - ord("a")]  # 다음 문자 간선
    if child == 0:  # 경로가 없는 상태
        exists = False  # 접두사도 부재
        break  # 추가 탐색 중단
    node = child  # 접두사 이동
pi = [0] * len(pattern)  # 패턴의 접두·접미 경계 표
for i in range(1, len(pattern)):  # 경계를 한 문자씩 확장
    j = pi[i - 1]  # 직전 경계 길이
    while j and pattern[i] != pattern[j]:  # 경계 뒤 문자가 불일치
        j = pi[j - 1]  # 더 짧은 경계 복구
    if pattern[i] == pattern[j]:  # 경계 확장 가능
        j += 1  # 새 일치 길이
    pi[i] = j  # 현재 경계 저장
matched, count = 0, 0  # 텍스트 일치 길이와 발생 수
for character in text:  # 텍스트를 되돌리지 않는 검색
    while matched and character != pattern[matched]:  # 불일치 복구
        matched = pi[matched - 1]  # 겹친 후보 유지
    if character == pattern[matched]:  # 현재 문자 일치
        matched += 1  # 일치 길이 증가
    if matched == len(pattern):  # 패턴 전체 발생
        count += 1  # 결과 누적
        matched = pi[matched - 1]  # 겹치는 다음 발생 준비
print("WORD", "YES" if exists and terminal[node] else "NO")  # 완전 단어 출력
print("PREFIX", "YES" if exists else "NO")  # 접두사 출력
print("MATCHES", count)  # KMP 발생 수 출력
```

### 언어별 차이

| 비교할 점 | C | C++ | Python |
| --- | --- | --- | --- |
| 표준 입출력 | scanf와 printf의 서식 지정자를 자료형에 맞춥니다. | std::cin과 std::cout으로 같은 토큰과 결과를 처리합니다. | sys.stdin.read().split()으로 읽은 토큰을 필요한 자료형으로 바꿉니다. |
| 배열과 허용 범위 | 트라이201노드×26간선, 문자열101·21칸과 접두사20칸의 고정 상한입니다. | 같은 상한의 고정 배열을 사용하며 입력 범위를 지킵니다. | 상태 길이에 맞춰 리스트를 만들지만 입력의 허용 범위는 같습니다. |
| 정수 연산 | 이 예제의 입력 상한에서 int 또는 long long의 연산 범위를 지킵니다. | C와 같은 정수 상한을 사용하며 중간 계산의 자료형을 확인합니다. | 정수는 임의 정밀도이지만 같은 입력 상한에서 같은 계산을 수행합니다. |

### 예제의 비용과 실행 파일

- 시간: O(P+T+M)
- 보조 공간: O(26P+M+T)

고정 알파벳 트라이와 선형 접두사·텍스트 탐색을 사용하며 읽은 문자열도 보관합니다.

[예제 입력](<예제_examples/28-트라이와문자열매칭_trie-kmp-aho/input.txt>) · [예상 출력](<예제_examples/28-트라이와문자열매칭_trie-kmp-aho/output.txt>) · [예제 실행 방법](<예제_examples/28-트라이와문자열매칭_trie-kmp-aho/README.md>) · [세 언어 확인 기록](<예제_examples/확인기록_validation.md>)
<!-- multilang-examples:end -->

## 보관 풀이와 연결

현재 대표 보관 풀이에서 이 유형으로 직접 분류한 문제는 없습니다. 위의 자체 예제와 참고 자료로 원리를 익힐 수 있으며, 다른 알고리즘으로 푼 문제를 이 유형의 채점 사례로 표시하지 않습니다.
