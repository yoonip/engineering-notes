# 두 가지 펄스를 각각 적용하며 현재 위치에서 끝나는 최대 부분합을 갱신합니다. 누적합의 최댓값·최솟값 차이를 쓰는 기본
# 풀이와 달리 부분수열을 직접 연장할지 결정합니다.
def solution(sequence):
    positive = negative = float('-inf')
    answer = float('-inf')
    for index, value in enumerate(sequence):
        pulse = value if index%2==0 else -value
        positive = max(pulse, positive+pulse)
        negative = max(-pulse, negative-pulse)
        answer = max(answer, positive, negative)
    return answer
