# 문제: 조이스틱
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/42860
# 풀이: 문자 변경 비용과 가로 이동을 나눈다. 연속 A 구간 앞의 두 회귀 경로를 비교하고 같은 구간 안의 불리한 후보는 건너뛴다.
# 복잡도: 이름 길이 N: 시간 O(N), 추가 공간 O(1). 연속 A 구간은 한 번씩만 스캔한다.

def solution(name):
    vertical = sum(min(ord(ch) - ord('A'), ord('Z') - ord(ch) + 1) for ch in name)
    n = len(name)
    horizontal = n - 1
    index = 0
    while index < n:
        next_index = index + 1
        while next_index < n and name[next_index] == 'A':
            next_index += 1
        tail = n - next_index
        horizontal = min(horizontal, 2 * index + tail, index + 2 * tail)
        # 같은 A 구간 내부에서 되돌리면 더 멀어지므로 구간을 한 번만 본다.
        index = next_index
    return vertical + horizontal
