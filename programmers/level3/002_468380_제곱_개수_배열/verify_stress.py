from solution import solution

def main():
    assert solution([100000] * 100000, 1, 5000000000) == [500000000000000, 5000000001]
    print('대형 입력 검사 통과')

if __name__ == '__main__':
    main()
