def to_seconds(time_string):
    minutes, seconds = time_string.split(":")
    return int(minutes) * 60 + int(seconds)

def solution(video_len, pos, op_start, op_end, commands):
    video_end = to_seconds(video_len)
    current = to_seconds(pos)
    opening_start = to_seconds(op_start)
    opening_end = to_seconds(op_end)
    if opening_start <= current <= opening_end:
        current = opening_end
    for command in commands:
        if command == "prev":
            current = max(0, current - 10)
        elif command == "next":
            current = min(video_end, current + 10)
        if opening_start <= current <= opening_end:
            current = opening_end
    minutes = current // 60
    seconds = current % 60
    return f"{minutes:02d}:{seconds:02d}"

# 전체 코드 줄별 설명
# def to_seconds(time_string):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. 분:초 문자열을 초로 바꾸는 보조 함수.
#     minutes, seconds = time_string.split(":")  # split은 구분자로 문자열 분리. ()로 묶은 여러 값은 변경 불가 튜플. =는 값 저장. 콜론으로 분·초 문자열을 나눔.
#     return int(minutes) * 60 + int(seconds)  # return은 결과를 돌려주고 함수 종료. int는 정수 변환. 분을 60배 하고 초를 더해 정수 초 반환.
# 
# def solution(video_len, pos, op_start, op_end, commands):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. 영상 길이·현재 위치·오프닝·명령을 입력받음.
#     video_end = to_seconds(video_len)  # =는 값 저장. 영상의 끝을 초로 저장.
#     current = to_seconds(pos)  # =는 값 저장. 현재 재생 위치를 초로 저장.
#     opening_start = to_seconds(op_start)  # =는 값 저장. 오프닝 시작 시각을 초로 저장.
#     opening_end = to_seconds(op_end)  # =는 값 저장. 오프닝 끝 시각을 초로 저장.
#     if opening_start <= current <= opening_end:  # if는 조건이 참일 때 실행. <=는 이하 비교. 초기 위치가 오프닝 양 끝을 포함하는 구간인지 확인.
#         current = opening_end  # =는 값 저장. 오프닝 끝으로 건너뜀.
#     for command in commands:  # for·in은 원소를 차례로 꺼내는 반복문. 주어진 재생 명령을 순서대로 처리.
#         if command == "prev":  # if는 조건이 참일 때 실행. ==는 같음 비교. 10초 전으로 이동하는 명령인지 확인.
#             current = max(0, current - 10)  # max는 최댓값. =는 값 저장. 0초보다 작아지지 않도록 10초를 뺌.
#         elif command == "next":  # elif는 앞 조건이 거짓일 때 검사할 다음 조건. ==는 같음 비교. 10초 후로 이동하는 명령인지 확인.
#             current = min(video_end, current + 10)  # min은 최솟값. =는 값 저장. 영상 끝을 넘지 않도록 10초를 더함.
#         if opening_start <= current <= opening_end:  # if는 조건이 참일 때 실행. <=는 이하 비교. 이동 후 위치도 오프닝 구간인지 검사.
#             current = opening_end  # =는 값 저장. 오프닝 끝으로 건너뜀.
#     minutes = current // 60  # //는 내림한 정수 몫. =는 값 저장. 총 초를 60으로 나눈 몫이 분.
#     seconds = current % 60  # %는 나머지. =는 값 저장. 60으로 나눈 나머지가 초.
#     return f"{minutes:02d}:{seconds:02d}"  # return은 결과를 돌려주고 함수 종료. f-string의 {} 안은 값 삽입, :02d는 두 자리 정수 표시. 각 숫자를 두 자리로 맞춰 분:초 문자열 반환.

# 풀이 요약
# 모든 시각을 초로 바꾼다. 명령마다 10초를 이동하고 0초와 영상 끝으로 범위를 제한한 뒤 오프닝 안이면 끝으로 건너뛴다. 명령을 실행하기 전 초기 위치도 오프닝인지 확인한다. 마지막에는 몫과 나머지로 분:초를 복원한다.
# 명령 수 C: 시간 O(C), 보조 공간 O(1).
