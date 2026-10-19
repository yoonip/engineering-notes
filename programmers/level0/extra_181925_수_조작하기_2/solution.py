def solution(numLog):
    controls = {1: 'w', -1: 's', 10: 'd', -10: 'a'}
    return ''.join(controls[b - a] for a, b in zip(numLog, numLog[1:]))

# 전체 코드 줄별 설명
# def solution(numLog):  # def는 함수 정의. 수의 변화 기록 리스트 입력.
#     controls = {1: 'w', -1: 's', 10: 'd', -10: 'a'}  # 딕셔너리는 키를 값에 연결. 변화량을 조작 문자에 대응.
#     return ''.join(controls[b - a] for a, b in zip(numLog, numLog[1:]))  # [1:]은 첫 원소 제외, zip은 인접 값들을 묶음. 차이로 문자를 찾아 join으로 연결.

# 풀이 요약
# 인접 기록의 차이가 어떤 조작에 해당하는지 역으로 찾아 연결합니다.
# 