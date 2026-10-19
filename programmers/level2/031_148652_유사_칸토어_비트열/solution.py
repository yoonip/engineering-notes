def solution(n, l, r):
    def prefix(level, length):
        if level == 0:
            return length
        block = 5 ** (level - 1)
        groups, rest = divmod(length, block)
        full = groups - int(groups > 2)
        total = full * 4 ** (level - 1)
        if groups == 2:
            return total
        return total + prefix(level - 1, rest)
    return prefix(n, r) - prefix(n, l - 1)

# 전체 코드 줄별 설명
# def solution(n, l, r):  # def는 함수 정의. n은 단계, l·r은 1부터 세는 구간 양끝 입력.
#     def prefix(level, length):  # 중첩 함수. 해당 단계의 앞 length개 비트에 포함된 1의 수 계산.
#         if level == 0:  # if는 조건 분기, ==는 같음. 0단계 비트열은 '1'.
#             return length  # 길이 0이면 0, 길이 1이면 1 반환.
#         block = 5 ** (level - 1)  # **는 거듭제곱, ()는 연산 묶음. 이전 단계 한 덩어리의 길이.
#         groups, rest = divmod(length, block)  # divmod는 몫·나머지 반환. 온전한 덩어리 수와 남은 길이로 언패킹.
#         full = groups - int(groups > 2)  # int는 참을 1로 변환. 가운데 0 덩어리까지 지났다면 1 덩어리 수에서 제외.
#         total = full * 4 ** (level - 1)  # *는 곱셈. 온전한 유효 덩어리마다 이전 단계의 1 개수 합산.
#         if groups == 2:  # 남은 부분이 가운데 0 덩어리 안에 있으면 추가 1이 없음.
#             return total  # 온전한 덩어리의 합만 반환.
#         return total + prefix(level - 1, rest)  # 나머지 부분은 한 단계 줄여 재귀 호출한 결과를 더함.
#     return prefix(n, r) - prefix(n, l - 1)  # 앞 r개에서 앞 l-1개를 빼 폐구간 [l,r]의 1 개수 반환.

# 풀이 요약
# 비트열은 이전 단계 네 덩어리와 가운데 0 덩어리로 나뉩니다. 완전한 덩어리는 4의 거듭제곱으로 세고 남은 부분만 재귀 처리합니다.
# 예: n=2의 [4,17]은 8개. 비트열을 직접 만들지 않으며 시간·재귀 공간 O(n).
