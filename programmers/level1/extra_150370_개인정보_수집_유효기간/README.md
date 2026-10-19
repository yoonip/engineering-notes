# 개인정보 수집 유효기간

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/150370) · Level 1 · Python3

유형: 날짜 계산 · 해시

## 풀이 원리

모든 달이 28일이라는 문제 규칙에 따라 날짜를 하나의 일수로 바꾼다. 수집일에 약관 개월 수×28을 더한 날부터 만료이므로 오늘이 그 날짜 이상이면 파기 대상이다. 일반 달력의 월별 일수나 윤년을 적용하면 안 된다.

약관 T개, 개인정보 P개: 평균 시간 O(T+P), 공간 O(T+P).

## 공식 예제

입력 인수: `["2022.05.19", ["A 6", "B 12", "C 3"], ["2021.05.02 A", "2021.07.01 B", "2022.02.19 C", "2022.02.20 C"]]`

반환값: `[1, 3]`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있다.

## 코드와 줄별 설명

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
def solution(today, terms, privacies):
    def to_days(date):
        y, m, d = map(int, date.split("."))
        return y * 12 * 28 + m * 28 + d
    term_dict = {}
    for term in terms:
        kind, months = term.split()
        term_dict[kind] = int(months)
    today_days = to_days(today)
    answer = []
    for i, privacy in enumerate(privacies, start=1):
        date, kind = privacy.split()
        expiry_days = to_days(date) + term_dict[kind] * 28
        if today_days >= expiry_days:
            answer.append(i)
    return answer

# 전체 코드 줄별 설명
# def solution(today, terms, privacies):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. 오늘 날짜, 약관 정보, 개인정보 목록을 입력받는 함수
#     def to_days(date):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. 날짜를 일수로 변환하는 내부 함수
#         y, m, d = map(int, date.split("."))  # map은 각 원소에 함수 적용. split은 구분자로 문자열 분리. ()로 묶은 여러 값은 변경 불가 튜플. =는 값 저장. "."을 기준으로 날짜를 나누고 각각 정수로 변환
#         return y * 12 * 28 + m * 28 + d  # return은 결과를 돌려주고 함수 종료. 1년 12개월, 1개월 28일 기준으로 전체 일수 계산
#     term_dict = {}  # {}는 키:값을 저장하는 딕셔너리. =는 값 저장. 약관 종류별 유효기간을 저장할 딕셔너리
#     for term in terms:  # for·in은 원소를 차례로 꺼내는 반복문. 약관 정보를 하나씩 반복
#         kind, months = term.split()  # split은 구분자로 문자열 분리. ()로 묶은 여러 값은 변경 불가 튜플. =는 값 저장. 공백 기준 분리 (예: "A 6" → "A", "6")
#         term_dict[kind] = int(months)  # int는 정수 변환. []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. =는 값 저장. 약관 종류를 키로, 유효기간을 정수로 저장
#     today_days = to_days(today)  # =는 값 저장. 오늘 날짜를 일수로 변환
#     answer = []  # []는 리스트. =는 값 저장. 파기할 개인정보 번호를 저장할 리스트
#     for i, privacy in enumerate(privacies, start=1):  # for·in은 원소를 차례로 꺼내는 반복문. enumerate는 인덱스·값을 함께 제공. ()로 묶은 여러 값은 변경 불가 튜플. =는 이름 붙인 인수에 값 지정. 개인정보를 1번부터 번호를 붙여 순회
#         date, kind = privacy.split()  # split은 구분자로 문자열 분리. ()로 묶은 여러 값은 변경 불가 튜플. =는 값 저장. 수집 날짜와 약관 종류 분리
#         expiry_days = to_days(date) + term_dict[kind] * 28  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. =는 값 저장. 수집일에 유효기간을 더해 만료 기준일 계산
#         if today_days >= expiry_days:  # if는 조건이 참일 때 실행. >=는 이상 비교. 오늘이 만료 기준일과 같거나 늦으면
#             answer.append(i)  # append는 리스트 끝에 추가. 파기할 개인정보 번호를 추가
#     return answer  # return은 결과를 돌려주고 함수 종료. 파기해야 하는 개인정보 번호 목록 반환

# 풀이 요약
# 모든 달이 28일이라는 문제 규칙에 따라 날짜를 하나의 일수로 바꾼다. 수집일에 약관 개월 수×28을 더한 날부터 만료이므로 오늘이 그 날짜 이상이면 파기 대상이다. 일반 달력의 월별 일수나 윤년을 적용하면 안 된다.
# 약관 T개, 개인정보 P개: 평균 시간 O(T+P), 공간 O(T+P).
```

## 확인한 범위

2026-10-16 00:21:54의 Python3 제출 내역에서 정답 100/100을 확인했다. 원본은 그대로 보관했다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
