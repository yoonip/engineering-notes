# 문제: 전화번호 목록
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/42577
# 풀이: 번호를 사전순으로 정렬한다. 접두어 관계인 번호는 붙어서 나타나므로 인접한 번호만 비교한다.
# 복잡도: 번호 N개·최대 길이 L: 시간 O(LN log N), 정렬 추가 공간 O(N).

def solution(phone_book):
    phone_book.sort()
    for index in range(len(phone_book) - 1):
        if phone_book[index + 1].startswith(phone_book[index]):
            return False
    return True
