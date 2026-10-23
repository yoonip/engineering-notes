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

# 전체 코드 줄별 설명
# def solution(s, skip, index):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. def는 함수 정의입니다. 세 매개변수로 입력을 받습니다.
#     alphabet = ""  # =는 값 저장. ""는 빈 문자열입니다. =로 변수에 값을 저장합니다.
#     for char in "abcdefghijklmnopqrstuvwxyz":  # for·in은 원소를 차례로 꺼내는 반복문. 문자열에서 글자를 하나씩 꺼내 반복합니다.
#         if char not in skip:  # if는 조건이 참일 때 실행. not in은 포함되지 않음. not in은 해당 글자가 skip에 포함되지 않았는지 검사합니다.
#             alphabet += char  # +=는 더하거나 연결한 값을 저장. alphabet = alphabet + char와 같습니다. 글자를 뒤에 붙입니다.
#     answer = ""  # =는 값 저장. 변환 결과를 저장할 빈 문자열입니다.
#     for char in s:  # for·in은 원소를 차례로 꺼내는 반복문. 입력 문자열 s의 글자를 순서대로 하나씩 처리합니다.
#         position = alphabet.index(char)  # index는 값이 처음 나오는 위치. =는 값 저장. .index()는 글자의 위치를 구합니다. 위치는 0부터입니다.
#         next_position = (position + index) % len(alphabet)  # len은 길이. %는 나머지. =는 값 저장. len()은 길이, %는 나머지입니다. 길이가 22라면 위치 22는 0으로 돌아옵니다.
#         answer += alphabet[next_position]  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. +=는 더하거나 연결한 값을 저장. 문자열[위치]로 변환할 글자를 읽어 결과 뒤에 붙입니다.
#     return answer  # return은 결과를 돌려주고 함수 종료. 완성한 문자열을 반환합니다. for문 바깥이므로 모든 글자를 처리한 뒤 실행됩니다.

# 풀이 요약
# skip에 없는 알파벳만 순서대로 이어 새 알파벳표를 만든다. 현재 문자의 표 안 위치에 index를 더하고 표 길이로 나눈 나머지를 쓰면 z 뒤에서 다시 처음으로 돌아간다. 건너뛸 문자를 표에서 미리 제거했으므로 이동할 때 다시 검사하지 않는다.
# 문자 수 N: 알파벳 조회 O(N), 문자열 연결 복사를 포함한 보수적 시간 상한 O(N²), 공간 O(N).
