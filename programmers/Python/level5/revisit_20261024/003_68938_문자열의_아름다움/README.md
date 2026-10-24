# 문자열의 아름다움 — Python 재풀이

[문제 원문](<https://school.programmers.co.kr/learn/courses/30/lessons/68938>) · [재풀이 목록](<../README.md>)

정답률 3%와 풀이 인원 275명은 이번 목록 확인 시점의 값입니다. 전체 3순위로 진행했습니다.

## 사이트 채점

사이트 채점 합계 100점과 이번 재풀이 이후의 Python3 정답 100점 제출 내역을 확인했습니다. 정답은 실제 1번째 제출이며, 총 1회 제출했습니다.

| 제출 | 결과 | 합계 점수 | 입력 코드 | 채점 기록 |
| --- | --- | ---: | --- | --- |
| 1 | 정답 | 100 | [코드](<solution.py>) | [채점 결과 발췌](<attempts/attempt1_grading.txt>) |

[채점·제출 내역 JSON](<grading.json>)에는 실제 제출 시각, 합계, 테스트별 결과와 시간, 메모리, 입력 SHA256 및 새 제출 내역을 기록합니다. 제출한 입력 파일은 원본 바이트를 보관하며, 화면에 넣을 때의 LF 정규화 해시를 별도 기록합니다.

## 로컬 검증

[제출 전 후보 검증 원본](<local_checks.json>)은 사이트 채점과 별도인 로컬 비교·성능 기록입니다. 로컬 검증에 기록한 코드 해시는 정답 제출 입력과 같습니다.

## 풀이 요약

부분문자열 길이가 m이면 아름다움의 상한은 m−1. 전체 상한 N(N−1)(N+1)/6에서 실제로 부족한 거리만 차감.
양끝 문자가 다르면 상한 그대로. 양끝이 같고 중간에 다른 문자가 있으면 양끝 같은 문자 연속길이의 최솟값만큼 감소.
한 연속구간 안은 모두 같은 문자라 아름다움0. 구간 길이 L마다 L(L−1)(L+1)/6을 따로 차감.
떨어진 같은 문자 구간 A·B 사이의 감점은 sum((A−k+1)(B−k+1)). 감점이 k 이상인 시작점·끝점 조합을 세는 방식.
previous[문자][k]에 이전 시작점 수를 누적해 두고, 현재 구간의 끝점 수를 곱한 뒤 현재 시작점도 추가.
전체 need 반복 횟수는 모든 구간 길이의 합 N. 시간 O(N), 공간 O(N). baby9, oo0.

## 정답 제출 코드

실제 1번째 정답 제출 입력의 전체 내용입니다. 원본 파일의 줄바꿈 바이트는 그대로 두며, 아래 표시는 LF로 정규화합니다.

```python
def solution(s):
    n = len(s)
    longest = [0] * 26
    start = 0
    while start < n:
        char = s[start]
        end = start + 1
        while end < n and s[end] == char:
            end += 1
        letter = ord(char) - 97
        length = end - start
        if length > longest[letter]:
            longest[letter] = length
        start = end
    previous = [[0] * (length + 1) for length in longest]
    answer = n * (n - 1) * (n + 1) // 6
    start = 0
    while start < n:
        char = s[start]
        end = start + 1
        while end < n and s[end] == char:
            end += 1
        length = end - start
        answer -= length * (length - 1) * (length + 1) // 6
        counts = previous[ord(char) - 97]
        for need in range(1, length + 1):
            choices = length - need + 1
            answer -= choices * counts[need]
            counts[need] += choices
        start = end
    return answer

# 전체 코드 줄별 설명
# def solution(s):  # 문자열 s의 모든 부분문자열 아름다움 합을 구하는 함수
#     n = len(s)  # len으로 전체 길이를 읽어 기본 합 계산에 사용
#     longest = [0] * 26  # 알파벳별 최대 연속길이; 필요한 누적 칸만 확보
#     start = 0  # 첫 연속구간의 시작 인덱스
#     while start < n:  # 같은 문자가 이어지는 최대 구간을 차례로 탐색
#         char = s[start]  # 이번 연속구간의 알파벳
#         end = start + 1  # 구간 끝 다음 위치를 한 칸부터 확인
#         while end < n and s[end] == char:  # 문자열 안이고 같은 문자일 때만 구간 확장
#             end += 1  # 오른쪽 경계를 다음 칸으로 이동
#         letter = ord(char) - 97  # ord로 a~z를 0~25의 배열 번호로 변환
#         length = end - start  # 이번 최대 연속구간의 길이
#         if length > longest[letter]:  # 이 알파벳에서 더 긴 구간을 찾은 경우
#             longest[letter] = length  # 필요한 누적 배열의 최대 깊이 갱신
#         start = end  # 방금 센 구간 다음 문자부터 다시 탐색
#     previous = [[0] * (length + 1) for length in longest]  # 리스트 내포로 알파벳마다 독립적인 길이별 누적 배열 생성
#     answer = n * (n - 1) * (n + 1) // 6  # 모든 부분문자열의 길이−1 합; //로 정수 계산
#     start = 0  # 실제 감점을 계산할 두 번째 구간 순회 시작
#     while start < n:  # 각 구간의 같은 문자 양끝 조합을 차감
#         char = s[start]  # 현재 구간이 담은 알파벳
#         end = start + 1  # 현재 구간 끝 탐색 시작
#         while end < n and s[end] == char:  # 같은 알파벳이 이어지는 동안만 전진
#             end += 1  # 현재 연속구간의 오른쪽 경계 증가
#         length = end - start  # 이번 구간의 문자 수
#         answer -= length * (length - 1) * (length + 1) // 6  # 한 구간 안의 부분문자열은 전부0이므로 그 기본 합 제외
#         counts = previous[ord(char) - 97]  # 같은 알파벳의 이전 구간들이 만든 시작점 누적 배열
#         for need in range(1, length + 1):  # 양끝 같은 문자 길이가 need 이상일 때의 감점1씩 합산
#             choices = length - need + 1  # 현재 구간에서 need개 이상을 포함하는 끝점 수
#             answer -= choices * counts[need]  # 이전 시작점과 현재 끝점의 모든 조합에서 감점 차감
#             counts[need] += choices  # 현재 구간의 시작점도 다음 같은 알파벳 구간을 위해 누적
#         start = end  # 다음 연속구간으로 이동
#     return answer  # 길이 상한에서 모든 같은 문자 감점을 뺀 합 반환

# 풀이 요약
# 부분문자열 길이가 m이면 아름다움의 상한은 m−1. 전체 상한 N(N−1)(N+1)/6에서 실제로 부족한 거리만 차감.
# 양끝 문자가 다르면 상한 그대로. 양끝이 같고 중간에 다른 문자가 있으면 양끝 같은 문자 연속길이의 최솟값만큼 감소.
# 한 연속구간 안은 모두 같은 문자라 아름다움0. 구간 길이 L마다 L(L−1)(L+1)/6을 따로 차감.
# 떨어진 같은 문자 구간 A·B 사이의 감점은 sum((A−k+1)(B−k+1)). 감점이 k 이상인 시작점·끝점 조합을 세는 방식.
# previous[문자][k]에 이전 시작점 수를 누적해 두고, 현재 구간의 끝점 수를 곱한 뒤 현재 시작점도 추가.
# 전체 need 반복 횟수는 모든 구간 길이의 합 N. 시간 O(N), 공간 O(N). baby9, oo0.
```
