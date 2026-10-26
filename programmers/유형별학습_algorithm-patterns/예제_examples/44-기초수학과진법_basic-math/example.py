import sys  # 표준 입력 전체를 토큰으로 읽기

def main():  # 입력 한 건을 계산하고 결과 출력
    tokens = iter(sys.stdin.read().split())  # 공백과 줄바꿈을 같은 구분자로 처리
    base, modulus = int(next(tokens)), int(next(tokens))  # 진법과 양의 나누는 수
    text = next(tokens)  # 전체 정수로 바꾸지 않을 숫자 문자열
    remainder = 0  # 빈 접두사의 나머지
    for ch in text:  # 높은 자리부터 순서대로 읽기
        digit = ord(ch) - ord("0") if "0" <= ch <= "9" else ord(ch) - ord("A") + 10  # 숫자·대문자를 자릿값으로 변환
        remainder = (remainder * base + digit) % modulus  # 이전 접두사에 한 자리 붙인 나머지
    print(remainder)  # 전체 진법 숫자의 나머지

if __name__ == "__main__":  # 직접 실행할 때만 예제 시작
    main()  # 표준 입력 한 건 처리
