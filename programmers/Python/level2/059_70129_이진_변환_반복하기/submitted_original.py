def solution(s):
    conversions = removed = 0
    while s != '1':
        ones = s.count('1')
        removed += len(s) - ones
        s = bin(ones)[2:]
        conversions += 1
    return [conversions, removed]

# 전체 코드 줄별 설명
# def solution(s):  # def는 함수 정의, s는 0·1 문자열 입력.
#     conversions = removed = 0  # 연쇄 대입으로 변환 횟수·제거한 0 수 초기화.
#     while s != '1':  # while은 반복, !=는 다름. 문자열이 '1'이 될 때까지 진행.
#         ones = s.count('1')  # count는 해당 문자 수. 0을 지운 뒤 남는 길이는 1 개수.
#         removed += len(s) - ones  # len은 길이, +=는 더해 저장. 현재 제거되는 0 개수 누적.
#         s = bin(ones)[2:]  # bin은 '0b' 접두사가 있는 이진 문자열 생성. [2:] 슬라이스로 접두사 제거.
#         conversions += 1  # 한 번 변환했으므로 횟수 증가.
#     return [conversions, removed]  # [] 리스트에 횟수·제거 수를 묶어 return으로 반환.

# 풀이 요약
# 1의 개수를 세어 남은 길이를 구하고 그 길이를 이진수로 바꾸는 과정을 반복합니다.
# 예: '110010101001'은 세 번 변환하며 0 여덟 개를 제거해 [3,8]. 초기 길이 N일 때 시간·공간 O(N).
