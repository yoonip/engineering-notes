def solution(n):
    digits = []
    while n > 0:
        n, remainder = divmod(n - 1, 3)
        digits.append('124'[remainder])
    return ''.join(reversed(digits))

# 전체 코드 줄별 설명
# def solution(n):  # def는 함수 정의. 변환할 10진수 자연수 입력.
#     digits = []  # []는 리스트. 낮은 자리부터 구한 숫자 글자를 보관.
#     while n > 0:  # while은 조건 반복. 몫이 0이 되면 모든 자리 계산 완료.
#         n, remainder = divmod(n - 1, 3)  # divmod는 몫·나머지 반환. 1을 빼서 1·2·4를 0·1·2 인덱스로 대응시키는 0 없는 3진법 처리.
#         digits.append('124'[remainder])  # 문자열 []는 해당 위치 글자 조회, append는 끝에 추가. 나머지 0→1,1→2,2→4.
#     return ''.join(reversed(digits))  # reversed는 역순, join은 구분자 없이 글자들을 이어 붙임. 낮은 자리부터 모았으므로 뒤집어 반환.

# 풀이 요약
# 각 자리의 기호가 1·2·4인 0 없는 3진법이다. 매번 n-1을 3으로 나눠 나머지 0·1·2를 세 글자에 대응시킨다.
# 예: 6은 (6-1)÷3의 나머지 2로 끝자리 4, 몫 1로 앞자리 1을 얻어 14. 시간·공간 O(log₃N).
# 