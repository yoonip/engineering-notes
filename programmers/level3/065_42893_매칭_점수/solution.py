# re는 문자열에서 특정 패턴을 찾는 정규 표현식 도구.
import re
# 링크 점수의 소수 오차 방지.
from fractions import Fraction

# 검색 단어와 HTML 문자열 목록을 받음.
def solution(word, pages):
    # 검색 단어의 대소문자 차이 제거.
    word = word.lower()
    # 페이지 주소·외부 링크·기본 점수를 각각 저장.
    addresses, links, basic = [], [], []
    # for로 각 HTML 문자열 순회.
    for page in pages:
        # r은 원시 문자열, \b는 단어 경계, [^>]는 > 이외 문자, *는 0회 이상, \s는 공백, re.I는 대소문자 무시.
        meta = re.search(r'<meta\b[^>]*\bproperty\s*=\s*"og:url"[^>]*>', page, re.I).group()
        # group(1)은 따옴표 안 content 주소만 추출.
        url = re.search(r'\bcontent\s*=\s*"([^"]+)"', meta, re.I).group(1)
        # 현재 페이지 고유 주소 저장.
        addresses.append(url)
        # a 태그의 href 외부 주소를 추출.
        links.append(re.findall(r'<a\s+href\s*=\s*"([^"]+)"', page, re.I))
        # 숫자·특수 문자를 단어 구분자로 처리.
        basic.append(re.findall(r'[a-z]+', page.lower()).count(word))
    # enumerate로 주소→페이지 인덱스 표 생성.
    index = {url: i for i, url in enumerate(addresses)}
    # 기본 점수를 정확한 분수로 변환해 최종 점수의 초깃값 생성.
    scores = [Fraction(value) for value in basic]
    # 각 페이지 번호와 그 페이지의 외부 링크 목록 순회.
    for i, outgoing in enumerate(links):
        # 링크가 없는 페이지는 나누기를 하지 않음.
        if not outgoing:
            # 이번 반복 건너뜀.
            continue
        # 기본 점수÷외부 링크 수를 정확한 분수로 계산.
        share = Fraction(basic[i], len(outgoing))
        # 외부 링크를 하나씩 확인.
        for url in outgoing:
            # 입력 목록 안에 있는 페이지에만 점수 반영.
            if url in index:
                # 기본 점수만 분배하고 받은 점수는 재분배하지 않음.
                scores[index[url]] += share
    # 동점이면 먼저 나온 가장 작은 인덱스 선택.
    return max(range(len(pages)), key=lambda i: scores[i])
