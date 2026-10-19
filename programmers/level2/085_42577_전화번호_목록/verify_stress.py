from solution import solution

def main():
    actual = solution([f"{i:06d}" for i in range(1000000)])
    assert actual is True
    print('대형 입력 검사 통과')

if __name__ == '__main__':
    main()
