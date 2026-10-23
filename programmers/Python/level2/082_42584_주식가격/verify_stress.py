from solution import solution

def main():
    prices = [10000 - i // 10 for i in range(100000)]
    expected = [min(10 - i % 10, 99999 - i) for i in range(100000)]
    assert solution(prices) == expected
    print('대형 입력 검사 통과')

if __name__ == '__main__':
    main()
