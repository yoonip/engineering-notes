def solution(numbers):
    answer = 45 - sum(numbers)
    return answer

# 전체 코드 줄별 설명
# def solution(numbers):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. 0~9 중 일부 숫자가 담긴 리스트를 입력받음
#     answer = 45 - sum(numbers)  # sum은 원소 합. =는 값 저장. 0부터 9까지의 합 45에서 리스트에 존재하는 숫자의 합을 뺌
#     return answer  # return은 결과를 돌려주고 함수 종료. 리스트에 없는 숫자들의 합을 반환

# 풀이 요약
# 0~9의 합은 45다. 입력 숫자는 중복되지 않으므로 45에서 입력 합을 빼면 빠진 숫자들의 합만 남는다.
# 입력 길이 N: 시간 O(N), 보조 공간 O(1).
