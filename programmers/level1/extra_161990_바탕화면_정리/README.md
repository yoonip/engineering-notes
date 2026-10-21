# 바탕화면 정리

[Level 1 목록 / Level 1 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/161990) · Level 1 · Python3

유형: 구현 · 최솟값·최댓값

## 풀이 원리

파일이 있는 모든 칸의 최소 행·열과 최대 행·열을 구합니다. 드래그 사각형의 오른쪽·아래 끝은 칸 경계이므로 최대 좌표에 1을 더합니다. 각 방향의 극단을 포함해야 모든 파일을 덮으며, 그보다 줄이면 적어도 한 파일을 놓칩니다.

지도 H×W: 시간 O(HW), 보조 공간 O(1).

## 공식 예제

입력 인수: `[[".#...", "..#..", "...#."]]`

반환값: `[0, 1, 3, 4]`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있습니다.

## 코드와 줄별 설명

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
def solution(wallpaper):
    lux = len(wallpaper)
    luy = len(wallpaper[0])
    rdx = 0
    rdy = 0
    for r, row in enumerate(wallpaper):
        for c, cell in enumerate(row):
            if cell == "#":
                lux = min(lux, r)
                luy = min(luy, c)
                rdx = max(rdx, r + 1)
                rdy = max(rdy, c + 1)
    return [lux, luy, rdx, rdy]

# 전체 코드 줄별 설명
# def solution(wallpaper):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. wallpaper: 각 행을 문자열로 저장한 리스트
#     lux = len(wallpaper)  # len은 길이. =는 값 저장. 시작 행: 전체 행 수로 초기화한 뒤 더 작은 파일 행을 찾음
#     luy = len(wallpaper[0])  # len은 길이. []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. =는 값 저장. 시작 열: 첫 행의 길이, 즉 전체 열 수로 초기화
#     rdx = 0  # =는 값 저장. 끝 행: 파일을 찾을 때마다 필요한 아래쪽 경계로 갱신
#     rdy = 0  # =는 값 저장. 끝 열: 파일을 찾을 때마다 필요한 오른쪽 경계로 갱신
#     for r, row in enumerate(wallpaper):  # for·in은 원소를 차례로 꺼내는 반복문. enumerate는 인덱스·값을 함께 제공. ()로 묶은 여러 값은 변경 불가 튜플. 행 번호 r과 해당 행의 문자열을 함께 꺼냄
#         for c, cell in enumerate(row):  # for·in은 원소를 차례로 꺼내는 반복문. enumerate는 인덱스·값을 함께 제공. ()로 묶은 여러 값은 변경 불가 튜플. 그 행에서 열 번호 c와 문자 하나를 함께 꺼냄
#             if cell == "#":  # if는 조건이 참일 때 실행. ==는 같음 비교. 파일이 있는 칸만 처리. 빈칸 "."은 건너뜀
#                 lux = min(lux, r)  # min은 최솟값. =는 값 저장. 기존 시작 행과 현재 행 중 작은 값 → 가장 위쪽
#                 luy = min(luy, c)  # min은 최솟값. =는 값 저장. 기존 시작 열과 현재 열 중 작은 값 → 가장 왼쪽
#                 rdx = max(rdx, r + 1)  # max는 최댓값. =는 값 저장. 현재 파일 칸의 아래쪽 경계까지 포함
#                 rdy = max(rdy, c + 1)  # max는 최댓값. =는 값 저장. 현재 파일 칸의 오른쪽 경계까지 포함
#     return [lux, luy, rdx, rdy]  # return은 결과를 돌려주고 함수 종료. []는 리스트. [시작 행, 시작 열, 끝 행, 끝 열]을 반환

# 풀이 요약
# 파일이 있는 모든 칸의 최소 행·열과 최대 행·열을 구한다. 드래그 사각형의 오른쪽·아래 끝은 칸 경계이므로 최대 좌표에 1을 더한다. 각 방향의 극단을 포함해야 모든 파일을 덮으며, 그보다 줄이면 적어도 한 파일을 놓친다.
# 지도 H×W: 시간 O(HW), 보조 공간 O(1).
```

## 확인한 범위

2026-10-16 00:17:09의 Python3 제출 내역에서 정답 100/100을 확인했습니다. 원본은 그대로 보관했습니다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같습니다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았습니다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있습니다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
