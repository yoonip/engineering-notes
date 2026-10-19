def solution(number, k):
    stack = []
    for digit in number:
        while k > 0 and stack and stack[-1] < digit:
            stack.pop()
            k -= 1
        stack.append(digit)
    if k > 0:
        stack = stack[:-k]
    return ''.join(stack)

# 전체 코드 줄별 설명
# def solution(number, k):  # def는 함수 정의. 숫자 문자열·지울 자릿수 입력.
#     stack = []  # []는 빈 리스트. 남길 숫자들을 스택으로 저장.
#     for digit in number:  # for~in으로 숫자 문자를 왼쪽부터 순회.
#         while k > 0 and stack and stack[-1] < digit:  # while은 반복, and는 모두 참, [-1]은 마지막 원소. 더 큰 뒷 숫자가 오면 작은 앞 숫자 제거.
#             stack.pop()  # pop은 마지막 원소를 꺼내 삭제.
#             k -= 1  # -=는 빼서 저장. 남은 삭제 횟수 감소.
#         stack.append(digit)  # append로 현재 숫자 추가. 같은 자리 문자 비교는 숫자 크기 순서와 같음.
#     if k > 0:  # if는 분기. 내림차순 숫자 등으로 삭제 횟수가 남았는지 검사.
#         stack = stack[:-k]  # [:-k] 슬라이스로 마지막 k개를 제외. 앞자리 큰 숫자를 보존.
#     return ''.join(stack)  # join으로 숫자 문자들을 연결해 return으로 반환.

# 풀이 요약
# 뒤에서 더 큰 숫자가 나오면 지울 수 있는 만큼 앞의 작은 숫자를 스택에서 제거합니다. 삭제가 남으면 끝에서 지웁니다.
# 예: 1924에서 1·2를 지우면 94. 각 자릿수는 한 번씩 추가·제거되므로 시간·공간 O(N).
