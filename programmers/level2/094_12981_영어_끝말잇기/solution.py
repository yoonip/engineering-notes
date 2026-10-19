# 문제: 영어 끝말잇기
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/12981
# 풀이: 단어 set으로 중복을 확인하고 앞 단어의 끝과 현재 단어의 시작을 비교한다. 첫 위반 인덱스의 몫·나머지로 사람과 차례를 구한다.
# 복잡도: 전체 단어 길이 합 L: 평균 시간 O(L), 추가 공간 O(L).

def solution(n, words):
    seen = set()
    for index, word in enumerate(words):
        if word in seen or (index > 0 and words[index - 1][-1] != word[0]):
            return [index % n + 1, index // n + 1]
        seen.add(word)
    return [0, 0]
