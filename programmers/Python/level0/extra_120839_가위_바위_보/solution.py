def solution(rsp):
    wins = {'2': '0', '0': '5', '5': '2'}
    return ''.join(wins[char] for char in rsp)

# 전체 코드 줄별 설명
# def solution(rsp):  # def는 함수 정의. 가위·바위·보를 표시한 문자열 입력.
#     wins = {'2': '0', '0': '5', '5': '2'}  # {}는 딕셔너리. 각 상대 값에 이기는 값을 대응.
#     return ''.join(wins[char] for char in rsp)  # []로 이기는 값 조회. 생성기 표현식 결과를 join으로 입력 순서대로 연결.

# 풀이 요약
# 가위에는 바위, 바위에는 보, 보에는 가위를 대응시킵니다.
# 