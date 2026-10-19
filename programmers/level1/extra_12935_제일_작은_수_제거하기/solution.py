def solution(arr):
    arr.remove(min(arr))
    if len(arr) == 0:
        return [-1]
    return arr

# 전체 코드 줄별 설명
# def solution(arr):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. arr: 정수들이 저장된 리스트를 입력받는 함수
#     arr.remove(min(arr))  # min은 최솟값. remove는 지정한 값의 첫 항목 삭제. min()으로 가장 작은 값을 찾고 remove()로 제거
#     if len(arr) == 0:  # if는 조건이 참일 때 실행. len은 길이. ==는 같음 비교. 숫자를 제거한 후 리스트의 원소가 0개인지 확인
#         return [-1]  # return은 결과를 돌려주고 함수 종료. []는 리스트. 리스트가 비었으면 [-1]을 반환하고 함수 종료
#     return arr  # return은 결과를 돌려주고 함수 종료. 남은 숫자들이 들어 있는 리스트를 반환

# 풀이 요약
# min으로 가장 작은 값을 구하고 remove로 그 값을 배열에서 지운다. 원소가 하나뿐이었다면 빈 배열이 되므로 [-1]을 반환한다. remove는 위치가 아니라 값을 받으며 입력 리스트를 직접 바꾼다.
# 원소 N개: 시간 O(N), 보조 공간 O(1).
