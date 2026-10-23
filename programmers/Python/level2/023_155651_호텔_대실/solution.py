def solution(book_time):
    changes = [0] * 1450
    for start, end in book_time:
        sh, sm = map(int, start.split(':'))
        eh, em = map(int, end.split(':'))
        changes[sh * 60 + sm] += 1
        # 방을 다시 쓸 수 있는 시각은 종료 10분 뒤다.
        changes[eh * 60 + em + 10] -= 1
    active = answer = 0
    # 시간 변화량을 누적하면 동시에 점유 중인 방 수가 된다.
    for change in changes:
        active += change
        answer = max(answer, active)
    return answer
