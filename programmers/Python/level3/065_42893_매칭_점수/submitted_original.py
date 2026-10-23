import re
from fractions import Fraction

def solution(word, pages):
    word = word.lower()
    addresses, links, basic = [], [], []
    for page in pages:
        meta = re.search(r'<meta\b[^>]*\bproperty\s*=\s*"og:url"[^>]*>', page, re.I).group()
        url = re.search(r'\bcontent\s*=\s*"([^"]+)"', meta, re.I).group(1)
        addresses.append(url)
        links.append(re.findall(r'<a\s+href\s*=\s*"([^"]+)"', page, re.I))
        basic.append(re.findall(r'[a-z]+', page.lower()).count(word))
    index = {url: i for i, url in enumerate(addresses)}
    scores = [Fraction(value) for value in basic]
    for i, outgoing in enumerate(links):
        if not outgoing:
            continue
        share = Fraction(basic[i], len(outgoing))
        for url in outgoing:
            if url in index:
                scores[index[url]] += share
    return max(range(len(pages)), key=lambda i: scores[i])

# 전체 코드 줄별 설명
# import re  # import는 모듈 가져오기. re는 문자열에서 특정 패턴을 찾는 정규 표현식 도구.
# from fractions import Fraction  # Fraction은 분자·분모로 유리수를 정확하게 표현하는 자료형. 링크 점수의 소수 오차 방지.
# 
# def solution(word, pages):  # def는 함수 정의. 검색 단어와 HTML 문자열 목록을 받음.
#     word = word.lower()  # lower는 소문자로 변환. 검색 단어의 대소문자 차이 제거.
#     addresses, links, basic = [], [], []  # []는 리스트. 페이지 주소·외부 링크·기본 점수를 각각 저장.
#     for page in pages:  # for로 각 HTML 문자열 순회.
#         meta = re.search(r'<meta\b[^>]*\bproperty\s*=\s*"og:url"[^>]*>', page, re.I).group()  # search는 첫 패턴 검색, group은 매칭 문자열. r은 원시 문자열, \b는 단어 경계, [^>]는 > 이외 문자, *는 0회 이상, \s는 공백, re.I는 대소문자 무시.
#         url = re.search(r'\bcontent\s*=\s*"([^"]+)"', meta, re.I).group(1)  # ()는 정규식 캡처 그룹, +는 1회 이상. group(1)은 따옴표 안 content 주소만 추출.
#         addresses.append(url)  # append는 끝에 추가. 현재 페이지 고유 주소 저장.
#         links.append(re.findall(r'<a\s+href\s*=\s*"([^"]+)"', page, re.I))  # findall은 모든 매칭 결과 목록. a 태그의 href 외부 주소를 추출.
#         basic.append(re.findall(r'[a-z]+', page.lower()).count(word))  # [a-z]+는 연속 영문자 단어, count는 완전 일치 개수. 숫자·특수 문자를 단어 구분자로 처리.
#     index = {url: i for i, url in enumerate(addresses)}  # {}는 딕셔너리 컴프리헨션. enumerate로 주소→페이지 인덱스 표 생성.
#     scores = [Fraction(value) for value in basic]  # 리스트 컴프리헨션. 기본 점수를 정확한 분수로 변환해 최종 점수의 초깃값 생성.
#     for i, outgoing in enumerate(links):  # 각 페이지 번호와 그 페이지의 외부 링크 목록 순회.
#         if not outgoing:  # not은 부정. 링크가 없는 페이지는 나누기를 하지 않음.
#             continue  # 이번 반복 건너뜀.
#         share = Fraction(basic[i], len(outgoing))  # len은 링크 수. 기본 점수÷외부 링크 수를 정확한 분수로 계산.
#         for url in outgoing:  # 외부 링크를 하나씩 확인.
#             if url in index:  # in은 키 포함 여부. 입력 목록 안에 있는 페이지에만 점수 반영.
#                 scores[index[url]] += share  # []로 목적지 점수 조회, +=는 더해 저장. 기본 점수만 분배하고 받은 점수는 재분배하지 않음.
#     return max(range(len(pages)), key=lambda i: scores[i])  # max는 최댓값 선택, key는 비교 기준, lambda는 짧은 익명 함수. 동점이면 먼저 나온 가장 작은 인덱스 선택.

# 풀이 요약
# HTML에서 페이지 주소와 외부 링크를 추출하고, 영문자끼리 이어진 단어만 비교해 기본 점수를 센다. 각 링크에 기본 점수/외부 링크 수를 한 번 분배한다.
# 예제 1은 기본 점수 3·1·1에 링크 점수를 더해 4.5·4·1.5가 되어 0번이 이긴다. 목록 밖으로 향하는 링크도 분모에는 포함한다.
# 전체 HTML 길이 S, 전체 링크 수 E일 때 파싱·집계는 O(S+E). 분수 계산 비용은 분모 크기에 따르며 페이지는 최대 20개다. 공간 O(S+E).
# 