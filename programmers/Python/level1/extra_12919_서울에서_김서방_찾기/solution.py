def solution(seoul):
    index = seoul.index("Kim")
    answer = f"김서방은 {index}에 있다"
    return answer

# 전체 코드 줄별 설명
# def solution(seoul):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. 서울 사람들의 이름 리스트를 입력받음.
#     index = seoul.index("Kim")  # index는 값이 처음 나오는 위치. =는 값 저장. Kim이 있는 위치를 찾음.
#     answer = f"김서방은 {index}에 있다"  # f-string의 {} 안에 계산한 값 삽입. =는 값 저장. 찾은 위치를 문장 안에 넣음.
#     return answer  # return은 결과를 돌려주고 함수 종료. 완성된 안내 문장 반환.

# 풀이 요약
# index로 Kim이 있는 0부터 시작하는 위치를 구한다. f-string의 중괄호에 그 위치를 넣어 문제에서 지정한 문장을 만든다.
# 이름 수 N: 검색 시간 O(N), 보조 공간 O(1). 결과 문자열은 별도다.
