def solution(intStrs, k, s, l):
    answer = []
    for text in intStrs:
        value = int(text[s:s + l])
        if value > k:
            answer.append(value)
    return answer

# 전체 코드 줄별 설명
# def solution(intStrs, k, s, l):  # def는 함수 정의. 숫자 문자열 리스트·기준값·시작 인덱스·길이 입력.
#     answer = []  # []는 빈 리스트. 조건을 만족하는 정수 저장.
#     for text in intStrs:  # for로 각 문자열 순회.
#         value = int(text[s:s + l])  # [시작:끝]은 끝 제외 슬라이싱. int로 잘라낸 길이 l의 문자열을 정수로 변환.
#         if value > k:  # if는 조건, >는 초과 비교. 기준보다 큰지 검사.
#             answer.append(value)  # append로 결과 끝에 정수 추가.
#     return answer  # 입력 순서의 결과 리스트 반환.

# 풀이 요약
# 각 문자열에서 필요한 부분만 잘라 정수로 바꾸고 k보다 큰 값을 남깁니다.
# 