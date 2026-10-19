# HTML 파서로 주소와 링크를 읽고 정확한 분수로 점수를 계산합니다.
from html.parser import HTMLParser
from fractions import Fraction
import re

class Page(HTMLParser):
    def __init__(self,text):
        super().__init__();self.url=None;self.links=[];self.feed(text)
    def handle_starttag(self,tag,attrs):
        values=dict(attrs)
        if tag=='meta' and values.get('property')=='og:url':self.url=values.get('content')
        if tag=='a' and values.get('href'):self.links.append(values['href'])

def solution(word,pages):
    parsed=[Page(page) for page in pages]
    base=[sum(token.lower()==word.lower() for token in re.findall(r'[A-Za-z]+',page)) for page in pages]
    score=list(map(Fraction,base));index={page.url:i for i,page in enumerate(parsed)}
    for i,page in enumerate(parsed):
        if not page.links:continue
        share=Fraction(base[i],len(page.links))
        for url in page.links:
            if url in index:score[index[url]]+=share
    return max(range(len(pages)),key=lambda i:(score[i],-i))
