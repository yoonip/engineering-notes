"""Parse public model announcements; this module makes no network requests."""

from __future__ import annotations

import json
import re
from datetime import date as calendar_date, datetime
from urllib.parse import urljoin, urlsplit

from bs4 import BeautifulSoup


MODEL_NAME = re.compile(
    r"(?:GPT[\s\-‑]?\d|\bo\d\b|Claude\s+(?!Code\b)[\w.-]+\s*\d|"
    r"Gemini\s*\d|Gemma\s*\d|Genie\s*\d|Veo\s*\d|Imagen\s*\d|"
    r"DeepSeek[\s-]?(?:V|R)?\d|Qwen\s*\d|GLM[\s-]?\d|Kimi\s+[^:]{0,35}\d)",
    re.I,
)
ANNOUNCEMENT = re.compile(
    r"\b(?:introduc\w*|announc\w*|releas\w*|launch\w*|new|next|updat\w*)\b|"
    r"소개|공개|출시|발표|새로운|새 모델|업데이트|제공|확대|확장",
    re.I,
)
NEW_FAMILY = re.compile(
    r"\b(?:introducing|announcing|releasing|launching|meet)\b|"
    r"\bnew\b.{0,35}\b(?:model|frontier)\b|"
    r"모델.{0,20}(?:공개|출시|발표)|(?:새|신규).{0,20}모델",
    re.I,
)
NON_MODEL = re.compile(
    r"partnership|partnering|customer|case study|\b(?:program|programme|certification)\b|검증 프로그램|how .{1,65} (?:uses?|is using)|"
    r"powered by|\b(?:hiring|careers?|webinar|meetup|hackathon|pop-up|pop up)\b|"
    r"\b(?:plugin|newsletter|academic plan|subscription|fund|partnership)\b|"
    r"학술 플랜|파트너십|고객 사례|활용 사례|사용 사례|커리어|팝업|밋업|"
    r"workflow.{0,15}(?:with|using)|with.{0,20}workflows?",
    re.I,
)
VARIANT = re.compile(
    r"(?:^|[-_])(?:FP\d+|BF\d+|INT\d+|GPTQ|AWQ|GGUF|EXL\d*|Base|"
    r"Adapter|LoRA|Eagle\d*|DFlash)(?:$|[-_])|\b(?:test|experimental)\b",
    re.I,
)
MODEL_TASKS = {"text-generation", "image-text-to-text", "any-to-any"}


def _text(node) -> str:
    return " ".join(node.get_text(" ", strip=True).replace("\u200b", "").split()) if node else ""


def _date(value: str) -> str:
    """Normalize a date actually printed by the publisher; never infer a year."""
    value = " ".join(value.split())
    match = re.search(r"\b(20\d{2}-\d{2}-\d{2})(?:T|\b)", value)
    if match:
        try:
            return calendar_date.fromisoformat(match.group(1)).isoformat()
        except ValueError:
            return ""
    for fmt in ("%b %d, %Y", "%B %d, %Y"):
        try:
            return datetime.strptime(value, fmt).date().isoformat()
        except ValueError:
            pass
    return ""


def _allowed(source: dict, url: str) -> bool:
    parsed = urlsplit(url)
    return parsed.scheme == "https" and parsed.hostname in source.get("hosts", [])


def eligible(source: dict, item: dict) -> bool:
    """Keep model releases and access updates, excluding customer/product stories."""
    if not _allowed(source, item.get("url", "")):
        return False
    title = item.get("title", "")
    if not title or NON_MODEL.search(title):
        return False
    if item.get("kind") == "weights":
        return not VARIANT.search(title)
    description = item.get("description", "")
    access_update = False
    if source.get("provider") == "OpenAI" or source.get("id", "").startswith("openai-"):
        categories = {str(category).strip().casefold() for category in item.get("categories", [])}
        customer_categories = {
            "startup", "스타트업", "story", "스토리", "ai adoption", "ai 도입",
            "applied ai", "ai 활용 사례", "customer stories", "customer story",
            "guides", "가이드", "webinar", "webinars", "웨비나",
        }
        if categories & customer_categories:
            return False
        slug = urlsplit(item["url"]).path.rstrip("/").rsplit("/", 1)[-1]
        model_path = re.match(
            r"^(?:introducing-|announcing-|new-)?(?:gpt(?:-|$)|o\d(?:-|$)|sora(?:-|$)|dall-e(?:-|$))",
            slug, re.I,
        )
        release_title = re.match(r"^(?:introducing|announcing|releasing|meet)\b", title, re.I)
        native_release = re.match(r"^(?:GPT|Sora|o\d)[^,，]{0,70}(?:소개|공개|출시|발표)", title, re.I)
        new_model_title = NEW_FAMILY.search(title) and re.search(r"\bmodels?\b|모델", title + " " + description, re.I)
        access_update = bool(model_path and re.search(
            r"for-everyone|for-developers|모두를 위한|개발자를 위한|전 세계.{0,20}제공|available in the API",
            title + " " + slug + " " + description, re.I,
        ))
        # Company posts can be genuine launches, but model use by a customer is not one.
        # Requiring a release-oriented route/title also avoids brand-name allowlists.
        if not (model_path or release_title or native_release or new_model_title):
            return False
    if MODEL_NAME.search(title):
        # A model name alone in a customer story is insufficient evidence of a release.
        return bool(access_update or ANNOUNCEMENT.search(title) or re.match(r"^(?:Gemini|Gemma|Genie|Veo|Imagen|Kimi)\b", title, re.I))
    # Future model families need not appear in a hard-coded version list.
    return bool(NEW_FAMILY.search(title) and re.search(r"\bmodels?\b|모델", title + " " + description, re.I))


