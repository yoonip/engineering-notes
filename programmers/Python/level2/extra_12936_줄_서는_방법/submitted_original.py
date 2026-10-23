from math import factorial

def solution(n, k):
    available = list(range(1, n + 1))
    answer = []
    k -= 1
    block = factorial(n)
    for remaining in range(n, 0, -1):
        block //= remaining
        index, k = divmod(k, block)
        answer.append(available.pop(index))
    return answer

# 전체 코드 줄별 설명
# from math import factorial  # import는 도구 가져오기. factorial(n)은 1부터 n까지의 곱 n!, 0!은 1. 순열 개수 계산에 사용.
# 
# def solution(n, k):  # def는 함수 정의. 사람 수와 1부터 세는 사전순 순번 입력.
#     available = list(range(1, n + 1))  # range는 끝 제외한 정수 범위, list는 리스트 변환. 아직 배치하지 않은 번호를 오름차순으로 보관.
#     answer = []  # []는 결과 순열 리스트.
#     k -= 1  # -=는 빼서 저장. 순번을 0부터 세는 인덱스로 변환해 경계 계산을 단순화.
#     block = factorial(n)  # 현재 남은 모든 순열 개수.
#     for remaining in range(n, 0, -1):  # range의 세 번째 -1은 감소. 남은 사람 수를 n부터 1까지 줄임.
#         block //= remaining  # //=는 정수 나눗셈 후 저장. 첫 번호 하나를 고정한 묶음 크기는 (remaining-1)!.
#         index, k = divmod(k, block)  # divmod는 몫·나머지. 몫은 선택할 번호 위치, 나머지는 그 묶음 안 순번.
#         answer.append(available.pop(index))  # pop(index)는 해당 원소를 꺼내 삭제. append는 결과 끝에 추가.
#     return answer  # k번째 줄서기 순열 반환.

# 풀이 요약
# 첫 사람 하나를 고정하면 뒤에는 (N-1)!가지가 있다. k를 묶음 크기로 나눈 몫으로 첫 사람을 고르고 나머지 순번으로 다음 자리를 찾는다.
# 예: n=3,k=5를 0부터 세면 4. 묶음 크기 2에서 몫 2라 첫 번호 3, 나머지 0이라 이후 [1,2]. 시간 O(N²), 공간 O(N).
# 