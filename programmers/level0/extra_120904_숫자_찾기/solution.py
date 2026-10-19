def solution(num, k):
    position = str(num).find(str(k))
    return position + 1 if position != -1 else -1

# 전체 코드 줄별 설명
# def solution(num, k):  # def는 함수 정의. 검사할 정수와 찾을 한 자리 숫자 입력.
#     position = str(num).find(str(k))  # str은 문자열 변환, find는 처음 나타난 인덱스 반환. 없으면 -1.
#     return position + 1 if position != -1 else -1  # 조건 표현식, !=는 다름 비교. 찾았을 때만 0부터 세는 인덱스를 1부터 세는 순번으로 변환.

# 풀이 요약
# 정수를 문자열로 바꾸어 숫자 문자의 첫 위치를 찾습니다.
# 