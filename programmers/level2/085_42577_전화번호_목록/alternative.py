def solution(phone_book):
    full = set(phone_book)
    for number in phone_book:
        for end in range(1, len(number)):
            if number[:end] in full:
                return False
    return True
