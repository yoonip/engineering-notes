# 치킨 쿠폰

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/120884) · Level 0 · Python3

## 풀이

쿠폰을 치킨으로 바꾸고 서비스 치킨의 쿠폰까지 다시 교환합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(chicken):
    coupons = chicken
    service = 0
    while coupons >= 10:
        free, rest = divmod(coupons, 10)
        service += free
        coupons = free + rest
    return service

# 전체 코드 줄별 설명
# def solution(chicken):  # def는 함수 정의. 처음 주문한 치킨 수 입력.
#     coupons = chicken  # 처음 치킨 한 마리당 쿠폰 한 장으로 초기화.
#     service = 0  # 서비스 치킨 누적 개수 초기화.
#     while coupons >= 10:  # while은 조건 반복, >=는 이상. 교환할 쿠폰이 10장 이상인 동안 반복.
#         free, rest = divmod(coupons, 10)  # divmod는 몫과 나머지 반환. 몫은 서비스 치킨 수, 나머지는 남은 쿠폰.
#         service += free  # +=는 더해 저장. 이번 서비스 치킨 수 누적.
#         coupons = free + rest  # 서비스 치킨에서도 받은 새 쿠폰과 남은 쿠폰을 합침.
#     return service  # 추가로 받을 수 있는 서비스 치킨 총 개수 반환.

# 풀이 요약
# 쿠폰을 치킨으로 바꾸고 서비스 치킨의 쿠폰까지 다시 교환합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점이다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼다. 이 기록을 정리하면서 새로 제출한 것은 아니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
