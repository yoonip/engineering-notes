# 크기가 작은 부분 문자열

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/147355) · Level 1 · Python3

유형: 문자열 · 슬라이딩 구간

## 풀이 원리

p의 길이와 같은 부분 문자열을 t의 모든 시작 위치에서 자릅니다. 각 조각을 숫자로 바꿔 p 이하인지 셉니다. 시작 위치의 마지막 값은 len(t)-len(p)이므로 range의 끝에 1을 더합니다.

t 길이 T, p 길이 P: 시간 O(TP), 보조 공간 O(P).

## 공식 예제

입력 인수: `["3141592", "271"]`

반환값: `2`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있습니다.

## 코드와 줄별 설명

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
def solution(t, p):
    answer = 0
    n = len(p)
    for i in range(len(t) - n + 1):
        num = int(t[i:i+n])
        if num <= int(p):
            answer += 1
    return answer

# 전체 코드 줄별 설명
# def solution(t, p):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. 문자열 t와 비교할 숫자 문자열 p를 입력받음
#     answer = 0  # =는 값 저장. 조건을 만족하는 부분 문자열의 개수를 저장
#     n = len(p)  # len은 길이. =는 값 저장. p의 문자열 길이를 구함
#     for i in range(len(t) - n + 1):  # for·in은 원소를 차례로 꺼내는 반복문. len은 길이. range는 끝값 직전까지 정수 순서 생성. t에서 길이가 n인 부분 문자열을 추출할 시작 위치 반복
#         num = int(t[i:i+n])  # int는 정수 변환. [시작:끝]은 끝을 제외하는 슬라이스. =는 값 저장. t[i:i+n]으로 n글자를 추출하고 int()로 정수 변환
#         if num <= int(p):  # if는 조건이 참일 때 실행. int는 정수 변환. <=는 이하 비교. 추출한 숫자가 p보다 작거나 같으면
#             answer += 1  # +=는 더하거나 연결한 값을 저장. 조건을 만족하므로 개수를 1 증가
#     return answer  # return은 결과를 돌려주고 함수 종료. 조건을 만족한 부분 문자열의 총개수 반환

# 풀이 요약
# p의 길이와 같은 부분 문자열을 t의 모든 시작 위치에서 자른다. 각 조각을 숫자로 바꿔 p 이하인지 센다. 시작 위치의 마지막 값은 len(t)-len(p)이므로 range의 끝에 1을 더한다.
# t 길이 T, p 길이 P: 시간 O(TP), 보조 공간 O(P).
```

## 확인한 범위

2026-10-16 00:26:21의 Python3 제출 내역에서 정답 100/100을 확인했습니다. 원본은 그대로 보관했습니다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같습니다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았습니다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있습니다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
