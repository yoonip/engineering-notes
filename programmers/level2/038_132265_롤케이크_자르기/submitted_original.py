from collections import Counter

def solution(topping):
    right = Counter(topping)
    left = set()
    answer = 0
    for value in topping:
        left.add(value)
        right[value] -= 1
        if right[value] == 0:
            del right[value]
        if len(left) == len(right):
            answer += 1
    return answer

# 전체 코드 줄별 설명
# from collections import Counter  # collections의 Counter를 import. 원소별 남은 개수를 저장하는 딕셔너리형 자료구조.
# 
# def solution(topping):  # def는 함수 정의, topping은 토핑 번호 목록 입력.
#     right = Counter(topping)  # 처음에는 모든 토핑을 오른쪽 조각에 배치.
#     left = set()  # set()은 중복 없는 빈 집합. 왼쪽에 등장한 토핑 종류 저장.
#     answer = 0  # =는 대입. 공평한 분할 수 초기화.
#     for value in topping:  # for~in으로 토핑을 왼쪽부터 순회.
#         left.add(value)  # add는 집합에 추가. 왼쪽 토핑 종류 갱신.
#         right[value] -= 1  # [키]의 개수 접근, -=는 빼서 저장. 토핑 하나를 오른쪽에서 제외.
#         if right[value] == 0:  # if는 조건 분기, ==는 같음. 이 종류가 오른쪽에 더 없는지 검사.
#             del right[value]  # del은 항목 삭제. 개수 0인 종류가 len에 포함되지 않게 제거.
#         if len(left) == len(right):  # len은 원소 수. 양쪽의 서로 다른 토핑 종류 수 비교.
#             answer += 1  # +=는 더해 저장. 공평한 절단 위치 하나 누적.
#     return answer  # return으로 가능한 분할 수 반환.

# 풀이 요약
# 경계를 한 칸씩 옮기며 왼쪽은 집합, 오른쪽은 개수 표로 종류 수를 유지합니다. 두 종류 수가 같은 경계를 셉니다.
# 예: 첫 예제는 네 번째·다섯 번째 토핑 뒤에서 잘라 2가지. 토핑 N개·종류 U개일 때 시간 O(N), 공간 O(U).
