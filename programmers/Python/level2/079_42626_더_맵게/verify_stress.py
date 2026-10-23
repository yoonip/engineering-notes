from solution import solution

def main():
    actual = solution([0] * 1000000, 1)
    assert actual == -1
    print('대형 입력 검사 통과')

if __name__ == '__main__':
    main()
