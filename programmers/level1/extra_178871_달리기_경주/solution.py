def solution(players, callings):
    position = {}
    for i, name in enumerate(players):
        position[name] = i
    for name in callings:
        i = position[name]
        front = players[i - 1]
        players[i - 1], players[i] = players[i], players[i - 1]
        position[name] = i - 1
        position[front] = i
    return players

# 전체 코드 줄별 설명
# def solution(players, callings):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. 현재 선수 순서와 추월 호출을 입력받음.
#     position = {}  # {}는 키:값을 저장하는 딕셔너리. =는 값 저장. 선수 이름별 현재 위치를 저장할 딕셔너리.
#     for i, name in enumerate(players):  # for·in은 원소를 차례로 꺼내는 반복문. enumerate는 인덱스·값을 함께 제공. ()로 묶은 여러 값은 변경 불가 튜플. 선수의 위치와 이름을 함께 읽음.
#         position[name] = i  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. =는 값 저장. 이름에 해당하는 현재 위치 저장.
#     for name in callings:  # for·in은 원소를 차례로 꺼내는 반복문. 추월하는 선수의 이름을 순서대로 확인.
#         i = position[name]  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. =는 값 저장. 추월할 선수의 현재 위치 조회.
#         front = players[i - 1]  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. =는 값 저장. 바로 앞 선수의 이름을 보관.
#         players[i - 1], players[i] = players[i], players[i - 1]  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. =는 값 저장. 두 선수의 배열 위치를 동시에 교환.
#         position[name] = i - 1  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. =는 값 저장. 추월한 선수의 딕셔너리 위치 갱신.
#         position[front] = i  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. =는 값 저장. 뒤로 밀린 선수의 위치도 갱신.
#     return players  # return은 결과를 돌려주고 함수 종료. 모든 추월 후 선수 순서 반환.

# 풀이 요약
# 선수 이름별 현재 배열 위치를 딕셔너리에 저장한다. 이름이 불리면 앞 선수와 배열 원소 두 개를 교환하고 두 사람의 위치 정보도 갱신한다. 매번 이름을 배열에서 다시 찾지 않아 호출 한 번을 평균 상수 시간에 처리한다.
# 선수 P명, 호출 C번: 평균 시간 O(P+C), 공간 O(P). 선수 리스트를 직접 바꾼다.
