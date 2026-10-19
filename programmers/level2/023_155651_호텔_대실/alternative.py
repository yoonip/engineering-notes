from heapq import heappush,heappop

def solution(book_time):
    def minutes(text):
        h,m=map(int,text.split(':'))
        return h*60+m
    heap=[]
    rooms=0
    for start,end in sorted((minutes(a),minutes(b)+10) for a,b in book_time):
        while heap and heap[0]<=start: heappop(heap)
        heappush(heap,end)
        rooms=max(rooms,len(heap))
    return rooms
