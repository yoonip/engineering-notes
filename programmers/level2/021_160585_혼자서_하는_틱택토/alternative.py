def solution(board):
    target=''.join(board)
    lines=((0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6))
    seen=set()
    def visit(state,turn):
        if state in seen: return
        seen.add(state)
        if any(state[a]!='.' and state[a]==state[b]==state[c] for a,b,c in lines): return
        for i,char in enumerate(state):
            if char=='.':
                visit(state[:i]+turn+state[i+1:],'X' if turn=='O' else 'O')
    visit('.'*9,'O')
    return int(target in seen)
