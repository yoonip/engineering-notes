import sys  # 표준 입력 전체를 토큰으로 읽기

def main():  # 입력 한 건을 계산하고 결과 출력
    tokens = iter(sys.stdin.read().split())  # 공백과 줄바꿈을 같은 구분자로 처리
    a, b = int(next(tokens)), int(next(tokens))  # 정수와 양의 분모
    quotient, remainder = divmod(a, b)  # Python의 내림 몫과 비음수 나머지
    print(quotient, remainder)  # 세 언어가 같은 q와 r을 출력

if __name__ == "__main__":  # 직접 실행할 때만 예제 시작
    main()  # 표준 입력 한 건 처리
