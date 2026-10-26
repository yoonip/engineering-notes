import sys # 한 줄 문자열 입력
text = sys.stdin.readline().rstrip('\n') + '\0' # 줄바꿈을 제거하고 검사할 끝 표시 추가
position = count = total = 0 # 스캔 위치·정수 개수·합 초기화
while True: # 토큰이 끝날 때까지 정수 하나씩 해석
    while text[position] == ' ': # 토큰 앞 공백 검사
        position += 1 # 공백 다음 위치로 이동
    sign, number = 1, 0 # 기본 양수 부호와 현재 정수 초기화
    if text[position] in '+-': # 선택적 부호 검사
        sign = -1 if text[position] == '-' else 1 # 문자에 맞는 부호 저장
        position += 1 # 부호 뒤 숫자로 이동
    while '0' <= text[position] <= '9': # 연속된 십진수 숫자 읽기
        number = number * 10 + ord(text[position]) - ord('0') # 기존 자리값에 새 숫자 추가
        position += 1 # 다음 문자로 이동
    total += sign * number # 해석한 정수를 전체 합에 반영
    count += 1 # 읽은 정수 개수 증가
    while text[position] == ' ': # 토큰 뒤 공백 검사
        position += 1 # 다음 구분자 위치로 이동
    if text[position] != ',': # 구분자가 없으면 마지막 정수인지 확인
        break # 전체 줄 해석 종료
    position += 1 # 콤마 뒤 다음 정수로 이동
print(count, total) # 정수 개수와 합 출력
