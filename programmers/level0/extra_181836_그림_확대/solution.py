def solution(picture, k):
    answer = []
    for row in picture:
        expanded = ''.join(char * k for char in row)
        answer.extend([expanded] * k)
    return answer

# 전체 코드 줄별 설명
# def solution(picture, k):  # def는 함수 정의. 그림의 행 문자열 리스트와 확대 배율 입력.
#     answer = []  # []는 빈 리스트. 확대된 행 저장.
#     for row in picture:  # for로 각 행 문자열 순회.
#         expanded = ''.join(char * k for char in row)  # 문자 * 정수는 반복. 각 픽셀을 가로로 k번 반복한 뒤 join으로 연결.
#         answer.extend([expanded] * k)  # 같은 확대 행을 세로로 k번 반복. extend로 여러 행을 결과에 추가.
#     return answer  # 가로·세로 모두 k배로 확대한 그림 반환.

# 풀이 요약
# 문자를 k번 반복해 가로 확대하고 완성된 행을 k번 반복해 세로 확대합니다.
# 