from solution import solution

def main():
    name = "A" * 20
    actual = solution(name)
    assert actual == 0
    print('대형 입력 검사 통과')

if __name__ == '__main__':
    main()
