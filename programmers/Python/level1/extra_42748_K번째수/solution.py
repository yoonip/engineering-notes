def solution(array, commands):
    answer = []
    for command in commands:
        start = command[0]
        end = command[1]
        k = command[2]
        numbers = []
        for index in range(start - 1, end):
            numbers.append(array[index])
        numbers.sort()
        number = numbers[k - 1]
        answer.append(number)
    return answer

# 전체 코드 줄별 설명
# def solution(array, commands):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. array: 원본 숫자 배열, commands: [i, j, k] 명령들의 목록
#     answer = []  # []는 리스트. =는 값 저장. 각 명령에서 구한 K번째 숫자를 저장할 빈 리스트
#     for command in commands:  # for·in은 원소를 차례로 꺼내는 반복문. 각 구간 질의의 시작·끝·선택 순위를 처리.
#         start = command[0]  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. =는 값 저장. 질의의 시작 위치를 읽음.
#         end = command[1]  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. =는 값 저장. 질의의 마지막 위치를 읽음.
#         k = command[2]  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. =는 값 저장. 정렬한 구간에서 고를 순위.
#         numbers = []  # []는 리스트. =는 값 저장. 이번 구간의 값을 모을 리스트.
#         for index in range(start - 1, end):  # for·in은 원소를 차례로 꺼내는 반복문. range는 끝값 직전까지 정수 순서 생성. 문제의 1부터 시작하는 구간을 배열 인덱스로 변환.
#             numbers.append(array[index])  # append는 리스트 끝에 추가. []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. 해당 구간 원소를 복사.
#         numbers.sort()  # sort는 원래 리스트 정렬. 잘라낸 숫자들을 오름차순(작은 숫자부터 큰 숫자 순서)으로 정렬
#         number = numbers[k - 1]  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. =는 값 저장. 정렬한 배열에서 k번째 값을 선택.
#         answer.append(number)  # append는 리스트 끝에 추가. 이 질의의 결과를 추가.
#     return answer  # return은 결과를 돌려주고 함수 종료. 모든 명령의 결과를 순서대로 반환

# 풀이 요약
# 질의의 시작·끝 위치로 구간을 복사하고 정렬한 뒤 k번째를 읽는다. 문제의 위치는 1부터 시작하므로 배열 접근은 1을 뺀다. 끝 위치를 포함하려면 range의 끝값은 문제의 end 그대로 둔다.
# 질의 구간 길이 L_i: 시간 O(Σ L_i log(L_i+1)), 보조 공간 O(max L_i). 결과 리스트는 질의 수만큼 필요하다.
