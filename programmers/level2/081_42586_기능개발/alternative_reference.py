def solution(progresses, speeds):
    progresses = progresses[:]
    front, answer = 0, []
    while front < len(progresses):
        for i in range(front, len(progresses)):
            progresses[i] += speeds[i]
        count = 0
        while front < len(progresses) and progresses[front] >= 100:
            front += 1
            count += 1
        if count:
            answer.append(count)
    return answer
