def solution(files):
    parsed = []
    for filename in files:
        start = next(i for i, ch in enumerate(filename) if '0' <= ch <= '9')
        end = start
        while end < len(filename) and end < start + 5 and filename[end].isdigit():
            end += 1
        parsed.append((filename[:start].lower(), int(filename[start:end]), filename))
    parsed.sort(key=lambda item: item[1])
    parsed.sort(key=lambda item: item[0])
    return [item[2] for item in parsed]
