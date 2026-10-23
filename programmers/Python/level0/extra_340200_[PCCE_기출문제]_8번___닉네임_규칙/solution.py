def solution(nickname):
    answer = ""
    for letter in nickname:
        if letter == "l":
            answer += "I"
        elif letter == "w":
            answer += "vv"
        elif letter == "W":
            answer += "VV"
        elif letter == "O":
            answer += "0"
        else:
            answer += letter
    while len(answer) < 4:
        answer += "o"
    if len(answer) > 8:
        answer = answer[:8]
    return answer

# 전체 코드 줄별 설명
# def solution(nickname):  # def는 함수 정의. nickname은 바꿀 닉네임 문자열.
#     answer = ""  # 빈 문자열로 결과 초기화.
#     for letter in nickname:  # for는 문자열의 각 문자를 하나씩 순회.
#         if letter == "l":  # if는 조건문. ==로 소문자 l인지 비교.
#             answer += "I"  # +=는 이어 붙여 저장. l을 대문자 I로 변경.
#         elif letter == "w":  # elif는 앞 조건이 거짓일 때 다음 조건 검사.
#             answer += "vv"  # 소문자 w를 소문자 v 두 개로 변경.
#         elif letter == "W":  # 대문자 W인지 검사.
#             answer += "VV"  # 대문자 V 두 개를 이어 붙임.
#         elif letter == "O":  # 대문자 O인지 검사.
#             answer += "0"  # 숫자 문자 0으로 변경.
#         else:  # 위 어느 조건도 아닌 문자.
#             answer += letter  # 원래 문자를 그대로 이어 붙임.
#     while len(answer) < 4:  # while은 조건이 참인 동안 반복, len은 길이. 4글자가 될 때까지 반복해야 함.
#         answer += "o"  # 부족한 길이를 소문자 o로 채움.
#     if len(answer) > 8:  # 결과가 8글자를 초과하는지 검사.
#         answer = answer[:8]  # [:8]은 앞에서 8번째 문자까지 자르는 슬라이싱. 끝 인덱스 8은 제외.
#     return answer  # return으로 규칙에 맞춘 닉네임 반환.

# 풀이 요약
# 문자를 바꾼 뒤 길이가 4가 될 때까지 o를 반복해서 붙입니다. if를 while로, 기준 3을 4로 바꾸는 한 줄 수정입니다.
# 