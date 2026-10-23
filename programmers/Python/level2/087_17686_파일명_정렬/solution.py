from re import match

def solution(files):
    def key(filename):
        # () 캡처를 groups로 꺼내 언패킹.
        head, number = match(r'(\D+)(\d{1,5})', filename).groups()
        return (head.lower(), int(number))
    return sorted(files, key=key)
