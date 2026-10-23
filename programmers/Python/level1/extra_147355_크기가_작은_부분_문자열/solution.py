def solution(t, p):
    answer = 0
    n = len(p)
    for i in range(len(t) - n + 1):
        num = int(t[i:i+n])
        if num <= int(p):
            answer += 1
    return answer

# 전체 코드 줄별 설명
# def solution(t, p):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. 문자열 t와 비교할 숫자 문자열 p를 입력받음
#     answer = 0  # =는 값 저장. 조건을 만족하는 부분 문자열의 개수를 저장
#     n = len(p)  # len은 길이. =는 값 저장. p의 문자열 길이를 구함
#     for i in range(len(t) - n + 1):  # for·in은 원소를 차례로 꺼내는 반복문. len은 길이. range는 끝값 직전까지 정수 순서 생성. t에서 길이가 n인 부분 문자열을 추출할 시작 위치 반복
#         num = int(t[i:i+n])  # int는 정수 변환. [시작:끝]은 끝을 제외하는 슬라이스. =는 값 저장. t[i:i+n]으로 n글자를 추출하고 int()로 정수 변환
#         if num <= int(p):  # if는 조건이 참일 때 실행. int는 정수 변환. <=는 이하 비교. 추출한 숫자가 p보다 작거나 같으면
#             answer += 1  # +=는 더하거나 연결한 값을 저장. 조건을 만족하므로 개수를 1 증가
#     return answer  # return은 결과를 돌려주고 함수 종료. 조건을 만족한 부분 문자열의 총개수 반환

# 풀이 요약
# p의 길이와 같은 부분 문자열을 t의 모든 시작 위치에서 자른다. 각 조각을 숫자로 바꿔 p 이하인지 센다. 시작 위치의 마지막 값은 len(t)-len(p)이므로 range의 끝에 1을 더한다.
# t 길이 T, p 길이 P: 시간 O(TP), 보조 공간 O(P).
