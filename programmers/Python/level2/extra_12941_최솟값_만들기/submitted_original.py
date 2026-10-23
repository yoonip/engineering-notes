def solution(A, B):
    small_first = sorted(A)
    large_first = sorted(B, reverse=True)
    return sum(a * b for a, b in zip(small_first, large_first))

# 전체 코드 줄별 설명
# def solution(A, B):  # def는 함수 정의. 같은 길이의 두 숫자 목록 입력.
#     small_first = sorted(A)  # sorted는 오름차순으로 정렬한 새 리스트 반환. A의 작은 값부터 사용.
#     large_first = sorted(B, reverse=True)  # reverse=True는 내림차순 정렬 옵션. B의 큰 값부터 사용.
#     return sum(a * b for a, b in zip(small_first, large_first))  # zip은 같은 위치끼리 묶기, for의 두 변수는 언패킹. *는 곱셈, sum은 생성식의 곱 합산.

# 풀이 요약
# 작은 수와 큰 수를 짝지어야 큰 수끼리 곱해지는 비용을 줄일 수 있다. 한쪽 오름차순·다른 쪽 내림차순인 그리디 풀이.
# 예: [1,2,4]와 [5,4,4]는 5+8+16=29. a≤b,c≤d이면 ac+bd-(ad+bc)=(b-a)(d-c)≥0이다. 시간 O(N log N), 공간 O(N).
# 