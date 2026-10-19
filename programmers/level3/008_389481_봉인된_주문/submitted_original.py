def solution(n, bans):
    removed = []
    for word in bans:
        value = 0
        for letter in word:
            value = value * 26 + ord(letter) - ord('a') + 1
        removed.append(value)
    removed.sort()
    for value in removed:
        if value <= n:
            n += 1
        else:
            break
    letters = []
    while n:
        n, digit = divmod(n - 1, 26)
        letters.append(chr(ord('a') + digit))
    return ''.join(reversed(letters))

# 전체 코드 줄별 설명
# def solution(n, bans):  # def는 함수 정의. n은 삭제 후 순번, bans는 삭제된 주문 문자열 목록.
#     removed = []  # []는 빈 리스트. 삭제 주문의 원래 순번을 저장.
#     for word in bans:  # for~in으로 삭제 주문 하나씩 순회.
#         value = 0  # 원래 순번을 계산할 누적값 초기화.
#         for letter in word:  # 주문의 각 문자를 왼쪽부터 순회.
#             value = value * 26 + ord(letter) - ord('a') + 1  # ord는 문자 번호 반환. a=1~z=26인 26진수처럼 앞자리 값을 26배 해 더함.
#         removed.append(value)  # append는 리스트 끝에 원소 하나 추가.
#     removed.sort()  # sort는 원본 리스트를 오름차순으로 정렬.
#     for value in removed:  # 앞에서 삭제된 주문부터 순회.
#         if value <= n:  # if는 조건문, <=는 이하. 찾으려는 원래 위치 앞의 삭제인지 검사.
#             n += 1  # +=는 더해 저장. 삭제된 주문 하나를 건너뛰기 위해 목표 원래 순번을 한 칸 뒤로 이동.
#         else:  # else는 뒤쪽 삭제인 경우.
#             break  # break는 반복 종료. 정렬돼 있으므로 나머지 삭제도 영향을 주지 않음.
#     letters = []  # 정답 주문의 문자들을 뒷자리부터 담을 리스트.
#     while n:  # while은 조건이 참인 동안 반복. 정수 0은 거짓.
#         n, digit = divmod(n - 1, 26)  # divmod는 (몫, 나머지). 1~26 표기를 0~25로 바꾸기 위해 먼저 1을 뺌.
#         letters.append(chr(ord('a') + digit))  # chr는 문자 번호를 문자로 변환. 나머지를 a~z로 바꿔 추가.
#     return ''.join(reversed(letters))  # reversed는 역순 순회, 빈 문자열의 join은 문자들을 이어 붙임. return으로 주문 반환.

# 풀이 요약
# 각 주문을 a=1~z=26인 자릿수로 해석하면 길이 우선·사전순과 같은 원래 순번을 얻습니다.
# 삭제 순번을 정렬해 목표 앞의 삭제를 하나씩 건너뛴 후, 원래 순번을 다시 문자열로 바꿉니다. 주문 길이 L·삭제 수 B에 대해 시간 O(BL+B log B), 공간 O(B).
# 예: 30번째를 찾을 때 d·e·aa·ae가 앞에서 삭제되므로 원래 34번째 주문 ah를 반환합니다.
