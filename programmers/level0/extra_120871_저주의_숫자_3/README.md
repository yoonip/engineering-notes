# 저주의 숫자 3

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/120871) · Level 0 · Python3

## 풀이

숫자를 하나씩 증가시키면서 3의 배수와 3을 포함한 수를 모두 건너뜁니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(n):
    value = 0
    for _ in range(n):
        value += 1
        while value % 3 == 0 or '3' in str(value):
            value += 1
    return value

# 전체 코드 줄별 설명
# def solution(n):  # def는 함수 정의. 3x 마을 숫자로 바꿀 순번 입력.
#     value = 0  # 실제로 사용할 숫자 초기화.
#     for _ in range(n):  # range는 n번 반복, _는 사용하지 않는 반복 변수.
#         value += 1  # +=는 더해 저장. 다음 숫자로 이동.
#         while value % 3 == 0 or '3' in str(value):  # while은 반복, %는 나머지, or는 하나라도 참. 3의 배수이거나 숫자 3 포함이면 제외.
#             value += 1  # 금지 숫자를 건너뛰어 다음 후보 검사.
#     return value  # 금지 조건을 피한 n번째 숫자 반환.

# 풀이 요약
# 숫자를 하나씩 증가시키면서 3의 배수와 3을 포함한 수를 모두 건너뜁니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
