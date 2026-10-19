from collections import Counter  # 값별 개수를 세는 Counter만 import 필요


def solution(arr):  # 연습 입력 예시: [3, 1, 2, 1]
    # 1. append / pop / len: 추가, 꺼내기, 길이
    arr.append(5)  # 리스트 맨 뒤에 5 추가
    print("append:", arr)  # 예시: [3, 1, 2, 1, 5]
    last = arr.pop()  # 마지막 값 5를 꺼내고 리스트에서 제거
    print("pop:", last, arr)  # 예시: 5 [3, 1, 2, 1]
    print("len:", len(arr))  # 예시: 숫자 4개이므로 4

    # 2. sort / min / max: 정렬, 최솟값, 최댓값
    arr.sort()  # 기존 리스트를 오름차순으로 정렬
    print("sort:", arr)  # 예시: [1, 1, 2, 3]
    arr.sort(reverse=True)  # 기존 리스트를 내림차순으로 정렬
    print("descending:", arr)  # 예시: [3, 2, 1, 1]
    smallest = min(arr)  # 가장 작은 숫자를 저장
    largest = max(arr)  # 가장 큰 숫자를 저장
    print("min/max:", smallest, largest)  # 예시: 1 3

    # 3. lower / count: 소문자로 바꾸기, 특정 값의 개수
    text = "pPoooyY"  # 대문자와 소문자가 섞인 문자열
    text = text.lower()  # 소문자로 바꾼 결과를 다시 저장
    print("lower:", text)  # 결과: ppoooyy
    p_count = text.count("p")  # p 개수 2를 저장; import 불필요
    y_count = text.count("y")  # y 개수 2를 저장; import 불필요
    print("count:", p_count, y_count)  # 결과: 2 2
    print("same count:", p_count == y_count)  # 결과: True
    print("list count:", arr.count(1))  # 예시: 숫자 1이 2개이므로 2

    # 4. split / int / str: 나누고, 정수로 바꾸고, 문자열로 만들기
    s = "3 -1 2"  # 공백으로 구분된 숫자 문자열
    words = s.split()  # 문자열 리스트 ["3", "-1", "2"] 생성
    print("split:", words)  # 결과: ['3', '-1', '2']
    numbers = []  # 정수들을 담을 빈 리스트
    for word in words:  # 나눠진 문자열을 하나씩 꺼냄
        number = int(word)  # 현재 문자열을 정수로 변환
        numbers.append(number)  # 정수를 리스트에 추가
    print("int:", numbers)  # 결과: [3, -1, 2]
    answer = str(min(numbers)) + " " + str(max(numbers))  # 두 값을 문자열로 연결
    print("str:", answer)  # 결과: -1 3

    # 5. for / range: 값으로 반복하기, 인덱스로 반복하기
    for number in numbers:  # 값 3, -1, 2를 하나씩 꺼냄
        print("value:", number)  # 현재 숫자를 출력
    for i in range(len(numbers)):  # 인덱스 0, 1, 2를 하나씩 꺼냄
        print("index/value:", i, numbers[i])  # 위치와 해당 값을 출력

    # 6. Counter: 모든 값의 등장 횟수를 한꺼번에 기록
    size_counts = Counter(arr)  # 예시: 숫자 1은 2개, 2와 3은 각 1개
    print("Counter[1]:", size_counts[1])  # 예시: 숫자 1의 개수 2
    counts = list(size_counts.values())  # 개수들만 꺼내 리스트로 저장
    counts.sort(reverse=True)  # 개수가 많은 순서로 정렬
    print("Counter values:", counts)  # 예시: [2, 1, 1]

    return 0  # 연습용 종료 값; 특정 문제의 정답은 아님
