def solution(phone_book):
    phone_book.sort()
    for index in range(len(phone_book) - 1):
        if phone_book[index + 1].startswith(phone_book[index]):
            return False
    return True

# 전체 코드 줄별 설명
# def solution(phone_book):  # def는 함수 정의. phone_book은 전화번호 문자열 목록.
#     phone_book.sort()  # sort는 제자리 사전순 정렬. 접두어가 같은 번호들이 붙게 됨.
#     for index in range(len(phone_book) - 1):  # len은 길이, range는 끝 미포함. 인접한 두 번호의 앞 인덱스 순회.
#         if phone_book[index + 1].startswith(phone_book[index]):  # []는 접근, startswith는 접두어 검사. 바로 다음 번호가 앞 번호로 시작하는지 확인.
#             return False  # False는 거짓. 접두어 관계가 하나라도 있으면 즉시 반환.
#     return True  # True는 참. 모든 인접 쌍을 통과하면 접두어 관계 없음.

# 풀이 요약
# 사전순 정렬에서 어떤 번호를 접두어로 가진 번호는 바로 뒤에 모이므로 인접 쌍만 비교하면 됩니다.
# 예: 119 뒤의 1195524421이 119로 시작해 False. 번호 N개·최대 길이 L일 때 시간 O(LN log N), 정렬 공간 O(N).
