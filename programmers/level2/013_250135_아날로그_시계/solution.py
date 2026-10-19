# 문제: 아날로그 시계
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/250135
# 풀이: 시침·분침에 대한 초침의 상대 속도로 누적 겹침 수를 계산한다. 세 바늘이 함께 겹친 시점의 중복과 시작점 포함 여부를 보정한다.
# 복잡도: 시각을 나타내는 제한 범위 정수 기준 시간·추가 공간 O(1).

def solution(h1, m1, s1, h2, m2, s2):
    start = h1 * 3600 + m1 * 60 + s1
    end = h2 * 3600 + m2 * 60 + s2
    def count(t):
        return t * 719 // 43200 + t * 59 // 3600 - t // 43200 + 1
    at_start = start * 719 % 43200 == 0 or start * 59 % 3600 == 0
    return count(end) - count(start) + int(at_start)
