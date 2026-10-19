# 항공권을 목적지 사전순으로 하나씩 선택하고 막히면 되돌립니다. 처음 완성되는 경로가 사전순 최솟값입니다. 오일러 경로보다
# 최악 시간은 훨씬 큽니다.
# 작은 입력의 비교·검증용입니다. 원래 최대 입력 제출에는 기본 풀이를 사용합니다.
def solution(tickets):
    ordered=sorted(enumerate(tickets),key=lambda p:p[1][1]);used=set();path=['ICN']
    def dfs():
        if len(used)==len(tickets):return True
        for index,(a,b) in ordered:
            if index not in used and a==path[-1]:
                used.add(index);path.append(b)
                if dfs():return True
                path.pop();used.remove(index)
        return False
    dfs();return path
