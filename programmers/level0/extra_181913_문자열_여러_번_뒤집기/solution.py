def solution(my_string, queries):
    chars = list(my_string)
    for start, end in queries:
        chars[start:end + 1] = chars[start:end + 1][::-1]
    return ''.join(chars)

# 전체 코드 줄별 설명
# def solution(my_string, queries):  # def는 함수 정의. 문자열과 뒤집을 범위 쿼리 입력.
#     chars = list(my_string)  # list는 문자열을 문자 리스트로 변환. 문자열과 달리 일부 구간 수정 가능.
#     for start, end in queries:  # 각 쿼리의 양 끝 인덱스를 나누어 받음.
#         chars[start:end + 1] = chars[start:end + 1][::-1]  # 슬라이싱은 끝 제외. [::-1]은 역순 복사. 해당 구간만 역순으로 대입.
#     return ''.join(chars)  # join으로 수정된 문자 리스트를 문자열로 연결하여 반환.

# 풀이 요약
# 끝 인덱스를 포함하도록 end+1까지 잘라 뒤집고 원래 위치에 넣습니다.
# 