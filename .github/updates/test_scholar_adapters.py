"""Small structural fixtures for paper identities and public course descriptions."""
import unittest
import scholar_adapters as s


class ScholarAdapterTests(unittest.TestCase):
    def test_arxiv_cross_listing_and_version_share_publication_identity(self):
        source = {'adapter': 'arxiv', 'hosts': ['arxiv.org']}
        first = s.prepare_item(source, {'title': 'A hardware benchmark', 'url': 'https://arxiv.org/abs/2610.12345',
                                        'description': 'arXiv:2610.12345v1 Announce Type: new Abstract: We test memory traffic.'})
        second = s.prepare_item(source, {'title': 'A hardware benchmark', 'url': 'https://arxiv.org/abs/2610.12345v2',
                                         'description': 'arXiv:2610.12345v2 Announce Type: cross Abstract: We test memory traffic.'})
        self.assertEqual(first['url'], second['url'])
        self.assertEqual(first['description'], second['description'])
        self.assertEqual(second['version'], '2')
        self.assertEqual(first['kind'], '프리프린트 초록')

    def test_title_filter_is_subject_scope_not_citation_ranking(self):
        source = {'adapter': 'arxiv', 'hosts': ['arxiv.org'], 'title_patterns': [r'\b(?:survey|benchmark)\b']}
        self.assertTrue(s.eligible(source, {'url': 'https://arxiv.org/abs/2610.12345', 'title': 'A Survey of Hardware Models'}))
        self.assertFalse(s.eligible(source, {'url': 'https://arxiv.org/abs/2610.12345', 'title': 'A Particular Model'}))

    def test_arxiv_bad_id_and_external_host_are_rejected(self):
        source = {'adapter': 'arxiv', 'hosts': ['arxiv.org']}
        self.assertFalse(s.eligible(source, {'url': 'https://arxiv.org/search', 'title': 'A Survey'}))
        self.assertFalse(s.eligible(source, {'url': 'https://evil.invalid/abs/2610.12345', 'title': 'A Survey'}))

    def test_mit_research_notice_is_not_award_or_appointment(self):
        source = {'adapter': 'mit_research', 'hosts': ['news.mit.edu']}
        self.assertFalse(s.eligible(source, {'url': 'https://news.mit.edu/award', 'title': 'MIT scientist wins award', 'description': 'AI researchers'}))
        self.assertTrue(s.eligible(source, {'url': 'https://news.mit.edu/research', 'title': 'A new memory design', 'description': 'Researchers report a study.'}))

    def test_learning_award_and_learner_story_are_not_new_material(self):
        source = {'adapter': 'ocw_notices', 'hosts': ['www.ocw-openmatters.org']}
        self.assertFalse(s.eligible(source, {'url': 'https://www.ocw-openmatters.org/award/', 'title': 'MIT OpenCourseWare Wins an Award'}))
        self.assertFalse(s.eligible(source, {'url': 'https://www.ocw-openmatters.org/story/', 'title': 'How MIT Courses Inspired a Doctoral Journey'}))
        self.assertTrue(s.eligible(source, {'url': 'https://www.ocw-openmatters.org/book/', 'title': 'Learners develop a book of AI insights'}))

    def test_kmooc_card_does_not_turn_course_period_into_publication_date(self):
        source = {'adapter': 'kmooc', 'url': 'https://www.kmooc.kr/', 'hosts': ['www.kmooc.kr']}
        text = '''<li class="card_item"><a href="/view/course/detail/42"><strong class="title">회로와 컴퓨터</strong>
                  <p class="institution">국립대학교</p><div class="date">2026.10.16 ~ 2026.12.14</div></a></li>'''
        rows = s.discover(source, text)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]['date'], '')
        self.assertIn('2026.10.16', rows[0]['course_period'])

    def test_kmooc_duplicate_cards_and_external_pages_are_not_added(self):
        source = {'adapter': 'kmooc', 'url': 'https://www.kmooc.kr/', 'hosts': ['www.kmooc.kr']}
        text = ('<li class="card_item"><a href="/view/course/detail/42"><strong class="title">회로</strong></a></li>' * 2
                + '<li class="card_item"><a href="https://evil.invalid/42"><strong class="title">위조</strong></a></li>')
        self.assertEqual(len(s.discover(source, text)), 1)

    def test_kmooc_detail_uses_course_objectives_not_related_course_titles(self):
        source = {'adapter': 'kmooc', 'hosts': ['www.kmooc.kr']}
        text = '''<title>회로와 컴퓨터 | K-MOOC</title><strong class="title">다른 추천 강좌</strong>
                  <article><h3>수업내용/목표</h3><p>회로와 자료의 흐름을 설명하는 과정입니다.</p>
                  <h3>강좌 미리보기</h3><p>미리보기 광고</p></article>'''
        row = s.detail(source, text, 'https://www.kmooc.kr/view/course/detail/42')
        self.assertEqual(row['title'], '회로와 컴퓨터')
        self.assertEqual(row['date'], '')
        self.assertNotIn('광고', row['description'])

    def test_wrong_html_adapter_fails_and_feed_detail_has_no_network(self):
        with self.assertRaises(ValueError):
            s.discover({'adapter': 'unknown'}, '<html/>')
        self.assertEqual(s.detail({'adapter': 'arxiv'}, '<html/>', 'https://arxiv.org/abs/2610.12345'), {})


if __name__ == '__main__':
    unittest.main()
