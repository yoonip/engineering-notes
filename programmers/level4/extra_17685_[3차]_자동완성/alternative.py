def solution(words):
    root={None:0}
    for word in words:
        node=root;node[None]+=1
        for letter in word:node=node.setdefault(letter,{None:0});node[None]+=1
    answer=0
    for word in words:
        node=root
        for length,letter in enumerate(word,1):
            node=node[letter]
            if node[None]==1:break
        answer+=length
    return answer
