# 문제: 서버 증설 횟수
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/389479
# 풀이: 만료 시각별 서버 수를 배열에 기록한다. 매 시각 만료분을 빼고 부족한 만큼만 추가해 서버별 반복 검사를 피한다.
# 복잡도: 시간대 T개·유지 기간 K: 시간 O(T+K), 추가 공간 O(T+K).

def solution(players, m, k):
    expires = [0] * (len(players) + k)
    active = 0
    answer = 0
    for hour, people in enumerate(players):
        active -= expires[hour]
        added = max(0, people // m - active)
        active += added
        answer += added
        expires[hour + k] += added
    return answer
