def solution(sales, links):
    n=len(sales)
    if n>20:raise ValueError("직원 20명 이하의 참석 조합 전수 비교용입니다")
    teams={}
    for manager,child in links:teams[manager]=teams.get(manager,1<<(manager-1))|1<<(child-1)
    return min(sum(sales[i] for i in range(n) if mask>>i&1)
               for mask in range(1<<n) if all(mask&team for team in teams.values()))
