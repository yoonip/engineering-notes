# 문자열 돌리기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181945) · Level 0 · Python3

## 풀이

문자열의 각 문자를 개별 줄에 출력하면 세로로 돌린 모양이 됩니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
text = input()
for char in text:
    print(char)

# 전체 코드 줄별 설명
# text = input()  # input은 표준 입력 한 줄을 문자열로 읽음.
# for char in text:  # for는 문자열에서 문자를 앞에서부터 하나씩 순회.
#     print(char)  # print는 출력 후 줄바꿈하므로 한 줄에 한 문자씩 출력.

# 풀이 요약
# 문자열의 각 문자를 개별 줄에 출력하면 세로로 돌린 모양이 됩니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
