def solution(n, bans):
    removed = []
    # 삭제 주문 하나씩 순회.
    for word in bans:
        value = 0
        for letter in word:
            # a=1~z=26인 26진수처럼 앞자리 값을 26배 해 더함.
            value = value * 26 + ord(letter) - ord('a') + 1
        removed.append(value)
    # sort는 원본 리스트를 오름차순으로 정렬.
    removed.sort()
    for value in removed:
        # 찾으려는 원래 위치 앞의 삭제인지 검사.
        if value <= n:
            n += 1
        else:
            break
    letters = []
    while n:
        n, digit = divmod(n - 1, 26)
        # 나머지를 a~z로 바꿔 추가.
        letters.append(chr(ord('a') + digit))
    return ''.join(reversed(letters))
