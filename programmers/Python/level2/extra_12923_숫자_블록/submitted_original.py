from math import isqrt

def solution(begin, end):
    answer = []
    for value in range(begin, end + 1):
        if value == 1:
            answer.append(0)
            continue
        block = 1
        for divisor in range(2, isqrt(value) + 1):
            if value % divisor == 0:
                partner = value // divisor
                if partner <= 10000000:
                    block = partner
                    break
                block = divisor
        answer.append(block)
    return answer

# 전체 코드 줄별 설명
# from math import isqrt  # import는 도구 가져오기. isqrt는 제곱근의 정수 내림값을 정확하게 반환.
# 
# def solution(begin, end):  # def는 함수 정의. 조회할 도로 구간의 양 끝 입력.
#     answer = []  # []는 구간의 최종 블록 번호 목록.
#     for value in range(begin, end + 1):  # range는 끝 제외이므로 end+1로 마지막 위치까지 포함.
#         if value == 1:  # ==는 같음. 1번 위치에는 어떤 블록도 설치되지 않음.
#             answer.append(0)  # append는 끝에 추가. 초기값 0 유지.
#             continue  # 다음 위치로 이동.
#         block = 1  # 2 이상 위치는 최소한 1번 블록이 설치됨.
#         for divisor in range(2, isqrt(value) + 1):  # 약수는 제곱근까지 짝을 찾아 확인하면 충분.
#             if value % divisor == 0:  # %는 나머지. 나누어떨어지면 약수 쌍 발견.
#                 partner = value // divisor  # //는 정수 나눗셈. 더 큰 쪽 약수 계산.
#                 if partner <= 10000000:  # 실제 존재하는 블록 번호의 최대값 천만 이하인지 검사.
#                     block = partner  # 작은 약수부터 검사하므로 최초로 허용된 큰 약수가 최대 적법 약수.
#                     break  # 더 확인할 필요 없이 약수 반복 종료.
#                 block = divisor  # 큰 약수가 상한을 넘으면 작은 약수라도 저장. 이 후보를 놓치면 소수의 큰 배수에서 틀림.
#         answer.append(block)  # 최종 선택 번호 저장.
#     return answer  # 구간별 블록 배열 반환.

# 풀이 요약
# 위치 x에는 x의 약수 중 자기 자신을 제외하고 천만 이하인 가장 큰 번호가 마지막에 설치된다. x=1은 0이다.
# 예: 8은 4번 블록, 10은 5번 블록. 140000266=14×10000019처럼 큰 쪽 약수가 상한을 넘으면 작은 약수 14가 답이 될 수 있다.
# 구간 길이 M≤5001일 때 시간 O(M√END), 결과 공간 O(M). 큰 범위 전체를 설치하는 시뮬레이션은 하지 않는다.
# 