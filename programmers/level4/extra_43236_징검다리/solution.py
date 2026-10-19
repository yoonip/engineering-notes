def solution(distance, rocks, n):
    positions = sorted(rocks) + [distance]  # sorted는 새 정렬 리스트 생성. +로 고정 도착점도 마지막 간격 검사에 포함.
    low, high = 1, distance  # 최소 간격의 가능한 탐색 범위를 1부터 전체 거리로 초기화.
    answer = 0  # 지금까지 확인한 가능한 최대 최소 간격.
    while low <= high:  # while은 조건이 참인 동안 반복. 이진 탐색 범위가 남아 있으면 실행.
        gap = (low + high) // 2  # //는 정수 나눗셈. 검사할 최소 간격 후보 선택.
        previous = 0  # 마지막으로 남긴 지점은 출발점 0.
        removed = 0  # 최소 간격을 유지하기 위해 제거한 바위 수 초기화.
        for position in positions:  # 앞에서부터 바위와 도착점 순회.
            if position - previous < gap:
                removed += 1
            else:  # else는 필요한 간격 이상 떨어진 경우.
                previous = position  # 현재 바위를 남기고 기준 위치로 갱신.
            if removed > n:  # 허용 제거 개수를 초과했는지 확인.
                break  # break로 불가능한 후보의 검사를 일찍 종료.
        if removed <= n:  # 이 간격이 최대 n개 제거로 가능하면 실행.
            answer = gap  # 가능한 최솟값의 최댓값 후보 저장.
            low = gap + 1  # 더 큰 간격이 가능한지 오른쪽 절반 탐색.
        else:  # 너무 많은 바위 제거가 필요한 경우.
            high = gap - 1  # 간격을 줄여 왼쪽 절반 탐색.
    return answer  # return으로 제거 후 최소 간격의 가능한 최댓값 반환.
