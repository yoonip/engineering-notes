from fractions import Fraction

def solution(h1,m1,s1,h2,m2,s2):
    start, end = h1*3600+m1*60+s1, h2*3600+m2*60+s2
    events = set()
    for period, speed in ((43200,719),(3600,59)):
        for turn in range(end*speed//period+1):
            instant = Fraction(turn*period,speed)
            if start <= instant <= end:
                events.add(instant)
    return len(events)
