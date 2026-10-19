def solution(numbers):
    def valid(bits):
        if len(bits) == 1:
            return True
        middle = len(bits) // 2
        if bits[middle] == '0':
            return '1' not in bits
        return valid(bits[:middle]) and valid(bits[middle + 1:])

    answer = []
    for number in numbers:
        bits = bin(number)[2:]
        size = 1
        while size < len(bits):
            size = size * 2 + 1
        bits = bits.zfill(size)
        answer.append(int(valid(bits)))
    return answer

# 전체 코드 줄별 설명
# def solution(numbers):  # def는 함수 정의. numbers는 표현 가능 여부를 판단할 십진 정수 목록.
#     def valid(bits):  # 포화 이진트리의 중위 순회 문자열을 검사하는 중첩 재귀 함수.
#         if len(bits) == 1:  # len은 길이, ==는 같음. 한 노드는 실제·더미 모두 가능한 리프.
#             return True  # True는 참. return으로 이 부분 트리가 유효함을 반환.
#         middle = len(bits) // 2  # //는 정수 나눗셈. 중위 순회에서 가운데 문자가 현재 트리의 루트.
#         if bits[middle] == '0':  # if는 조건문. 루트가 더미 노드인 경우.
#             return '1' not in bits  # not in은 미포함 검사. 더미 아래에는 실제 노드가 하나도 없어야 함.
#         return valid(bits[:middle]) and valid(bits[middle + 1:])  # [:끝]과 [시작:] 슬라이스로 좌·우 부분 트리를 분리. and는 두 검사 모두 참이어야 참.
# 
#     answer = []  # []는 결과를 순서대로 담을 빈 리스트.
#     for number in numbers:  # for~in으로 입력 정수 순회.
#         bits = bin(number)[2:]  # bin은 0b 접두사가 붙은 이진 문자열 생성. [2:]로 접두사를 제거.
#         size = 1  # 포화 이진트리의 가능한 노드 수 1·3·7·15... 중 시작값.
#         while size < len(bits):  # while은 조건이 참인 동안 반복. 이진 문자열 전체를 담을 크기까지 늘림.
#             size = size * 2 + 1  # 한 층을 늘리면 이전 크기의 두 배+루트 한 개.
#         bits = bits.zfill(size)  # zfill(길이)은 왼쪽에 0을 채움. 십진 값은 유지하면서 포화 트리 모양으로 맞춤.
#         answer.append(int(valid(bits)))  # int는 참·거짓을 1·0으로 변환. append는 결과 하나 추가.
#     return answer  # 입력 순서의 판정 목록 반환.

# 풀이 요약
# 이진 문자열을 노드 수 1·3·7·15...에 맞춰 왼쪽에 0을 채웁니다. 중위 순회이므로 각 부분 문자열의 가운데가 루트입니다.
# 루트가 0이면 그 부분 트리 전체에 1이 없어야 합니다. 루트가 1이면 왼쪽·오른쪽을 같은 규칙으로 검사합니다. 문자열 길이 L에 대해 슬라이스를 포함한 시간 O(L log L), 추가 공간 O(L).
# 예: 5는 101이고 가운데 루트가 0인데 실제 자식 1이 있으므로 불가. 42는 0101010이고 루트 1 아래의 각 부분 트리도 유효하므로 가능합니다.
