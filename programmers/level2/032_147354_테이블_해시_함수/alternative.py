def solution(data,col,row_begin,row_end):
    rows=sorted(data,key=lambda row:row[0],reverse=True)
    rows.sort(key=lambda row:row[col-1])
    prefix=[0]
    for index,row in enumerate(rows,1):
        prefix.append(prefix[-1]^sum(value%index for value in row))
    return prefix[row_end]^prefix[row_begin-1]
