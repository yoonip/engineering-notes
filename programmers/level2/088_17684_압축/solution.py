# 문제: 압축
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/17684
# 풀이: 가장 긴 사전 단어를 찾으며 해시 사전을 확장한다. 더 늘릴 수 없을 때 기존 색인을 출력하고 확장 단어를 등록한다.
# 복잡도: 문자열 길이 N: 문자열 복사·해시·사전 저장을 포함한 시간·추가 공간 상한 O(N²).

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
