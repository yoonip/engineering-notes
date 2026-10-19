def solution(n, words):
    for i, word in enumerate(words):
        repeated = word in words[:i]
        disconnected = i > 0 and words[i - 1][-1] != word[0]
        if repeated or disconnected:
            return [i % n + 1, i // n + 1]
    return [0, 0]
