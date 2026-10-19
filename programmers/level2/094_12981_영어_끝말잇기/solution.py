def solution(n, words):
    seen = set()
    # 발언 순서·단어를 언패킹.
    for index, word in enumerate(words):
        if word in seen or (index > 0 and words[index - 1][-1] != word[0]):
            return [index % n + 1, index // n + 1]
        # add로 이번 단어를 사용 목록에 추가.
        seen.add(word)
    return [0, 0]
