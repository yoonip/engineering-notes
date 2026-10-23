def solution(targets):
    # 가장 먼저 끝나는 아직 미처리 구간부터 맞힌다.
    targets.sort(key=lambda target: target[1])
    answer = 0
    end = -1
    for start, stop in targets:
        # 끝점은 제외되므로 시작이 이전 끝점과 같아도 새 요격이 필요하다.
        if start >= end:
            answer += 1
            end = stop
    return answer
