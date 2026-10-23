def solution(s):
    value=int(s,2)
    length=len(s)
    turns=zeros=0
    while length!=1 or value!=1:
        ones=value.bit_count()
        zeros+=length-ones
        value=ones
        length=value.bit_length()
        turns+=1
    return [turns,zeros]
