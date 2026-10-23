from solution import solution

def main():
    nodes = list(range(1, 400001))
    edges = [[i, i + 1] for i in range(1, 400000)]
    assert solution(nodes, edges) == [0, 0]
    print('대형 입력 검사 통과')

if __name__ == '__main__':
    main()
