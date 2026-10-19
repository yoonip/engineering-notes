def solution(m, musicinfos):
    def notes(text):
        result = []
        for ch in text:
            if ch == '#':
                result[-1] += '#'
            else:
                result.append(ch)
        return result
    pattern = notes(m)
    failure = [0] * len(pattern)
    j = 0
    for i in range(1, len(pattern)):
        while j and pattern[i] != pattern[j]:
            j = failure[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
        failure[i] = j
    answer, longest = '(None)', -1
    for record in musicinfos:
        start, end, title, score = record.split(',')
        minutes = lambda text: int(text[:2]) * 60 + int(text[3:])
        duration = minutes(end) - minutes(start)
        melody, j = notes(score), 0
        for i in range(duration):
            note = melody[i % len(melody)]
            while j and note != pattern[j]:
                j = failure[j - 1]
            if note == pattern[j]:
                j += 1
            if j == len(pattern):
                if duration > longest:
                    answer, longest = title, duration
                break
    return answer
