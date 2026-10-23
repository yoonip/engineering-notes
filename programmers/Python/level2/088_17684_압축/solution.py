def solution(msg):
    # A~Z를 색인 1~26으로 초기화.
    dictionary = {chr(65 + index): index + 1 for index in range(26)}
    answer = []
    word = ''
    for character in msg:
        # 한 글자 더 붙인 단어가 사전에 있는지 확인.
        if word + character in dictionary:
            word += character
        else:
            # 마지막 일치 단어의 색인도 출력.
            answer.append(dictionary[word])
            dictionary[word + character] = len(dictionary) + 1
            # =로 다음 입력 단어를 현재 문자부터 새로 시작.
            word = character
    if word:
        answer.append(dictionary[word])
    return answer
