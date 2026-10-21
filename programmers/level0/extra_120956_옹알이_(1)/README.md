# 옹알이 (1)

[Level 0 목록 / Level 0 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/120956) · Level 0 · Python3

## 풀이

허용 발음을 공백으로 바꾼 뒤 다른 글자가 남는지 확인합니다. 빈 문자열로 지우면 남은 글자가 붙어 잘못된 발음이 만들어질 수 있습니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(babbling):
    count = 0
    for word in babbling:
        for sound in ('aya', 'ye', 'woo', 'ma'):
            word = word.replace(sound, ' ')
        if not word.strip():
            count += 1
    return count

# 전체 코드 줄별 설명
# def solution(babbling):  # def는 함수 정의. 발음할 단어들의 리스트 입력.
#     count = 0  # 발음 가능한 단어 수 초기화.
#     for word in babbling:  # for로 각 단어 순회.
#         for sound in ('aya', 'ye', 'woo', 'ma'):  # ()는 튜플. 허용된 네 발음을 차례로 검사.
#             word = word.replace(sound, ' ')  # replace는 문자열 치환. 발음한 구간을 공백으로 바꿔 다른 글자가 새로 이어지는 것을 막음.
#         if not word.strip():  # strip은 양 끝 공백 제거, not은 부정. 남은 글자가 하나도 없으면 발음 가능한 조합.
#             count += 1  # +=는 더해 저장. 가능한 단어 개수 증가.
#     return count  # 발음 가능한 단어 총 개수 반환.

# 풀이 요약
# 허용 발음을 공백으로 바꾼 뒤 다른 글자가 남는지 확인합니다. 빈 문자열로 지우면 남은 글자가 붙어 잘못된 발음이 만들어질 수 있습니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
