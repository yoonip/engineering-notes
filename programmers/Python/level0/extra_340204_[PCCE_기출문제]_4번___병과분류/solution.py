code = input()
last_four_words = code[-4:]
if last_four_words == "_eye":
    print("Ophthalmologyc")
elif last_four_words == "head":
    print("Neurosurgery")
elif last_four_words == "infl":
    print("Orthopedics")
elif last_four_words == "skin":
    print("Dermatology")
else:
    print("direct recommendation")

# 전체 코드 줄별 설명
# code = input()  # input은 한 줄의 문자열 입력. =는 값 저장. 분류할 코드 문자열을 입력받음.
# last_four_words = code[-4:]  # [시작:끝]은 끝을 제외하는 슬라이스. =는 값 저장. 마지막 네 글자를 잘라 분류 기준으로 저장.
# if last_four_words == "_eye":  # if는 조건이 참일 때 실행. ==는 같음 비교. 끝 네 글자가 안과 코드인지 비교.
#     print("Ophthalmologyc")  # print는 값을 표준 출력에 표시. 문제에서 정한 안과 문자열 출력.
# elif last_four_words == "head":  # elif는 앞 조건이 거짓일 때 검사할 다음 조건. ==는 같음 비교. 신경외과 코드인지 비교.
#     print("Neurosurgery")  # print는 값을 표준 출력에 표시. 신경외과 이름 출력.
# elif last_four_words == "infl":  # elif는 앞 조건이 거짓일 때 검사할 다음 조건. ==는 같음 비교. 정형외과 코드인지 비교.
#     print("Orthopedics")  # print는 값을 표준 출력에 표시. 정형외과 이름 출력.
# elif last_four_words == "skin":  # elif는 앞 조건이 거짓일 때 검사할 다음 조건. ==는 같음 비교. 피부과 코드인지 비교.
#     print("Dermatology")  # print는 값을 표준 출력에 표시. 피부과 이름 출력.
# else:  # else는 앞 조건들에 해당하지 않는 경우. 어느 코드에도 해당하지 않는 경우.
#     print("direct recommendation")  # print는 값을 표준 출력에 표시. 직접 추천 문구 출력.

# 풀이 요약
# 코드 전체가 아니라 마지막 네 글자로 병과를 구분한다. 슬라이스 [-4:]로 접미사를 얻고 if·elif를 위에서부터 비교한다. 어느 조건도 맞지 않으면 else의 안내를 출력한다. 출력 철자는 문제에서 지정한 문자열을 유지한다.
# 접미사 길이가 4로 고정되어 분류 시간·보조 공간 O(1). 입력 문자열 저장은 O(N).
