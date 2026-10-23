# s는 0과 1 문자열들의 리스트.
def solution(s):
    # 각 문자열의 최종 결과를 저장.
    answer = []
    # for로 문자열을 하나씩 순회.
    for word in s:
        # 마지막에 넣은 문자를 먼저 꺼내는 스택을 리스트로 구현.
        stack = []
        # 추출한 110의 개수.
        count = 0
        # 문자열의 글자를 왼쪽부터 하나씩 읽음.
        for char in word:
            # append는 리스트 끝에 추가.
            stack.append(char)
            # len은 길이, and는 모두 참, [-3:]는 끝 세 글자, ==는 같음.
            if len(stack) >= 3 and stack[-3:] == ['1', '1', '0']:
                # 끝의 110을 제거하면 새로 이어진 부분도 이후에 확인 가능.
                del stack[-3:]
                # 추출 개수 증가.
                count += 1
        # join은 글자 목록을 구분자 없이 이어 문자열로 만듦.
        remaining = ''.join(stack)
        # 마지막 0 바로 뒤를 삽입 위치로 선택.
        index = remaining.rfind('0') + 1
        # 추출한 110을 한곳에 삽입.
        answer.append(remaining[:index] + '110' * count + remaining[index:])
    # return은 결과 반환.
    return answer
