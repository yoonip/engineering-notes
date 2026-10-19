# 문제: JadenCase 문자열 만들기
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/12951
# 풀이: 공백 한 칸으로 나눠 빈 단어를 보존한다. 단어별 capitalize 결과를 다시 같은 공백으로 이어 붙인다.
# 복잡도: 문자열 길이 N: 시간·추가 공간 O(N).

def solution(s):
    words = s.split(' ')
    changed = [word.capitalize() for word in words]
    return ' '.join(changed)
