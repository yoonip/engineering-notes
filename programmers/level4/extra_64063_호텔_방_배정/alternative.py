def solution(k, room_number):
    if len(room_number)>5000:raise ValueError("요청 5000개 이하의 순차 탐색 비교용입니다")
    occupied=set();answer=[]
    for requested in room_number:
        room=requested
        while room in occupied:room+=1
        occupied.add(room);answer.append(room)
    return answer
