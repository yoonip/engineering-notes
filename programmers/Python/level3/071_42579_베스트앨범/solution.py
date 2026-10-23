# 노래별 장르와 재생 수 목록을 받음.
def solution(genres, plays):
    # 장르별 총 재생 수와 장르별 노래 목록을 각각 저장.
    totals, songs = {}, {}
    # 고유 번호·장르·재생 수를 언패킹.
    for i, (genre, play) in enumerate(zip(genres, plays)):
        # 장르 전체 재생 수 누적.
        totals[genre] = totals.get(genre, 0) + play
        # 음수 재생 수와 번호를 튜플로 저장.
        songs.setdefault(genre, []).append((-play, i))
    # []는 결과 고유 번호 목록.
    answer = []
    # 음수 합계로 정렬해 많이 재생된 장르 먼저 처리.
    for genre in sorted(totals, key=lambda name: -totals[name]):
        # [:2]는 처음 최대 두 곡 선택.
        for negative_play, number in sorted(songs[genre])[:2]:
            # 선택한 곡의 고유 번호만 결과에 추가.
            answer.append(number)
    # 베스트앨범에 수록할 순서대로 반환.
    return answer
