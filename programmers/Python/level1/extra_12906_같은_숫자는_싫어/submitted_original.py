def solution(arr):  # 숫자 리스트를 받음
    answer = []  # 남길 숫자를 담을 리스트
    previous = -1  # 입력 숫자가 0~9이므로 입력에 없는 값으로 시작

    for number in arr:  # 숫자를 앞에서부터 하나씩 꺼냄
        if number != previous:  # 바로 이전 숫자와 다르면
            answer.append(number)  # 현재 숫자를 결과에 추가

        previous = number  # 다음 비교를 위해 현재 숫자를 기억

    return answer  # 연속된 중복을 제거한 리스트를 반환