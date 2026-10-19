n, m = map(int, input().split())
for i in range(m):
    print("*" * n)

# 전체 코드 줄별 설명
# n, m = map(int, input().split())  # map은 각 원소에 함수 적용. input은 한 줄의 문자열 입력. split은 구분자로 문자열 분리. ()로 묶은 여러 값은 변경 불가 튜플. =는 값 저장. 두 숫자를 공백으로 구분해 입력받고, 정수 n과 m에 저장
# for i in range(m):  # for·in은 원소를 차례로 꺼내는 반복문. range는 끝값 직전까지 정수 순서 생성. 세로 길이 m만큼 반복
#     print("*" * n)  # print는 값을 표준 출력에 표시. "*"을 가로 길이 n만큼 반복하여 한 줄 출력

# 풀이 요약
# 가로 길이 n만큼 별을 반복한 문자열이 한 행이다. 이 행을 세로 길이 m번 출력하면 직사각형이 된다. print가 행 끝에 줄바꿈을 붙인다.
# 출력 크기 n×m: 시간 O(nm), 한 행 생성 공간 O(n).
