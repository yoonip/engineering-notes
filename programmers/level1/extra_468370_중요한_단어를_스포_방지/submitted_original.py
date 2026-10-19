def solution(message, spoiler_ranges):
    n = len(message)

    hidden = [False] * n

    for start, end in spoiler_ranges:
        for i in range(start, end + 1):
            hidden[i] = True

    visible_words = set()
    spoiler_words = set()

    i = 0

    while i < n:
        if message[i] == " ":
            i += 1
            continue

        start = i

        while i < n and message[i] != " ":
            i += 1

        word = message[start:i]

        if any(hidden[start:i]):
            spoiler_words.add(word)
        else:
            visible_words.add(word)

    return len(spoiler_words - visible_words)