def _unique(items: list[dict]) -> list[dict]:
    unique = {}
    for item in items:
        old = unique.get(item["url"])
        if old is None or (bool(item.get("date")), len(item.get("description", ""))) > (bool(old.get("date")), len(old.get("description", ""))):
            unique[item["url"]] = item
    return list(unique.values())


def _anthropic(source: dict, soup: BeautifulSoup) -> list[dict]:
    items = []
    for anchor in soup.find_all("a", href=True):
        url = urljoin(source["url"], anchor["href"])
        if not _allowed(source, url):
            continue
        heading = anchor.find(["h1", "h2", "h3", "h4"])
        title = _text(heading) if heading else _text(anchor)
        if not heading and not MODEL_NAME.search(title):
            continue
        container = anchor.find_parent(["article", "li", "tr"])
        if container is None:
            # Current table rows keep title and date in a compact sibling region.
            container = anchor.find_parent("div", class_=lambda value: value and "details" in value)
        date = ""
        description = _text(anchor.find("p"))
        if container is not None:
            time = container.find("time")
            date = _date(time.get("datetime", "") or _text(time)) if time else ""
            if not date:
                match = re.search(r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w* \d{1,2}, 20\d{2}\b", _text(container))
                date = _date(match.group(0)) if match else ""
            if not description:
                description = _text(container.find("p"))
        item = {"url": url, "title": title, "date": date, "description": description[:600]}
        if eligible(source, item):
            items.append(item)
    return _unique(items)


def _deepseek(source: dict, soup: BeautifulSoup) -> list[dict]:
    article = soup.find("article") or soup
    date = ""
    items = []
    for heading in article.find_all(["h2", "h3"]):
        title = _text(heading)
        if heading.name == "h2":
            date = _date(title)
            continue
        anchor = heading.get("id")
        if not anchor:
            continue
        parts = []
        for sibling in heading.next_siblings:
            if getattr(sibling, "name", None) in ("h2", "h3"):
                break
            if getattr(sibling, "name", None) in ("p", "ul", "ol"):
                parts.append(_text(sibling))
        item = {"url": source["url"].split("#", 1)[0].rstrip("/") + "/#" + anchor,
                "title": title, "date": date, "description": " ".join(parts)[:600]}
        if eligible(source, item):
            items.append(item)
    return _unique(items)


def _kimi(source: dict, soup: BeautifulSoup) -> list[dict]:
    items = []
    main = soup.find("main") or soup
    cards = main.select(".menu-card")
    for card in cards:
        anchor = card.find("a", href=True)
        if not anchor:
            continue
        title = _text(card.select_one(".card-title")) or anchor.get("aria-label", "") or _text(anchor)
        date = _date(_text(card.select_one(".card-date")))
        description = _text(card.select_one(".card-description"))
        item = {"url": urljoin(source["url"], anchor["href"]), "title": title,
                "date": date, "description": description[:600]}
        if eligible(source, item):
            items.append(item)
    return _unique(items)


def _hub(source: dict, text: str) -> list[dict]:
    models = json.loads(text)
    if not isinstance(models, list):
        raise ValueError("Official Hub model list is not an array")
    org = source["organization"]
    items = []
    for model in models:
        model_id = model.get("id", "")
        if not model_id.startswith(org + "/") or model.get("private") or model.get("disabled"):
            continue
        name = model_id.split("/", 1)[1]
        if not any(name.startswith(prefix) for prefix in source.get("model_prefixes", [""])):
            continue
        if any(re.search(pattern, name, re.I) for pattern in source.get("exclude_model_patterns", [])):
            continue
        if VARIANT.search(name) or model.get("pipeline_tag") not in MODEL_TASKS:
            continue
        item = {"url": "https://huggingface.co/" + model_id, "title": model_id,
                "date": _date(model.get("createdAt", "")), "description": model.get("description") or "",
                "kind": "weights", "published_kind": "repository_created",
                "revision": model.get("sha", ""), "pipeline_tag": model.get("pipeline_tag", "")}
        if eligible(source, item):
            items.append(item)
    return _unique(items)


def discover(source: dict, text: str) -> list[dict]:
    """Read an already-fetched source response using its declared adapter."""
    adapter = source.get("adapter")
    if adapter == "huggingface_models":
        return _hub(source, text)
    soup = BeautifulSoup(text, "html.parser")
    parsers = {"anthropic_news": _anthropic, "deepseek_updates": _deepseek, "kimi_blog": _kimi}
    if adapter not in parsers:
        raise ValueError("Unknown model adapter: " + str(adapter))
    return parsers[adapter](source, soup)


def detail(source: dict, text: str, url: str) -> dict:
    """Read page metadata without turning modification dates into release dates."""
    soup = BeautifulSoup(text, "html.parser")
    result = {}
    title = soup.find("meta", property="og:title")
    description = soup.find("meta", property="og:description") or soup.find("meta", attrs={"name": "description"})
    if title and title.get("content"):
        result["title"] = title["content"]
    if description and description.get("content") and not description["content"].startswith("We’re on a journey"):
        result["description"] = description["content"][:600]
    published = soup.find("meta", property="article:published_time")
    time = soup.find("time", datetime=True)
    if published:
        result["date"] = _date(published.get("content", ""))
    elif time:
        result["date"] = _date(time.get("datetime", ""))
    canonical = soup.find("link", rel="canonical")
    if canonical and canonical.get("href") and _allowed(source, canonical["href"]):
        result["canonical"] = canonical["href"]
    # The updates URL includes a section identity; generic page metadata would erase it.
    if source.get("adapter") == "deepseek_updates":
        return {}
    if source.get("adapter") == "huggingface_models":
        # Hub's generic page timestamps describe a repository, not a launch.
        result.pop("date", None)
        result.pop("canonical", None)
    return result
