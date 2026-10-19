def solution(genres, plays):
    totals, songs = {}, {}
    for i, (genre, play) in enumerate(zip(genres, plays)):
        totals[genre] = totals.get(genre, 0) + play
        songs.setdefault(genre, []).append((-play, i))
    answer = []
    for genre in sorted(totals, key=lambda name: -totals[name]):
        for negative_play, number in sorted(songs[genre])[:2]:
            answer.append(number)
    return answer

# 전체 코드 줄별 설명
# def solution(genres, plays):  # def는 함수 정의. 노래별 장르와 재생 수 목록을 받음.
#     totals, songs = {}, {}  # {}는 딕셔너리. 장르별 총 재생 수와 장르별 노래 목록을 각각 저장.
#     for i, (genre, play) in enumerate(zip(genres, plays)):  # zip은 같은 위치끼리 묶음, enumerate는 번호 추가. 고유 번호·장르·재생 수를 언패킹.
#         totals[genre] = totals.get(genre, 0) + play  # get은 키 조회, 없으면 0. 장르 전체 재생 수 누적.
#         songs.setdefault(genre, []).append((-play, i))  # setdefault는 키가 없으면 빈 리스트 생성, append는 추가. 음수 재생 수와 번호를 튜플로 저장.
#     answer = []  # []는 결과 고유 번호 목록.
#     for genre in sorted(totals, key=lambda name: -totals[name]):  # sorted는 정렬, key는 기준, lambda는 짧은 익명 함수. 음수 합계로 정렬해 많이 재생된 장르 먼저 처리.
#         for negative_play, number in sorted(songs[genre])[:2]:  # 튜플은 앞부터 비교해 재생 수 내림차순·번호 오름차순. [:2]는 처음 최대 두 곡 선택.
#             answer.append(number)  # 선택한 곡의 고유 번호만 결과에 추가.
#     return answer  # 베스트앨범에 수록할 순서대로 반환.

# 풀이 요약
# 장르의 우선순위와 장르 안 노래의 우선순위를 따로 계산한다. (-재생 수,고유 번호)로 정렬하면 두 노래 조건이 한 번에 적용된다.
# 예: pop 총 3100회가 classic 1450회보다 앞서므로 pop의 4·1번, classic의 3·0번 순서가 된다.
# 노래 N개일 때 시간 O(N log N), 공간 O(N). 장르에 한 곡만 있으면 슬라이스 결과도 한 곡이다.
# 