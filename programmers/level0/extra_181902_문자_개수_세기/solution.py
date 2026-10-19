def solution(my_string):
    counts = [0] * 52
    for char in my_string:
        index = ord(char) - ord('A') if char.isupper() else ord(char) - ord('a') + 26
        counts[index] += 1
    return counts

# 전체 코드 줄별 설명
# def solution(my_string):  # def는 함수 정의. 알파벳 대소문자 문자열 입력.
#     counts = [0] * 52  # []는 리스트, *는 반복. 대문자 26개와 소문자 26개의 개수 초기화.
#     for char in my_string:  # for로 각 문자 순회.
#         index = ord(char) - ord('A') if char.isupper() else ord(char) - ord('a') + 26  # ord는 문자 코드, isupper는 대문자 검사. 대문자는 0~25, 소문자는 26~51로 변환.
#         counts[index] += 1  # []로 해당 위치 접근, +=는 더해 저장. 현재 문자 출현 횟수 증가.
#     return counts  # 정해진 알파벳 순서의 개수 리스트 반환.

# 풀이 요약
# 대문자와 소문자에 서로 다른 인덱스 구간을 배정해 출현 횟수를 셉니다.
# 