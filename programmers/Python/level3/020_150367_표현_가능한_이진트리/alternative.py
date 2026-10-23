# 문자열을 자르지 않고 인덱스 구간과 부모가 비어 있는지 여부를 전달합니다. 부모가 비어 있으면 모든 후손도 0이어야
# 합니다.
def solution(numbers):
    answer=[]
    for number in numbers:
        bits=bin(number)[2:]
        size=1
        while size<len(bits): size=size*2+1
        bits=bits.zfill(size)
        def walk(left,right,missing):
            if left>=right: return True
            middle=(left+right)//2
            if missing and bits[middle]=='1': return False
            missing=missing or bits[middle]=='0'
            return walk(left,middle,missing) and walk(middle+1,right,missing)
        answer.append(int(walk(0,size,False)))
    return answer
