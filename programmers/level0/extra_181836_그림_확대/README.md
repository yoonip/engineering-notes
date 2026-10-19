# 그림 확대

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181836) · Level 0 · Python3

## 풀이

문자를 k번 반복해 가로 확대하고 완성된 행을 k번 반복해 세로 확대합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(picture, k):
    answer = []
    for row in picture:
        expanded = ''.join(char * k for char in row)
        answer.extend([expanded] * k)
    return answer

# 전체 코드 줄별 설명
# def solution(picture, k):  # def는 함수 정의. 그림의 행 문자열 리스트와 확대 배율 입력.
#     answer = []  # []는 빈 리스트. 확대된 행 저장.
#     for row in picture:  # for로 각 행 문자열 순회.
#         expanded = ''.join(char * k for char in row)  # 문자 * 정수는 반복. 각 픽셀을 가로로 k번 반복한 뒤 join으로 연결.
#         answer.extend([expanded] * k)  # 같은 확대 행을 세로로 k번 반복. extend로 여러 행을 결과에 추가.
#     return answer  # 가로·세로 모두 k배로 확대한 그림 반환.

# 풀이 요약
# 문자를 k번 반복해 가로 확대하고 완성된 행을 k번 반복해 세로 확대합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점이다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼다. 이 기록을 정리하면서 새로 제출한 것은 아니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
