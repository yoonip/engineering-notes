def solution(arr, divisor):  # 숫자 목록과 나눌 숫자를 받음
    answer = []  # 조건에 맞는 숫자들을 담을 리스트

    for number in arr:  # 숫자를 하나씩 꺼냄
        if number % divisor == 0:  # 나누어떨어진다면
            answer.append(number)  # 결과에 추가

    if len(answer) == 0:  # 모든 숫자를 확인했는데 결과가 비었다면
        return [-1]  # 조건에 맞는 숫자가 없다는 답을 반환

    answer.sort()  # 남긴 숫자들을 작은 순서로 정렬
    return answer  # 정렬된 리스트를 반환

# def solution(arr, divisor):       # 숫자 배열 arr와 나눌 수 divisor를 입력받습니다.
#     answer = []                  # 조건에 맞는 숫자를 담을 빈 리스트를 만듭니다.
#     for num in arr:              # arr에서 숫자를 하나씩 꺼내 num에 넣습니다.
#         if num % divisor == 0:   # %는 나머지입니다. 나머지가 0인지 확인합니다.
#             answer.append(num)   # 나누어떨어지는 숫자를 answer 끝에 추가합니다.
#     if not answer:               # answer가 빈 리스트이면 실행합니다.
#         return [-1]              # 정수가 아닌, -1을 담은 리스트를 반환합니다.
#     return sorted(answer)        # 숫자를 오름차순으로 정렬한 리스트를 반환합니다.


def solution(arr, divisor):
    answer = []
    
    for number in arr:
        if number % divisor ==0:
            answer.append(number)
    
    if len(answer) ==0:
        return [-1]
    
    answer.sort()
    return answer

    