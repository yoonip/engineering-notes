def solution(land, P, Q):
    values=[x for row in land for x in row]
    def cost(target):return sum((target-x)*P if x<target else (x-target)*Q for x in values)
    low,high=min(values),max(values)
    while low<high:
        middle=(low+high)//2
        if cost(middle)<=cost(middle+1):high=middle
        else:low=middle+1
    return cost(low)
