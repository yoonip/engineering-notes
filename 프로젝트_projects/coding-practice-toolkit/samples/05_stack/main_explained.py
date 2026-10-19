# 자체 창작 연습 05 · 괄호 짝 검사 
# 핵심 상태: stack/st에는 아직 닫히지 않은 여는 괄호를 저장한다. top 또는 길이가 스택 크기다.
# Python 3: 파일의 위에서 아래로 실행한다. 들여쓰기가 반복문·조건문·함수의 범위다.
# sys.stdin은 표준입력이다. read()는 EOF까지 읽으므로 파일 입력과 온라인 채점에 편하다.
# 터미널에 직접 붙여 넣을 때 read()가 대기하면 Windows에서 Ctrl+Z 후 Enter로 EOF를 보낸다.

import sys
# read로 EOF까지 바이트 입력을 읽고 strip으로 끝의 줄바꿈을 제거한다.
# decode는 바이트를 Python 문자열로 바꾼다. 입력 문자 자체의 순서는 유지된다.
# 빈 문자열은 허용되지 않고 괄호 문자열 하나만 입력된다는 문제 조건을 따른다.
s = sys.stdin.buffer.read().strip().decode()
stack = []
ok = True
# list.append와 list.pop을 스택의 넣기/꺼내기로 쓴다.
# 빈 list는 조건식에서 False이므로 not stack은 스택이 비었다는 검사다.
# 빈 리스트에서 pop하면 예외가 나므로 먼저 비었는지 확인한다.
for ch in s:
    if ch == '(':
        stack.append(ch)
    elif not stack:
        ok = False
        break
    else:
        stack.pop()  # 가장 최근 여는 괄호 하나를 제거한다.
# 리스트가 비어 있지 않으면 True이므로 남은 여는 괄호를 검사한다.
# ok가 True인 채로 스택도 비어 있어야 YES다.
# 이 문제는 괄호 한 종류만 사용한다. 여러 종류라면 가장 위의 종류도 확인해야 한다.
if stack:
    ok = False
print('YES' if ok else 'NO')

# 복잡도: 시간 O(S), 공간 O(S). S는 문자열 길이.
# 마지막 경계 확인:
# - 끝에 남은 여는 괄호도 검사한다.
# - 스택이 빈 상태에서 pop하지 않는다.
# - 여는 괄호 수와 닫는 괄호 수만 같다고 올바른 것은 아니다: )(는 NO.
