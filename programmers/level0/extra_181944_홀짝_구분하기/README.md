# 홀짝 구분하기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181944) · Level 0 · Python3

## 풀이

2로 나눈 나머지가 0이면 짝수, 1이면 홀수입니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
n = int(input())
print(f"{n} is even" if n % 2 == 0 else f"{n} is odd")

# 전체 코드 줄별 설명
# n = int(input())  # input은 문자열 입력, int는 정수 변환.
# print(f"{n} is even" if n % 2 == 0 else f"{n} is odd")  # %는 나머지, ==는 같음 비교. 조건 표현식으로 짝수·홀수 문장을 골라 출력.

# 풀이 요약
# 2로 나눈 나머지가 0이면 짝수, 1이면 홀수입니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점이다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼다. 이 기록을 정리하면서 새로 제출한 것은 아니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
