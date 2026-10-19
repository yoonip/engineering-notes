def solution(msg):
    dictionary = {chr(65 + index): index + 1 for index in range(26)}
    answer = []
    word = ''
    for character in msg:
        if word + character in dictionary:
            word += character
        else:
            answer.append(dictionary[word])
            dictionary[word + character] = len(dictionary) + 1
            word = character
    if word:
        answer.append(dictionary[word])
    return answer

# 전체 코드 줄별 설명
# def solution(msg):  # def는 함수 정의. msg는 영문 대문자 메시지 입력.
#     dictionary = {chr(65 + index): index + 1 for index in range(26)}  # {} 딕셔너리 내포. chr은 문자 코드의 문자 반환. A~Z를 색인 1~26으로 초기화.
#     answer = []  # []는 출력 색인 리스트.
#     word = ''  # ''는 빈 문자열. 현재 사전에 있는 가장 긴 입력 단어 저장.
#     for character in msg:  # for~in으로 입력 문자를 순서대로 처리.
#         if word + character in dictionary:  # +는 문자열 연결, in은 키 포함 검사. 한 글자 더 붙인 단어가 사전에 있는지 확인.
#             word += character  # +=로 문자열 연결 후 저장. 더 긴 일치 단어로 확장.
#         else:  # else는 확장한 단어가 사전에 없는 경우.
#             answer.append(dictionary[word])  # [키]의 색인 번호를 append로 출력 목록에 추가.
#             dictionary[word + character] = len(dictionary) + 1  # len은 항목 수. 새 단어에 다음 색인 부여.
#             word = character  # =로 다음 입력 단어를 현재 문자부터 새로 시작.
#     if word:  # 빈 문자열은 거짓. 마지막에 아직 출력하지 않은 단어가 있는지 검사.
#         answer.append(dictionary[word])  # 마지막 일치 단어의 색인도 출력.
#     return answer  # return으로 LZW 압축 색인 목록 반환.

# 풀이 요약
# 사전에 있는 동안 단어를 늘리고, 더 늘릴 수 없으면 이전 단어의 색인을 출력한 뒤 확장 단어를 새로 등록합니다.
# 예: KAKAO는 K·A·KA·O로 읽어 [11,1,27,15]. 문자열 처리·저장을 포함한 최악 시간·공간 상한 O(N²).
