def solution(x, n):
    answer = []
    for i in range(1, n + 1):
        answer.append(x * i)
    return answer

# 전체 코드 줄별 설명
# def solution(x, n):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. x: 시작 숫자이자 증가 간격, n: 만들어야 할 숫자의 개수
#     answer = []  # []는 리스트. =는 값 저장. 결과 숫자들을 저장할 빈 리스트 생성
#     for i in range(1, n + 1):  # for·in은 원소를 차례로 꺼내는 반복문. range는 끝값 직전까지 정수 순서 생성. i를 1부터 n까지 1씩 증가시키면서 반복
#         answer.append(x * i)  # append는 리스트 끝에 추가. x에 i를 곱한 값을 리스트 맨 뒤에 추가
#     return answer  # return은 결과를 돌려주고 함수 종료. 완성된 숫자 리스트를 반환

# 풀이 요약
# x부터 시작해 x의 1배, 2배, …, n배를 차례로 저장한다. x가 음수여도 곱셈으로 같은 간격의 수열을 만들 수 있다.
# 반환 원소 N개: 시간·공간 O(N).
