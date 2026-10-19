
def solution(n, arr1, arr2):
    answer = []

    for a, b in zip(arr1, arr2):
        combined = a | b
        binary = bin(combined)[2:].zfill(n)
        row = binary.replace("1", "#").replace("0", " ")
        answer.append(row)

    return answer


# ========== 공부용 코드 (전체 주석 처리) ==========

# def solution(n, arr1, arr2):                  # 지도 크기 n과 두 개의 지도 배열을 입력받음
#     answer = []                              # 완성된 지도의 각 행을 저장할 빈 리스트
#
#     for a, b in zip(arr1, arr2):            # 두 지도에서 같은 위치의 숫자 a, b를 하나씩 가져옴
#         combined = a | b                    # 비트 OR 연산으로 두 지도를 합침 (하나라도 1이면 1)
#         binary = bin(combined)[2:].zfill(n)  # 2진수로 변환하고 0b 제거 후 앞에 0을 채워 길이를 n으로 맞춤
#         row = binary.replace("1", "#").replace("0", " ")  # 숫자 1은 벽(#), 0은 공백으로 변환
#         answer.append(row)                   # 변환한 한 행을 정답 리스트에 추가
#
#     return answer                            # 완성된 지도를 문자열 리스트로 반환
