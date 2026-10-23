def solution(words, queries):
    roots={}
    for word in words:
        for reverse in (False,True):
            node=roots.setdefault((len(word),reverse),{None:0});node[None]+=1
            for letter in word[::-1] if reverse else word:
                node=node.setdefault(letter,{None:0});node[None]+=1
    answer=[]
    for query in queries:
        reverse=query[0]=='?';pattern=query[::-1] if reverse else query
        node=roots.get((len(query),reverse))
        for letter in pattern:
            if letter=='?' or node is None:break
            node=node.get(letter)
        answer.append(node[None] if node is not None else 0)
    return answer
