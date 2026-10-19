def solution(s, skip, index):
    alphabet = ""

    for char in "abcdefghijklmnopqrstuvwxyz":
        if char not in skip:
            alphabet += char

    answer = ""

    for char in s:
        position = alphabet.index(char)
        next_position = (position + index) % len(alphabet)
        answer += alphabet[next_position]

    return answer


# 같은 정답 코드 + 줄별 문법 설명
# 아래는 전체가 주석이므로 실행되지 않습니다.

# def solution(s, skip, index):  # def는 함수 정의입니다. 세 매개변수로 입력을 받습니다.
#     alphabet = ""  # ""는 빈 문자열입니다. =로 변수에 값을 저장합니다.
#
#     for char in "abcdefghijklmnopqrstuvwxyz":  # 문자열에서 글자를 하나씩 꺼내 반복합니다.
#         if char not in skip:  # not in은 해당 글자가 skip에 포함되지 않았는지 검사합니다.
#             alphabet += char  # alphabet = alphabet + char와 같습니다. 글자를 뒤에 붙입니다.
#
#     answer = ""  # 변환 결과를 저장할 빈 문자열입니다.
#
#     for char in s:  # 입력 문자열 s의 글자를 순서대로 하나씩 처리합니다.
#         position = alphabet.index(char)  # .index()는 글자의 위치를 구합니다. 위치는 0부터입니다.
#         next_position = (position + index) % len(alphabet)  # len()은 길이, %는 나머지입니다. 길이가 22라면 위치 22는 0으로 돌아옵니다.
#         answer += alphabet[next_position]  # 문자열[위치]로 변환할 글자를 읽어 결과 뒤에 붙입니다.
#
#     return answer  # 완성한 문자열을 반환합니다. for문 바깥이므로 모든 글자를 처리한 뒤 실행됩니다.