
#def solution(n):
 #   digits = sorted(str(n), reverse=True)

  #  answer = int("".join(digits))

   # return answer

def solution(n):
    digits = []
    text = str(n)

    for digit in text:
        digits.append(digit)  # 글자를 하나씩 리스트에 담기

    digits.sort()     # 작은 순서로 정렬
    digits.reverse()  # 뒤집어서 큰 순서로 만들기

    answer = ""       # 글자를 이어 붙일 빈 문자열

    for digit in digits:
        answer = answer + digit  # 순서대로 이어 붙이기

    return int(answer)  # 완성한 문자열을 정수로 바꿔 반환
    
    
# ========== 공부용 코드 (전체 주석 처리) ==========

# def solution(n):                              # 정수 n을 입력받는 함수
#     digits = sorted(str(n), reverse=True)    # n을 문자열로 변환하고 각 자릿수를 내림차순으로 정렬
#
#     answer = int("".join(digits))             # 정렬된 문자들을 하나의 문자열로 합친 뒤 정수로 변환
#
#     return answer                             # 내림차순으로 정렬된 정수를 반환
