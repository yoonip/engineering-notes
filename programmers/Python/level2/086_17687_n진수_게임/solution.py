def solution(n, t, m, p):
    # 진법의 각 자릿수를 대문자까지 표현할 문자열.
    digits = '0123456789ABCDEF'
    stream = []
    number = 0
    while len(stream) < t * m:
        # 나눗셈 중에도 원래 정수를 보존하도록 작업용 변수 복사.
        value = number
        converted = '0' if value == 0 else ''
        while value:
            # 두 값 언패킹.
            value, remainder = divmod(value, n)
            converted = digits[remainder] + converted
        # extend는 문자열의 문자들을 리스트 끝에 각각 추가.
        stream.extend(converted)
        number += 1
    return ''.join(stream[p - 1:t * m:m])
