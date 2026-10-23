
def solution(wallet, bill):
    wallet.sort()
    bill.sort()

    answer = 0

    while bill[0] > wallet[0] or bill[1] > wallet[1]:
        bill[1] //= 2
        bill.sort()
        answer += 1

    return answer
