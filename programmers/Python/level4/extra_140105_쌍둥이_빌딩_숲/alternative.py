from functools import cache

def solution(n, count):
    if n>6:raise ValueError("작은 빌딩 배치를 직접 생성하는 비교용입니다")
    arrangements=[(1,1)]
    # 기존 높이를 모두 올리면 새 최저 높이 쌍을 붙여 넣을 수 있다.
    for _ in range(1,n):
        enlarged=[]
        for row in arrangements:
            raised=tuple(x+1 for x in row)
            for index in range(len(row)+1):enlarged.append(raised[:index]+(1,1)+raised[index:])
        arrangements=enlarged
    answer=0
    for row in arrangements:
        highest=visible=0
        for height in row:
            if height>highest:highest=height;visible+=1
        answer+=visible==count
    return answer
