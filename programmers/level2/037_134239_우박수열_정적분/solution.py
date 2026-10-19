# 문제: 우박수열 정적분
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/134239
# 풀이: 인접한 우박수열 점의 사다리꼴 넓이를 누적한다. 각 질의는 두 누적값의 차로 계산해 구간마다 다시 적분하지 않는다.
# 복잡도: 우박수열 길이 L·질의 Q개: 시간 O(L+Q), 반환값을 제외한 추가 공간 O(L).

def solution(k, ranges):
    prefix = [0.0]
    while k > 1:
        next_value = k // 2 if k % 2 == 0 else 3 * k + 1
        prefix.append(prefix[-1] + (k + next_value) / 2)
        k = next_value
    n = len(prefix) - 1
    answer = []
    for start, offset in ranges:
        end = n + offset
        answer.append(prefix[end] - prefix[start] if start <= end else -1.0)
    return answer
