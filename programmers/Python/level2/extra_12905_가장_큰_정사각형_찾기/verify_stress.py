from solution import solution

def main():
    assert solution([[1] * 1000 for _ in range(1000)]) == 1000000
    print('대형 입력 검사 통과')

if __name__ == '__main__':
    main()
