def solution(phone_book):
    # 접두어가 같은 번호들이 붙게 됨.
    phone_book.sort()
    for index in range(len(phone_book) - 1):
        # 바로 다음 번호가 앞 번호로 시작하는지 확인.
        if phone_book[index + 1].startswith(phone_book[index]):
            return False
    return True
