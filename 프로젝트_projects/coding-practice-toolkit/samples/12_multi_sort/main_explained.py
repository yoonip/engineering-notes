# 점수 내림차순, 점수 동점일 때 이름 오름차순으로 기록을 정렬한다.
# 중복 기록도 입력된 개수만큼 남겨야 하므로 집합으로 중복을 지우지 않는다.
# 이름은 영문 소문자만 허용하여 세 언어에서 같은 사전순으로 비교된다.
# 입력 제한과 실행 비용: 이름 최대 길이 L≤20. C++/Python O(N log N·L), 공간 O(NL). C qsort는 C 표준에 시간복잡도 보장이 없고 일반 구현은 O(N log N) 정렬이 흔하다. 이름 비교 자체는 O(L)이다.

# Record 또는 튜플 한 개가 점수와 이름을 함께 보관한다.
# C의 name[21]은 최대 20글자와 끝의 널 문자를 위한 공간이다.
# 점수는 음수도 가능하다. Python의 -score는 높은 점수가 작은 키로 먼저 오게 만든다.

# sys.stdin.buffer는 입력을 바이트로 읽는다. read는 전체 입력을 메모리에 올린다는 점을 고려한다.
# 문자열이 필요하면 decode하고 숫자가 필요하면 int로 바꾼다. 정수는 큰 값도 자동 확장된다.

import sys
read=sys.stdin.buffer.readline
n=int(read())
records=[]
for _ in range(n):
    score,name=read().split()
    # 점수와 이름을 같은 기록에 묶어 저장한다.
    # C %20s는 이름 버퍼 크기를 지키고, Python은 읽은 바이트를 문자열로 바꿔 저장한다.
    records.append((int(score),name.decode()))
# 첫 기준 점수를 먼저 비교하고 동점에서만 이름을 비교한다.
# C qsort의 비교함수는 음수/0/양수, C++ sort 비교함수는 앞에 와야 하는지의 참/거짓을 반환한다.
# C++은 완전히 같은 기록끼리 false여야 하고 Python은 (-점수,이름)을 오름차순 정렬한다.
records.sort(key=lambda x:(-x[0],x[1])) # 점수는 내림차순, 이름은 오름차순이다.
# 정렬 결과를 기록 단위로 출력한다.
# 전체 키에 reverse를 적용하면 이름까지 뒤집히므로 Python은 점수 부호만 바꾼다.
print('\n'.join(f'{score} {name}' for score,name in records))

# 손으로 확인: 95점 기록: bob,amy,amy → amy,amy,bob
# 손으로 확인: 80점 기록: zoe,ann → ann,zoe
# 손으로 확인: 95점 그룹이 80점 그룹보다 앞
# 완성 후 확인: C 비교함수는 점수의 단순 뺄셈보다 대소 비교로 부호를 반환한다.
# 완성 후 확인: C++ 비교함수에서 같은 기록끼리는 false를 반환해야 한다.
# 완성 후 확인: 이름 오름차순 조건을 빠뜨리지 않는다.
# 완성 후 확인: 이 문제의 이름은 영문 소문자로 제한해 세 언어의 비교 규칙을 일치시켰다.
