def solution(word):
    rank=0
    answer=0
    def visit(prefix):
        nonlocal rank,answer
        if prefix:
            rank+=1
            if prefix==word: answer=rank
        if len(prefix)==5: return
        for vowel in 'AEIOU': visit(prefix+vowel)
    visit('')
    return answer
