def solution(a, b):
    start = min(a, b)
    end = max(a, b)
    count = end - start + 1
    return (start + end) * count // 2

# 전체 코드 줄별 설명
# def solution(a, b):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. def: 함수 정의, a와 b를 입력받음
#     start = min(a, b)  # min은 최솟값. =는 값 저장. min(): a와 b 중 작은 값을 start에 저장
#     end = max(a, b)  # max는 최댓값. =는 값 저장. max(): a와 b 중 큰 값을 end에 저장
#     count = end - start + 1  # =는 값 저장. 정수의 개수 계산, 양 끝값을 포함하므로 1을 더함
#     return (start + end) * count // 2  # return은 결과를 돌려주고 함수 종료. //는 내림한 정수 몫. 등차수열의 합 공식으로 계산한 결과 반환

# 풀이 요약
# a와 b 중 작은 수를 시작, 큰 수를 끝으로 둔다. 정수 개수는 끝-시작+1이며, 연속 정수의 합은 (시작+끝)×개수/2다. 음수 구간에서도 같은 식이 성립한다.
# 문제의 정수 범위에서 시간·보조 공간 O(1).
