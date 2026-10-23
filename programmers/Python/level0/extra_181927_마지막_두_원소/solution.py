def solution(num_list):
    last, previous = num_list[-1], num_list[-2]
    return num_list + [last - previous if last > previous else last * 2]

# 전체 코드 줄별 설명
# def solution(num_list):  # def는 함수 정의. 정수 리스트 입력.
#     last, previous = num_list[-1], num_list[-2]  # 음수 인덱스 -1은 마지막, -2는 끝에서 두 번째 원소.
#     return num_list + [last - previous if last > previous else last * 2]  # 조건 표현식으로 추가 값 선택. []로 한 원소 리스트를 만들고 +로 연결.

# 풀이 요약
# 마지막 값이 더 크면 차이를, 아니면 마지막 값의 두 배를 뒤에 추가합니다.
# 