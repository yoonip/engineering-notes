def solution(myString, pat):
    changed = ''.join('B' if char == 'A' else 'A' for char in myString)
    return int(pat in changed)

# 전체 코드 줄별 설명
# def solution(myString, pat):  # def는 함수 정의. A·B 문자열과 찾을 패턴 입력.
#     changed = ''.join('B' if char == 'A' else 'A' for char in myString)  # 조건 표현식으로 A·B를 교환. 생성기 표현식 결과를 join으로 연결.
#     return int(pat in changed)  # in은 부분 문자열 포함 검사. int는 참·거짓을 1·0으로 변환.

# 풀이 요약
# 한 번의 문자 순회에서 A와 B를 바꾸어 이미 바꾼 문자를 다시 치환하는 실수를 피합니다.
# 