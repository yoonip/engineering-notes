def solution(record):
    parsed = [entry.split() for entry in record]
    final = {}
    for parts in reversed(parsed):
        if parts[0] != 'Leave':
            final.setdefault(parts[1], parts[2])
    suffix = {'Enter': '님이 들어왔습니다.', 'Leave': '님이 나갔습니다.'}
    return [final[p[1]] + suffix[p[0]] for p in parsed if p[0] in suffix]
