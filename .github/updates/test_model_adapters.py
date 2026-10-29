import json
from pathlib import Path
import unittest

from model_adapters import detail, discover, eligible


CONFIG = json.loads(Path(__file__).with_name("model_sources.json").read_text(encoding="utf-8"))
SOURCES = {source["id"]: source for source in CONFIG["sources"]}


class ModelAdaptersTest(unittest.TestCase):
    def test_anthropic_title_description_and_publisher_date(self):
        html = '<article><time>Oct 7, 2026</time><a href="/claude-newname-9"><h2>Introducing Claude Newname 9</h2><p>A new model for coding.</p></a></article>'
        rows = discover(SOURCES["anthropic"], html)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["date"], "2026-10-07")
        self.assertEqual(rows[0]["description"], "A new model for coding.")

    def test_news_table_sibling_date(self):
        html = '<div class="details"><div>Oct 9, 2026</div><a href="/claude-future-10"><h3>Introducing Claude Future 10</h3></a><a href="/claude-future-10"><p>Our new model.</p></a></div>'
        rows = discover(SOURCES["anthropic"], html)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["date"], "2026-10-09")

    def test_new_anthropic_model_family_is_not_fixed_to_claude_name(self):
        html = '<article><time>Oct 12, 2026</time><a href="/introducing-new-family"><h2>Introducing Novamind</h2><p>Our new frontier model.</p></a></article>'
        rows = discover(SOURCES["anthropic"], html)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["title"], "Introducing Novamind")

    def test_category_and_evaluation_update_are_not_new_models(self):
        html = '<article><a href="/news/announcements">Announcements</a><p>Our model announcement category.</p></article><article><a href="/news/evaluators"><h2>An update on independent evaluators</h2><p>Evaluation of our frontier models.</p></a></article>'
        self.assertEqual(discover(SOURCES["anthropic"], html), [])

    def test_deepseek_separate_section_urls_and_no_search_product(self):
        html = '<article><h2>Date: 2026-10-17</h2><h3 id="search">Opening up the search API</h3><p>Tool search.</p><h3 id="model-a">DeepSeek-V9 Release</h3><p>A model.</p><h2>Date: 2026-09-01</h2><h3 id="model-b">DeepSeek-V8 Update</h3><p>Another model.</p></article>'
        rows = discover(SOURCES["deepseek"], html)
        self.assertEqual([r["date"] for r in rows], ["2026-10-17", "2026-09-01"])
        self.assertTrue(rows[0]["url"].endswith("#model-a"))
        self.assertTrue(rows[1]["url"].endswith("#model-b"))
        self.assertEqual(detail(SOURCES["deepseek"], '<meta property="og:title" content="Change Log">', rows[0]["url"]), {})

    def test_kimi_card_and_footer_deduplication(self):
        html = '<main><div class="menu-card"><a href="/en/blog/kimi-k9" aria-label="Kimi K9"></a><h4 class="card-title">Kimi K9</h4><p class="card-date">2026-10-24</p></div><div class="menu-card"><a href="/en/blog/bench"></a><h4 class="card-title">PerceptionBench</h4></div></main><footer><a href="/en/blog/kimi-k9">Kimi K9 tech blog</a></footer>'
        rows = discover(SOURCES["kimi"], html)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["date"], "2026-10-24")

    def test_official_hub_only_and_no_quantized_variant(self):
        models = [
            {"id":"Qwen/Qwen9-Next", "createdAt":"2026-10-01T01:00:00Z", "lastModified":"2026-10-29T00:00:00Z", "pipeline_tag":"text-generation", "sha":"abc"},
            {"id":"Qwen/Qwen9-Next-FP8", "pipeline_tag":"text-generation"},
            {"id":"somebody/Qwen9-Next", "pipeline_tag":"text-generation"},
            {"id":"Qwen/Qwen9-Image", "pipeline_tag":"text-to-image"},
        ]
        rows = discover(SOURCES["qwen"], json.dumps(models))
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["date"], "2026-10-01")
        self.assertEqual(rows[0]["published_kind"], "repository_created")
        self.assertEqual(rows[0]["revision"], "abc")

    def test_repository_modified_time_is_not_release_date(self):
        html = '<meta property="article:published_time" content="2026-10-29"><meta name="description" content="A new model">'
        result = detail(SOURCES["qwen"], html, "https://huggingface.co/Qwen/Qwen9")
        self.assertNotIn("date", result)

    def test_hub_revision_and_modified_date_do_not_change_registration(self):
        first = {"id":"zai-org/GLM-9", "createdAt":"2026-01-03T00:00:00Z", "lastModified":"2026-02-01T00:00:00Z", "sha":"old", "pipeline_tag":"text-generation"}
        second = dict(first, lastModified="2026-10-29T00:00:00Z", sha="new")
        old = discover(SOURCES["zai"], json.dumps([first]))[0]
        new = discover(SOURCES["zai"], json.dumps([second]))[0]
        self.assertEqual(old["date"], new["date"])
        self.assertEqual(old["url"], new["url"])

    def test_invalid_date_and_task_specific_application_exclusion(self):
        models = [{"id":"Qwen/Qwen-Drive-9B", "createdAt":"2026-01-01T00:00:00Z", "pipeline_tag":"image-text-to-text"}, {"id":"Qwen/Qwen9-Next", "createdAt":"2026-99-01T00:00:00Z", "pipeline_tag":"text-generation"}]
        rows = discover(SOURCES["qwen"], json.dumps(models))
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["date"], "")

    def test_missing_date_stays_missing(self):
        html = '<meta property="og:title" content="Kimi K9"><script type="application/ld+json">{"dateModified":"2026-10-24"}</script>'
        self.assertNotIn("date", detail(SOURCES["kimi"], html, "https://www.kimi.com/en/blog/kimi-k9"))

    def test_native_release_and_unknown_future_family(self):
        self.assertTrue(eligible(SOURCES["openai-ko"], {"url":"https://openai.com/ko-KR/index/new-model", "title":"새 추론 모델을 공개합니다", "description":"추론 모델의 소개입니다."}))
        self.assertTrue(eligible(SOURCES["openai-en"], {"url":"https://openai.com/index/new-family", "title":"Introducing Novamind", "description":"Our new frontier model."}))

    def test_customer_story_is_not_model_release(self):
        for title in ["How X uses GPT-9 for coding", "OpenAI and X expand partnership", "GPT-9 customer case study", "GPT-9로 업무를 바꾸는 고객 사례", "Introducing the GPT-9 academic plan", "Introducing the Claude 9 plugin"]:
            self.assertFalse(eligible(SOURCES["openai-en"], {"url":"https://openai.com/index/story", "title":title, "description":"A new model."}), title)

    def test_official_rss_customer_categories_and_vertical_product(self):
        cases = [
            {"url":"https://openai.com/ko-KR/index/higgsfield-from-prompt-to-production-with-astra", "title":"Higgsfield AI, GPT-6 Astra로 하루 만에 새 동영상 기능 출시", "categories":["스타트업"], "description":"동영상 광고 제작을 돕습니다."},
            {"url":"https://openai.com/ko-KR/index/airbnb-gpt-6-astra", "title":"에어비앤비, GPT-6 Astra 및 OpenAI 프런티어 모델 이용 확대", "categories":["회사"], "description":"모델 이용을 확대합니다."},
            {"url":"https://openai.com/index/astra-for-law", "title":"Introducing Astra for Law", "categories":["Company"], "description":"OpenAI for Law brings frontier intelligence for law, custom firm workflows and connected data."},
        ]
        for item in cases:
            self.assertFalse(eligible(SOURCES["openai-ko"], item), item["title"])

    def test_company_category_can_still_contain_real_model_launch(self):
        self.assertTrue(eligible(SOURCES["openai-en"], {"url":"https://openai.com/index/introducing-gpt-5-4-mini-and-nano", "title":"Introducing GPT-5.4 mini and nano", "categories":["Company"], "description":"Two smaller faster models."}))
        self.assertTrue(eligible(SOURCES["openai-ko"], {"url":"https://openai.com/ko-KR/index/gpt-6-for-everyone", "title":"모두를 위한 GPT-6과 Intelligent UI", "categories":["제품"], "description":"GPT-6가 전 세계 사용자에게 제공됩니다."}))

    def test_external_links_and_unknown_adapter_fail(self):
        self.assertFalse(eligible(SOURCES["anthropic"], {"url":"https://attacker.example/introducing", "title":"Introducing Claude New 9"}))
        with self.assertRaises(ValueError):
            discover({"adapter":"unknown"}, "")


if __name__ == "__main__":
    unittest.main()
