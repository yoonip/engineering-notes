# 마지막 두 원소

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181927) · Level 0 · Python3

## 풀이

마지막 값이 더 크면 차이를, 아니면 마지막 값의 두 배를 뒤에 추가합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(num_list):
    last, previous = num_list[-1], num_list[-2]
    return num_list + [last - previous if last > previous else last * 2]

# 전체 코드 줄별 설명
# def solution(num_list):  # def는 함수 정의. 정수 리스트 입력.
#     last, previous = num_list[-1], num_list[-2]  # 음수 인덱스 -1은 마지막, -2는 끝에서 두 번째 원소.
#     return num_list + [last - previous if last > previous else last * 2]  # 조건 표현식으로 추가 값 선택. []로 한 원소 리스트를 만들고 +로 연결.

# 풀이 요약
# 마지막 값이 더 크면 차이를, 아니면 마지막 값의 두 배를 뒤에 추가합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
