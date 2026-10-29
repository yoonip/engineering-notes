"""Small source-shaped fixtures for official technology/industry metadata."""
import unittest
import sector_adapters as a


def source(adapter):
    return {'url':'https://example.org/list','adapter':adapter,'hosts':['example.org'],'series':'AI 브리프'}


class SectorAdapterTests(unittest.TestCase):
    def test_magazine_contents_without_sty3_and_footer_are_separated(self):
        text = '<div class="txt_box"><div class="txt_list"><ul class="info_list"><li>AI 투자와 NPU 산업</li></ul></div></div><footer><div class="txt_box"><div class="txt_list"><p class="info_list">푸터 주소</p></div></div></footer>'
        row = a.detail(source('sector_spri'), text, 'https://example.org/posts/view/12')
        self.assertIn('AI 투자와 NPU 산업', row['description'])
        self.assertNotIn('푸터 주소', row['description'])

    def test_spri_issue_identity_and_month_precision(self):
        text='<ul class="list"><li><a href="/posts/view/12?code=AI-Brief&data_page=1">자세히보기</a><div class="text_box"><div class="data">2026년 10월호</div></div></li></ul>'
        rows=a.discover(dict(source('sector_spri'),url='https://example.org/posts?code=AI-Brief'),text)
        self.assertEqual(rows[0]['url'],'https://example.org/posts/view/12?code=AI-Brief')
        self.assertEqual(rows[0]['date'],'2026-10')
        self.assertEqual(rows[0]['title'],'AI 브리프 · 2026년 10월호')

    def test_spri_visible_contents_win_over_stale_generic_meta(self):
        text='''<meta property="og:description" content="오래된 잘못된 메타 소개"><div class="view_top_box"><h3 class="title">2026년 10월호</h3><div class="data sty2">날짜 2026.10.12</div><button onclick="file_down('77');">PDF</button></div><div class="txt_box"><div class="info_list sty3">기술·연구 새롭게 발표된 반도체와 소프트웨어 연구를 다룹니다.</div></div>'''
        row=a.detail(source('sector_spri'),text,'https://example.org/posts/view/12')
        self.assertEqual(row['date'],'2026-10-12')
        self.assertIn('새롭게 발표된',row['description'])
        self.assertNotIn('잘못된',row['description'])
        self.assertEqual(row['pdf_url'],'https://example.org/download/77')

    def test_kistep_stable_report_id_and_not_hit_count(self):
        text='''<ul><li><strong class="title"><a href="/board.es?bid=0031&list_no=123&nPage=1&act=view">기술 동향</a></strong><ul class="basic_info"><li><em class="label">등록일</em><span class="txt">2026-10-27</span></li></ul><a href="/boardDownload.es?bid=0031&list_no=123&seq=1">PDF</a></li></ul>'''
        row=a.discover(source('sector_kistep'),text)[0]
        self.assertEqual(row['date'],'2026-10-27')
        self.assertNotIn('nPage',row['url'])
        self.assertIn('list_no=123',row['url'])

    def test_kistep_only_visible_intro_and_official_download(self):
        text='''<article class="board_view"><div class="publication_info"><h2 class="title">기술의 방향</h2><li class="date"><span>2026-10-27</span></li></div><div class="contents"><p>연구개발과 산업 기술의 현재 조건을 분석합니다.</p><p style="display:none">숨긴 내용을 쓰지 않습니다.</p></div><a href="https://evil.invalid/boardDownload.es?bid=1">파일</a></article>'''
        row=a.detail(source('sector_kistep'),text,'https://example.org/board.es?list_no=1')
        self.assertEqual(row['title'],'기술의 방향')
        self.assertNotIn('숨긴',row['description'])
        self.assertEqual(row['pdf_url'],'')

    def test_kari_printed_contents_not_generated_summary_modal(self):
        text='''<div class="bod-program-list"><ul class="pdf"><li><div class="desc"><strong>인사이트 Vol.7</strong><ul><li><em>작성일</em>2026-10-01</li><li><em>다운로드</em>120000</li></ul><a class="down" href="/attach/abc123/def456">다운로드</a></div><div class="desc ty2">우주 반도체의 현황 / 연구자</div></li></ul></div><div class="summary">AI가 만든 추측 요약</div>'''
        row=a.discover(source('sector_kari'),text)[0]
        self.assertEqual(row['date'],'2026-10-01')
        self.assertEqual(row['url'],'https://example.org/attach/abc123/def456')
        self.assertNotIn('AI가 만든',row['description'])
        self.assertTrue(row['description'].startswith('목차:'))

    def test_kari_no_date_is_not_invented(self):
        text='<div class="bod-program-list"><ul class="pdf"><li><div class="desc"><strong>발간물</strong><a class="down" href="/attach/abc/def">PDF</a></div></li></ul></div>'
        self.assertEqual(a.discover(source('sector_kari'),text)[0]['date'],'')

    def test_missing_nodes_return_empty_not_navigation(self):
        for adapter in ('sector_spri','sector_kistep','sector_kari'):
            self.assertEqual(a.discover(source(adapter),'<nav><a href="/index">홈</a></nav>'),[])

    def test_unsupported_adapter_and_invalid_date(self):
        with self.assertRaises(ValueError):a.discover(source('unknown'),'')
        with self.assertRaises(ValueError):a.detail(source('unknown'),'','https://example.org')
        self.assertEqual(a._date('2026-13-45'),'')


if __name__=='__main__':unittest.main()
