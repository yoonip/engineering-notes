def solution(s):
    output, first = [], True
    for ch in s:
        output.append(ch.upper() if first else ch.lower())
        first = ch == ' '
    return ''.join(output)
