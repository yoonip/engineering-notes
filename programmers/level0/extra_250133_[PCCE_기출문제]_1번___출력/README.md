# [PCCE 기출문제] 1번 / 출력

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/250133) · Level 0 · Python3

## 풀이

숫자 덧셈과 문자열 연결의 차이를 구분합니다. 문자열 값은 따옴표로 감싸 입력합니다.

## 코드와 줄별 설명

빈칸 채우기·한 줄 수정 형식이라 사이트에는 지정된 부분만 제출했습니다. 아래 전체 주석본은 학습용으로 보관합니다.

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
string_msg = "Spring is beginning"
int_val = 3
string_val = "3"
print(string_msg)
print(int_val + 10)
print(string_val + "10")

# 전체 코드 줄별 설명
# string_msg = "Spring is beginning"  # =은 대입, 따옴표는 문자열. 출력할 문장을 저장.
# int_val = 3  # 정수 3을 저장. 숫자의 덧셈에 사용.
# string_val = "3"  # 문자열 3을 저장. 숫자 3과 자료형이 다름.
# print(string_msg)  # print는 화면에 출력하는 함수. 괄호 안의 문자열 출력.
# print(int_val + 10)  # 정수끼리 +는 덧셈. 3+10=13 출력.
# print(string_val + "10")  # 문자열끼리 +는 연결. 3과 10을 이어 310 출력.

# 풀이 요약
# 숫자 덧셈과 문자열 연결의 차이를 구분합니다. 문자열 값은 따옴표로 감싸 입력합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
