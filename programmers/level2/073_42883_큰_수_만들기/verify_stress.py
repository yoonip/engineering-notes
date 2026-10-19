from solution import solution

def main():
    actual = solution("1" * 500000 + "9" * 500000, 500000)
    assert actual == "9" * 500000
    print('대형 입력 검사 통과')

if __name__ == '__main__':
    main()
