def solution(n, data):
    positions = {}
    friends = 'ACFJMNRT'
    def valid():
        for rule in data:
            a, b, op, distance = rule[0], rule[2], rule[3], int(rule[4])
            if a not in positions or b not in positions:
                continue
            actual = abs(positions[a] - positions[b]) - 1
            if not {'=': actual == distance, '<': actual < distance, '>': actual > distance}[op]:
                return False
        return True
    def place():
        if len(positions) == 8:
            return 1
        count = 0
        for friend in friends:
            if friend not in positions:
                positions[friend] = len(positions)
                if valid():
                    count += place()
                del positions[friend]
        return count
    return place()
