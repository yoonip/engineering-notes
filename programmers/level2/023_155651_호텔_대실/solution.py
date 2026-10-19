# 문제: 호텔 대실
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/155651
# 풀이: 입실 시각에 +1, 청소 종료 시각에 -1을 기록한다. 차분 배열을 누적해 동시에 필요한 객실 수의 최댓값을 구한다.
# 복잡도: 예약 N개·분 단위 범위 T=1450: 시간 O(N+T), 추가 공간 O(T).

def solution(book_time):
    changes = [0] * 1450
    for start, end in book_time:
        sh, sm = map(int, start.split(':'))
        eh, em = map(int, end.split(':'))
        changes[sh * 60 + sm] += 1
        changes[eh * 60 + em + 10] -= 1
    active = answer = 0
    for change in changes:
        active += change
        answer = max(answer, active)
    return answer
