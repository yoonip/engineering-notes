def solution(price, money, count):
    total = price * count * (count + 1) // 2
    return max(0, total - money)

# 전체 코드 줄별 설명
# def solution(price, money, count):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. price: 기본 이용료, money: 가진 돈, count: 이용 횟수
#     total = price * count * (count + 1) // 2  # //는 내림한 정수 몫. =는 값 저장. 1회부터 count회까지의 이용료를 모두 더한 금액
#     return max(0, total - money)  # return은 결과를 돌려주고 함수 종료. max는 최댓값. 부족한 금액을 반환하되, 돈이 충분하면 0을 반환

# 풀이 요약
# 이용료는 price×1부터 price×count까지 늘어난다. 1~count의 합인 count×(count+1)/2에 price를 곱해 총액을 구한다. 가진 돈이 충분하면 부족액이 음수가 되므로 max로 0을 반환한다.
# 문제의 정수 범위에서 시간·보조 공간 O(1).
