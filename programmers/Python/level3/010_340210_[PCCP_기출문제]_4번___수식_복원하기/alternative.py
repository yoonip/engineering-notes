def solution(expressions):
    equations = [text.split() for text in expressions]
    minimum = max(2, 1 + max(int(ch) for text in expressions for ch in text if ch.isdigit()))
    def parse(text, base):
        value = 0
        for ch in text:
            value = value * base + int(ch)
        return value
    def encode(value, base):
        if value < base:
            return str(value)
        return encode(value // base, base) + str(value % base)
    options = []
    for base in range(minimum, 10):
        restored, valid = [], True
        for a, operator, b, _, c in equations:
            value = parse(a, base) + (1 if operator == '+' else -1) * parse(b, base)
            if c == 'X':
                restored.append(encode(value, base))
            elif value != parse(c, base):
                valid = False
        if valid:
            options.append(restored)
    missing = [parts for parts in equations if parts[4] == 'X']
    output = []
    for i, (a, operator, b, _, _) in enumerate(missing):
        values = {option[i] for option in options}
        output.append(f'{a} {operator} {b} = {next(iter(values)) if len(values) == 1 else "?"}')
    return output
