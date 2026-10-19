def solution(n, arr1, arr2):
    answer = []
    for a, b in zip(arr1, arr2):
        combined = a | b
        binary = bin(combined)[2:].zfill(n)
        row = binary.replace("1", "#").replace("0", " ")
        answer.append(row)
    return answer

# 전체 코드 줄별 설명
# def solution(n, arr1, arr2):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. 지도 크기 n과 두 개의 지도 배열을 입력받음
#     answer = []  # []는 리스트. =는 값 저장. 완성된 지도의 각 행을 저장할 빈 리스트
#     for a, b in zip(arr1, arr2):  # for·in은 원소를 차례로 꺼내는 반복문. zip은 같은 위치의 값들을 짝지음. ()로 묶은 여러 값은 변경 불가 튜플. 두 지도에서 같은 위치의 숫자 a, b를 하나씩 가져옴
#         combined = a | b  # |는 비트 OR. =는 값 저장. 비트 OR 연산으로 두 지도를 합침 (하나라도 1이면 1)
#         binary = bin(combined)[2:].zfill(n)  # bin은 0b 접두사가 있는 이진수 문자열. zfill은 지정한 자릿수까지 앞을 0으로 채움. [시작:끝]은 끝을 제외하는 슬라이스. =는 값 저장. 2진수로 변환하고 0b 제거 후 앞에 0을 채워 길이를 n으로 맞춤
#         row = binary.replace("1", "#").replace("0", " ")  # replace는 문자열 치환. =는 값 저장. 숫자 1은 벽(#), 0은 공백으로 변환
#         answer.append(row)  # append는 리스트 끝에 추가. 변환한 한 행을 정답 리스트에 추가
#     return answer  # return은 결과를 돌려주고 함수 종료. 완성된 지도를 문자열 리스트로 반환

# 풀이 요약
# 두 지도의 각 행은 비트로 벽 위치를 나타낸다. OR 연산은 어느 지도에든 벽이 있으면 1을 남긴다. 이진수의 0b 접두사를 제거하고 n자리로 채운 뒤 1은 벽, 0은 공백으로 바꾼다.
# 한 변 N: 출력 문자 수 기준 시간·공간 O(N²).
