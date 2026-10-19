# 대표 번호 전체 배열을 훑는 대신 그룹마다 셀 집합을 유지합니다. 병합과 해제는 실제 구성원만 방문하지만 집합 자료구조가
# 추가로 필요합니다.
def solution(commands):
    owner=list(range(2500)); members={i:{i} for i in owner}; values={}; answer=[]
    def pos(r,c): return (int(r)-1)*50+int(c)-1
    for command in commands:
        p=command.split(); op=p[0]
        if op=='UPDATE' and len(p)==4:
            values[owner[pos(p[1],p[2])]]=p[3]
        elif op=='UPDATE':
            for group,value in list(values.items()):
                if value==p[1]: values[group]=p[2]
        elif op=='MERGE':
            a,b=owner[pos(p[1],p[2])],owner[pos(p[3],p[4])]
            if a==b: continue
            value=values.get(a,'') or values.get(b,'')
            for cell in members[b]: owner[cell]=a
            members[a].update(members.pop(b)); values.pop(b,None)
            values[a]=value
        elif op=='UNMERGE':
            cell=pos(p[1],p[2]); group=owner[cell]; value=values.pop(group,'')
            old=members.pop(group)
            for member in old:
                owner[member]=member; members[member]={member}
            values[cell]=value
        else:
            answer.append(values.get(owner[pos(p[1],p[2])],'') or 'EMPTY')
    return answer
