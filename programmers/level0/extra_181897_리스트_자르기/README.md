# 리스트 자르기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181897) · Level 0 · Python3

## 풀이

n에 따라 슬라이싱의 시작·끝·간격을 선택합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(n, slicer, num_list):
    a, b, c = slicer
    if n == 1:
        return num_list[:b + 1]
    if n == 2:
        return num_list[a:]
    if n == 3:
        return num_list[a:b + 1]
    return num_list[a:b + 1:c]

# 전체 코드 줄별 설명
# def solution(n, slicer, num_list):  # def는 함수 정의. 자르기 종류·범위 설정·리스트 입력.
#     a, b, c = slicer  # 리스트의 세 값을 시작·끝·간격 변수에 나누어 대입.
#     if n == 1:  # if는 조건, ==는 같음 비교. 첫 번째 자르기 유형 검사.
#         return num_list[:b + 1]  # [:끝]은 처음부터 끝 직전까지. b 위치를 포함하려고 1을 더함.
#     if n == 2:  # 두 번째 유형 검사.
#         return num_list[a:]  # [시작:]은 a 위치부터 끝까지 슬라이싱.
#     if n == 3:  # 세 번째 유형 검사.
#         return num_list[a:b + 1]  # a부터 b까지 양 끝을 포함하는 부분 리스트.
#     return num_list[a:b + 1:c]  # [시작:끝:간격] 형식으로 a부터 b까지 c칸 간격 추출.

# 풀이 요약
# n에 따라 슬라이싱의 시작·끝·간격을 선택합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점이다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼다. 이 기록을 정리하면서 새로 제출한 것은 아니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
