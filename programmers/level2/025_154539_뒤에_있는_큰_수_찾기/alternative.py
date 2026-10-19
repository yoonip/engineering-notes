def solution(numbers):
    n=len(numbers)
    following=[n]*n
    for i in range(n-1,-1,-1):
        j=i+1
        while j<n and numbers[j]<=numbers[i]:
            j=following[j]
        following[i]=j
    return [numbers[j] if j<n else -1 for j in following]
