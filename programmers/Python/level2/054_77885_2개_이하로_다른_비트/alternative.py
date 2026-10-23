def solution(numbers):
    answer=[]
    for number in numbers:
        bits=list('0'+bin(number)[2:])
        index=''.join(bits).rfind('0')
        bits[index]='1'
        if index+1<len(bits): bits[index+1]='0'
        answer.append(int(''.join(bits),2))
    return answer
