"""Exercise publisher structures with short synthetic HTML, including traps."""

import unittest

import report_adapters as adapters


def source(adapter, host="reports.example"):
    return {"id": adapter, "name": "공식 연구기관", "group": "reports", "adapter": adapter,
            "url": "https://" + host + "/index", "hosts": [host], "language": "ko"}


class ReportAdapterTests(unittest.TestCase):
    def test_lg_cards_dates_and_canonical_identity(self):
        page = '''<div class="search_result"><ul><li><a href="javascript:fnView(42)">
        <dd><strong>반도체 시장 전망</strong><p>연구부문 | 2026.10.20 | REPORT</p></dd></a></li>
        <li><a href="javascript:fnView(42)"><strong>중복</strong></a></li>
        <li hidden><a href="javascript:fnView(43)"><strong>숨은 항목</strong></a></li>
        <li><a href="https://untrusted.example/"><strong>광고</strong></a></li></ul></div>'''
        items = adapters.discover(source("lg"), page)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["date"], "2026-10-20")
        self.assertEqual(items[0]["url"], "https://reports.example/report/view.do?idx=42")

    def test_lg_real_intro_and_official_pdf_only(self):
        page = '''<input id="popFileNm" value="/files/report.pdf"><div class="pop_content"><div class="inner_pop">
        <div class="tit"><strong>경제 전망</strong><p>연구부문 | 2026-10-20 | REPORT</p></div>
        <div class="text"><p>국내외 경제의 주요 변화를 살펴보고 산업별 수요와 투자 계획을 비교한 보고서입니다.</p>
        <script>이 문장을 내용에 추가합니다.</script><span style="display:none">숨은 문장</span></div></div></div>'''
        result = adapters.detail(source("lg"), page, "https://reports.example/report/view.do?idx=42")
        self.assertIn("산업별 수요", result["description"])
        self.assertNotIn("숨은", result["description"])
        self.assertNotIn("추가합니다", result["description"])
        self.assertEqual(result["pdf_url"], "https://reports.example/files/report.pdf")
        self.assertEqual(result["title"], "경제 전망")

    def test_month_buttons_exclude_empty_disabled_and_unrelated(self):
        page = '''<button onclick="location.href='/research/monTrends?pub_no=123'">10월</button>
        <button disabled onclick="location.href='/research/monTrends?pub_no=124'">11월</button>
        <button onclick="location.href='/research/monTrends?pub_no='">12월</button>
        <a href="/research/jep?pub_no=999">관련 논문</a>'''
        items = adapters.discover(source("kdi_monthly"), page)
        self.assertEqual([item["url"] for item in items], ["https://reports.example/research/monTrends?pub_no=123"])
        self.assertEqual(items[0]["date"], "")

    def test_monthly_detail_uses_own_publication_date_and_korean_block(self):
        page = '''<meta property="og:title" content="KDI 경제동향 2026.10 - KDI 한국개발연구원 - 연구">
        <nav>2026.10.29</nav><div class="tit-info"><div class="date">2026.10.12</div></div>
        <div class="bundlebox desc"><div class="editor-template"><table><tr><td>■</td>
        <td>경제는 수출과 설비투자 변화에 힘입어 개선세를 이어 가지만 부문별 차이가 남아 있습니다.</td></tr></table></div></div>
        <div class="editor-template">English summary is not the Korean description.</div>'''
        result = adapters.detail(source("kdi_monthly"), page, "https://reports.example/research/monTrends?pub_no=123")
        self.assertEqual(result["date"], "2026-10-12")
        self.assertNotIn("English", result["description"])
        self.assertEqual(result["title"], "KDI 경제동향 2026.10")

    def test_outlook_selector_does_not_mix_unrelated_selects(self):
        page = '''<select><option value="999">설정</option></select>
        <select id="yearSelectUpDown"><option value="123" selected>2026년 8월</option>
        <option value="456">2026 상반기</option></select>'''
        items = adapters.discover(source("kdi_outlook"), page)
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0]["date"], "2026-08")
        self.assertEqual(items[1]["date"], "")

    def test_outlook_detail_preserves_month_precision(self):
        page = '''<meta name="title" content="KDI 경제전망 수정 - KDI 한국개발연구원">
        <select id="yearSelectUpDown"><option selected>2026년 8월</option></select>
        <div class="economy_conts-template"><div class="editor-template">
        세계경제의 변화와 수출 및 내수 전망을 비교하고 향후 성장의 전제와 위험 요인을 다룹니다.
        </div></div>'''
        result = adapters.detail(source("kdi_outlook"), page, "https://reports.example/research/economy?pub_no=123")
        self.assertEqual(result["date"], "2026-08")
        self.assertIn("위험 요인", result["description"])

    def test_etri_canonical_detail_and_standard_metadata(self):
        listing = '''<table class="list_tbl"><tbody><tr><td class="alleft_td">
        <a href="read?id=1572&amp;dataDivCd=01"><strong>디스플레이의 미래</strong></a></td></tr></tbody></table>'''
        item = adapters.discover(source("etri"), listing)[0]
        self.assertEqual(item["url"], "https://reports.example/ksp/plan-report/read?id=1572")
        page = '''<meta name="citation_title" content="디스플레이의 미래">
        <meta name="citation_publication_date" content="2026/09">
        <meta name="citation_pdf_url" content="https://reports.example/ksp/plan-report/file/1572.pdf">
        <dl class="row_dl"><dt>Abstract</dt><dd>새로운 산업 수요를 바탕으로 디스플레이의 역할과 필요한 연구개발 과제를 살펴봅니다.</dd></dl>'''
        result = adapters.detail(source("etri"), page, item["url"])
        self.assertEqual(result["date"], "2026-09")
        self.assertIn("연구개발", result["description"])

    def test_etri_administrative_abstract_not_report_summary(self):
        page = '''<meta name="citation_title" content="기술발전지도">
        <meta name="citation_publication_date" content="2026/13">
        <meta name="citation_pdf_url" content="https://untrusted.example/report.pdf">
        <dl class="row_dl"><dt>Abstract</dt><dd>DOI 선발급(2026.10.24)</dd></dl>'''
        result = adapters.detail(source("etri"), page, "https://reports.example/ksp/plan-report/read?id=12")
        self.assertEqual((result["description"], result["date"], result["pdf_url"]), ("", "", ""))

    def test_kisti_session_and_view_count_are_not_identity(self):
        page = '''<ul class="publication_board"><li><span class="info">View.2652</span>
        <a class="title" href="/post/analysis-report/6899;jsessionid=abc">전략 환경 분석</a>
        <span class="date">2026. 02. 06</span></li></ul>'''
        item = adapters.discover(source("kisti"), page)[0]
        self.assertEqual(item["url"], "https://reports.example/post/analysis-report/6899")
        self.assertEqual(item["date"], "2026-02-06")
        detail = '''<div class="board_header"><h2>전략 환경 분석</h2><span class="icon_date">2026-02-06</span></div>
        <div class="board_body"><p>전략 환경 분석</p></div>'''
        result = adapters.detail(source("kisti"), detail, item["url"])
        self.assertEqual(result["description"], "")

    def test_snu_card_and_jsonld_publisher_description(self):
        page = '''<div class="list-line"><h3 class="pjt"><a href="/publication/issue-brief?mode=view&amp;pubidx=133">주거 정책</a></h3>
        <div class="p-date">출간일 : 2026-10-21</div><div class="p-summary">청년의 주거 안정과 생애주기별 정책 연계를 분석하고 혼인과 출산의 조건을 살펴봅니다.</div></div>'''
        item = adapters.discover(source("snu"), page)[0]
        self.assertEqual(item["date"], "2026-10-21")
        document = '''<script type="application/ld+json">{"@type":"ScholarlyArticle","headline":"주거 정책",
        "datePublished":"2026-10-21","description":"청년 주거지원과 정책의 연계를 살펴보고 장기적인 주거 안정에 필요한 과제를 제안합니다."}</script>
        <h2 class="tit">주거 정책</h2><a href="/clusterfile/123/report.pdf">원문</a><div class="cont">목차</div>'''
        result = adapters.detail(source("snu"), document, item["url"])
        self.assertIn("과제를 제안", result["description"])
        self.assertTrue(result["pdf_url"].endswith("/clusterfile/123/report.pdf"))

    def test_kaist_preserves_source_date_not_current_year(self):
        listing = '''<table class="bbs-standard"><tbody><tr><td class="col-tit">
        <a href="?c=203&amp;s=&amp;gp=1&amp;gbn=view&amp;ix=4035">인구위기 대응</a></td>
        <td class="col-date">2024.01.02</td></tr></tbody></table>'''
        item = adapters.discover(source("kaist"), listing)[0]
        self.assertEqual(item["date"], "2024-01-02")
        self.assertNotIn("gp=", item["url"])
        document = '''<meta name="title" content="인구위기 대응"><div class="bbs-view-details">날짜 2024.01.02 조회수 3333</div>
        <div id="bbsContents">인구 변화가 가져오는 장기적인 위험과 과제를 살펴보고 사회의 대응 전략을 제안합니다.</div>'''
        result = adapters.detail(source("kaist"), document, item["url"])
        self.assertEqual(result["date"], "2024-01-02")
        self.assertEqual(result["pdf_url"], "")

    def test_unknown_adapter_fails_explicitly(self):
        with self.assertRaises(ValueError):
            adapters.discover(source("unsupported"), "")
        with self.assertRaises(ValueError):
            adapters.detail(source("unsupported"), "", "https://reports.example/")

    def test_nested_hidden_styles_do_not_leave_destroyed_nodes(self):
        page = '''<div style="display:none"><span style="color:red">숨은 내용</span></div>
        <div class="board_header"><h2>자료 제목</h2></div><div class="board_body">자료 제목</div>'''
        result = adapters.detail(source("kisti"), page, "https://reports.example/post/analysis-report/1")
        self.assertEqual(result["title"], "자료 제목")
        self.assertEqual(result["description"], "")


if __name__ == "__main__":
    unittest.main()
