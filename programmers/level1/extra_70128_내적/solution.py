def solution(a, b):
    answer = 0
    for x, y in zip(a, b):
        answer += x * y
    return answer

# 전체 코드 줄별 설명
# def solution(a, b):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. 두 정수 배열 a와 b를 입력받는 함수
#     answer = 0  # =는 값 저장. 내적 결과를 저장할 변수를 0으로 초기화
#     for x, y in zip(a, b):  # for·in은 원소를 차례로 꺼내는 반복문. zip은 같은 위치의 값들을 짝지음. ()로 묶은 여러 값은 변경 불가 튜플. zip()으로 두 배열의 같은 위치에 있는 값을 묶어 순회
#         answer += x * y  # +=는 더하거나 연결한 값을 저장. 같은 위치의 두 숫자를 곱해서 answer에 누적
#     return answer  # return은 결과를 돌려주고 함수 종료. 계산한 내적 결과 반환

# 풀이 요약
# 같은 위치의 원소끼리 곱한 값을 더하면 내적이다. zip이 두 배열의 대응 원소를 한 쌍씩 꺼내므로 별도의 인덱스 관리가 필요 없다.
# 배열 길이 N: 시간 O(N), 보조 공간 O(1).
