def solution(name, yearning, photo):
    scores = dict(zip(name, yearning))
    answer = []
    for people in photo:
        total = 0
        for person in people:
            total += scores.get(person, 0)
        answer.append(total)
    return answer

# 전체 코드 줄별 설명
# def solution(name, yearning, photo):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. 이름·그리움 점수·사진들을 입력받음.
#     scores = dict(zip(name, yearning))  # zip은 같은 위치의 값들을 짝지음. dict는 키와 값의 연결을 저장. =는 값 저장. 이름과 점수를 같은 순서로 짝지어 딕셔너리 생성.
#     answer = []  # []는 리스트. =는 값 저장. 사진별 점수 결과 리스트.
#     for people in photo:  # for·in은 원소를 차례로 꺼내는 반복문. 사진 한 장의 사람 목록을 읽음.
#         total = 0  # =는 값 저장. 이 사진의 점수 합 초기화.
#         for person in people:  # for·in은 원소를 차례로 꺼내는 반복문. 사진 속 사람을 한 명씩 확인.
#             total += scores.get(person, 0)  # get은 키 조회와 기본값 지정. +=는 더하거나 연결한 값을 저장. 등록된 점수를 더하고, 없는 사람은 0점으로 처리.
#         answer.append(total)  # append는 리스트 끝에 추가. 사진의 총점을 결과에 저장.
#     return answer  # return은 결과를 돌려주고 함수 종료. 모든 사진의 점수 리스트 반환.

# 풀이 요약
# 이름과 그리움 점수를 딕셔너리로 연결한다. 사진 속 이름마다 점수를 조회해 합한다. 등록되지 않은 이름은 get의 기본값 0으로 처리하므로 사진에 낯선 사람이 있어도 따로 예외 처리가 필요 없다.
# 등록 이름 N개, 사진 속 전체 인원 P명: 평균 시간 O(N+P), 결과 포함 공간 O(N+사진 수).
