def solution(arr, k):
    unique = list(dict.fromkeys(arr))[:k]
    return unique + [-1] * (k - len(unique))

# 전체 코드 줄별 설명
# def solution(arr, k):  # def는 함수 정의. 숫자 리스트와 목표 길이 입력.
#     unique = list(dict.fromkeys(arr))[:k]  # dict.fromkeys는 각 값을 키로 하는 딕셔너리 생성. 중복을 제거하며 처음 등장 순서 유지. list로 변환 후 앞 k개 선택.
#     return unique + [-1] * (k - len(unique))  # len은 길이, 리스트 * 횟수는 반복, +는 연결. 부족한 개수만큼 -1 추가.

# 풀이 요약
# 처음 등장한 서로 다른 수를 k개까지 남기고 부족한 자리는 -1로 채웁니다.
# 