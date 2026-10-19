def to_seconds(time_string):
    # "분:초" 문자열을 정수 초로 변환
    minutes, seconds = time_string.split(":")
    return int(minutes) * 60 + int(seconds)


def solution(video_len, pos, op_start, op_end, commands):
    # 계산하기 쉽게 모든 시간을 초로 바꾸기
    video_end = to_seconds(video_len)
    current = to_seconds(pos)
    opening_start = to_seconds(op_start)
    opening_end = to_seconds(op_end)

    # 처음 위치가 오프닝 안이면 먼저 건너뛰기
    if opening_start <= current <= opening_end:
        current = opening_end

    # 명령을 하나씩 순서대로 실행
    for command in commands:
        if command == "prev":
            current = max(0, current - 10)

        elif command == "next":
            current = min(video_end, current + 10)

        # 이동한 위치가 오프닝 안이면 건너뛰기
        if opening_start <= current <= opening_end:
            current = opening_end

    # 초를 다시 분과 초로 나누기
    minutes = current // 60
    seconds = current % 60

    # "mm:ss" 형식의 문자열로 반환
    return f"{minutes:02d}:{seconds:02d}"