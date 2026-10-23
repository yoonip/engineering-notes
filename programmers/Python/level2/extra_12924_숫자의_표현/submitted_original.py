def solution(n):
    length, answer = 1, 0
    while length * (length + 1) // 2 <= n:
        remaining = n - length * (length - 1) // 2
        if remaining % length == 0:
            answer += 1
        length += 1
    return answer

# 전체 코드 줄별 설명
# def solution(n):  # def는 함수 정의. 연속한 자연수 합으로 표현할 목표 입력.
#     length, answer = 1, 0  # 언패킹 대입. 연속 구간 길이와 가능한 방법 수 초기화.
#     while length * (length + 1) // 2 <= n:  # while은 조건 반복. //는 정수 나눗셈. 해당 길이의 최소 합 1+...+length가 n 이하인 동안만 검사.
#         remaining = n - length * (length - 1) // 2  # a+(a+1)+...은 length*a+0+...+(length-1). 증가분을 먼저 빼 시작값 곱만 남김.
#         if remaining % length == 0:  # %는 나머지, ==는 같음. 길이로 정확히 나눠지면 자연수 시작값이 존재.
#             answer += 1  # +=는 더해 저장. 이 길이에 해당하는 표현 하나 추가.
#         length += 1  # 다음 연속 구간 길이 확인.
#     return answer  # 가능한 연속 자연수 표현 수 반환.

# 풀이 요약
# 연속 합의 길이가 정해지면 시작값은 하나로 결정된다. n-L(L-1)/2가 L로 나누어지고 시작값이 1 이상인지 검사한다.
# 예: 15는 길이 1·2·3·5에서 각각 15,7+8,4+5+6,1+2+3+4+5로 표현된다. 최대 길이는 O(√N)이므로 시간 O(√N), 공간 O(1).
# 