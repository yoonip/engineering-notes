def solution(X, Y):
    parts = []
    for digit in "9876543210":
        count = min(X.count(digit), Y.count(digit))
        parts.append(digit * count)
    answer = "".join(parts)
    if answer == "":
        return "-1"
    if answer[0] == "0":
        return "0"
    return answer

# 전체 코드 줄별 설명
# def solution(X, Y):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. 숫자로 이루어진 문자열 X와 Y를 받는 함수
#     parts = []  # []는 리스트. =는 값 저장. 공통으로 사용할 숫자들을 문자열 조각으로 저장할 리스트
#     for digit in "9876543210":  # for·in은 원소를 차례로 꺼내는 반복문. 문자 "9"부터 "0"까지 큰 숫자 순서로 하나씩 확인
#         count = min(X.count(digit), Y.count(digit))  # min은 최솟값. count는 등장 횟수. =는 값 저장. 두 문자열에서 해당 숫자가 나온 횟수 중 작은 값
#         parts.append(digit * count)  # append는 리스트 끝에 추가. 해당 숫자를 count번 반복한 문자열을 리스트에 추가
#     answer = "".join(parts)  # join은 문자열들을 구분자로 연결. =는 값 저장. 저장한 문자열 조각들을 구분자 없이 하나로 이어 붙임
#     if answer == "":  # if는 조건이 참일 때 실행. ==는 같음 비교. 만들어진 문자열이 비어 있다면 공통 숫자가 하나도 없는 경우
#         return "-1"  # return은 결과를 돌려주고 함수 종료. 짝꿍이 없다는 뜻의 문자열 "-1"을 반환하고 함수 종료
#     if answer[0] == "0":  # if는 조건이 참일 때 실행. []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. ==는 같음 비교. 큰 순서로 붙였는데 첫 글자가 "0"이면 모든 글자가 "0"임
#         return "0"  # return은 결과를 돌려주고 함수 종료. "00", "000"처럼 여러 개여도 문자열 "0" 하나만 반환
#     return answer  # return은 결과를 돌려주고 함수 종료. 공통 숫자들로 만든 가장 큰 수를 문자열 그대로 반환

# 풀이 요약
# 각 숫자를 양쪽에서 쓸 수 있는 횟수는 두 문자열의 등장 횟수 중 작은 값이다. 9부터 0까지 그 개수만큼 이어 붙여 가장 큰 수를 만든다. 공통 숫자가 없으면 -1, 0만 있으면 0 하나를 반환한다.
# 입력 길이 X,Y와 결과 길이 L: 시간 O(X+Y+L), 공간 O(L). 숫자 종류는 10개다.
