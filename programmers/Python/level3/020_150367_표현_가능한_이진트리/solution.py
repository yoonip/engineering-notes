# numbers는 표현 가능 여부를 판단할 십진 정수 목록.
def solution(numbers):
    # 포화 이진트리의 중위 순회 문자열을 검사하는 중첩 재귀 함수.
    def valid(bits):
        # 한 노드는 실제·더미 모두 가능한 리프.
        if len(bits) == 1:
            # return으로 이 부분 트리가 유효함을 반환.
            return True
        # 중위 순회에서 가운데 문자가 현재 트리의 루트.
        middle = len(bits) // 2
        # 루트가 더미 노드인 경우.
        if bits[middle] == '0':
            # 더미 아래에는 실제 노드가 하나도 없어야 함.
            return '1' not in bits
        # and는 두 검사 모두 참이어야 참.
        return valid(bits[:middle]) and valid(bits[middle + 1:])

    # []는 결과를 순서대로 담을 빈 리스트.
    answer = []
    # for~in으로 입력 정수 순회.
    for number in numbers:
        # [2:]로 접두사를 제거.
        bits = bin(number)[2:]
        size = 1
        # 이진 문자열 전체를 담을 크기까지 늘림.
        while size < len(bits):
            # 한 층을 늘리면 이전 크기의 두 배+루트 한 개.
            size = size * 2 + 1
        # 십진 값은 유지하면서 포화 트리 모양으로 맞춤.
        bits = bits.zfill(size)
        # append는 결과 하나 추가.
        answer.append(int(valid(bits)))
    # 입력 순서의 판정 목록 반환.
    return answer
