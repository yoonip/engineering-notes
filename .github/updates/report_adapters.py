"""Parse public Korean report indexes and descriptions without network requests."""

from __future__ import annotations

from datetime import date as calendar_date
import html
import json
import re
from urllib.parse import parse_qs, urlencode, urljoin, urlsplit

from bs4 import BeautifulSoup


def _soup(text: str) -> BeautifulSoup:
    """Discard navigation, executable content and explicitly hidden elements."""
    soup = BeautifulSoup(text, "html.parser")
    for node in list(soup.select("script, style, nav, header, footer, template, [hidden], [aria-hidden='true']")):
        if node.name == "script" and node.get("type") == "application/ld+json":
            continue
        node.decompose()
    for node in list(soup.select("[style]")):
        if node.attrs is None:
            continue
        if re.search(r"(?:display\s*:\s*none|visibility\s*:\s*hidden)", node.get("style", ""), re.I):
            node.decompose()
    return soup


def _text(node) -> str:
    return re.sub(r"\s+", " ", node.get_text(" ", strip=True)).strip() if node else ""


def _meta(soup, key: str) -> str:
    node = soup.find("meta", attrs={"name": key}) or soup.find("meta", attrs={"property": key})
    return str(node.get("content", "")).strip() if node else ""


def _date(text: str) -> str:
    """Keep the source precision; never invent a day for month-only publications."""
    match = re.search(r"(\d{4})\s*[./년-]\s*(\d{1,2})(?:\s*[./월-]\s*(\d{1,2}))?", text)
    if not match:
        return ""
    year, month = int(match[1]), int(match[2])
    day = int(match[3]) if match[3] else None
    try:
        calendar_date(year, month, day or 1)
    except ValueError:
        return ""
    return f"{year:04d}-{month:02d}" + (f"-{day:02d}" if day else "")


def _url(source: dict, value: str, base: str | None = None) -> str:
    """Accept HTTPS links only on the source's explicit publisher hosts."""
    value = html.unescape(value).strip()
    if not value:
        return ""
    result = urljoin(base or source["url"], value)
    parts = urlsplit(result)
    hosts = set(source.get("hosts", [urlsplit(source["url"]).hostname]))
    if parts.scheme != "https" or parts.hostname not in hosts or parts.username or parts.password:
        return ""
    return result.split("#", 1)[0]


def _description(node, title: str = "") -> str:
    value = _text(node)
    if value == title or not re.search(r"[가-힣]", value):
        return ""
    if len(value) < 35 or value.startswith("DOI 선발급"):
        return ""
    return value


def _item(url: str, title: str, date: str = "", description: str = "", **extra) -> dict:
    return {"url": url, "title": title, "date": date, "description": description, **extra}


def _deduplicate(items: list[dict]) -> list[dict]:
    seen = set()
    out = []
    for item in items:
        if item["url"] and item["title"] and item["url"] not in seen:
            seen.add(item["url"])
            out.append(item)
    return out


def discover(source: dict, text: str) -> list[dict]:
    """Find canonical report URLs and source-dated list metadata."""
    soup = _soup(text)
    adapter = source["adapter"]
    out = []
    if adapter == "lg":
        for row in soup.select(".search_result > ul > li"):
            link = row.select_one("a[href]")
            match = re.fullmatch(r"javascript:fnView\((\d+)\);?", link.get("href", "")) if link else None
            if match:
                url = _url(source, "/report/view.do?idx=" + match[1])
                out.append(_item(url, _text(row.select_one("strong")), _date(_text(row.select_one("dd p")))))
    elif adapter == "kdi_monthly":
        for button in soup.select("button[onclick]"):
            if button.has_attr("disabled"):
                continue
            match = re.search(r"/research/monTrends\?pub_no=(\d+)", button.get("onclick", ""))
            if match:
                # The detail page supplies the publication date; a month button does not.
                out.append(_item(_url(source, "/research/monTrends?pub_no=" + match[1]), "KDI 경제동향 " + _text(button)))
    elif adapter == "kdi_outlook":
        options = soup.select("select#yearSelectUpDown option[value]")
        for option in options[: source.get("max_discover", 12)]:
            identity = option.get("value", "")
            if identity.isdigit():
                label = _text(option)
                out.append(_item(_url(source, "/research/economy?pub_no=" + identity), "KDI 경제전망 " + label, _date(label)))
    elif adapter == "etri":
        for row in soup.select("table.list_tbl tbody tr"):
            link = row.select_one("td.alleft_td a[href]")
            if not link:
                continue
            identity = parse_qs(urlsplit(link.get("href", "")).query).get("id", [""])[0]
            if identity.isdigit():
                out.append(_item(_url(source, "/ksp/plan-report/read?id=" + identity), _text(link)))
    elif adapter == "kisti":
        for row in soup.select("ul.publication_board > li"):
            link = row.select_one("a.title[href]")
            match = re.search(r"/post/analysis-report/(\d+)(?:;|$|\?)", link.get("href", "")) if link else None
            if match:
                out.append(_item(_url(source, "/post/analysis-report/" + match[1]), _text(link), _date(_text(row.select_one(".date"))), kind="분석 보고서"))
    elif adapter == "snu":
        for row in soup.select(".list-line"):
            link = row.select_one("h3.pjt a[href]")
            if not link:
                continue
            raw = link.get("href", "")
            parts = urlsplit(raw)
            identity = parse_qs(parts.query).get("pubidx", [""])[0]
            if identity.isdigit() and parts.path in ("/publication/report", "/publication/issue-brief"):
                url = _url(source, parts.path + "?mode=view&pubidx=" + identity)
                title = _text(link)
                out.append(_item(url, title, _date(_text(row.select_one(".p-date"))), _description(row.select_one(".p-summary"), title)))
    elif adapter == "kaist":
        for row in soup.select("table.bbs-standard tbody tr"):
            link = row.select_one("td.col-tit a[href]")
            if not link:
                continue
            identity = parse_qs(urlsplit(html.unescape(link.get("href", ""))).query).get("ix", [""])[0]
            if identity.isdigit():
                url = _url(source, "/ko/?" + urlencode({"c": "203", "gbn": "view", "ix": identity}))
                out.append(_item(url, _text(link), _date(_text(row.select_one(".col-date")))))
    else:
        raise ValueError("Unknown report adapter: " + str(adapter))
    return _deduplicate(out)


def detail(source: dict, text: str, url: str) -> dict:
    """Read the publisher's own description without inventing report findings."""
    soup = _soup(text)
    adapter = source["adapter"]
    title = description = date = pdf = ""
    if adapter == "lg":
        title = _text(soup.select_one(".inner_pop > .tit strong")) or _meta(soup, "og:title")
        date = _date(_text(soup.select_one(".inner_pop > .tit p")))
        description = _description(soup.select_one(".pop_content .text"), title)
        file_input = soup.select_one("input#popFileNm[value]")
        pdf = _url(source, file_input.get("value", ""), url) if file_input else ""
    elif adapter in ("kdi_monthly", "kdi_outlook"):
        title = (_meta(soup, "og:title") or _meta(soup, "title")).split(" - KDI 한국개발연구원", 1)[0]
        if adapter == "kdi_monthly":
            date = _date(_text(soup.select_one(".tit-info .date")))
            summary = soup.select_one(".bundlebox.desc .editor-template")
        else:
            date = _date(_text(soup.select_one("select#yearSelectUpDown option[selected]")))
            summary = soup.select_one(".economy_conts-template .editor-template")
        description = _description(summary, title)
        for button in soup.select("button[onclick]"):
            match = re.search(r"(/file/download\?atch_no=[^'\"\s]+)", button.get("onclick", ""))
            if match:
                pdf = _url(source, match[1], url)
                break
    elif adapter == "etri":
        title = _meta(soup, "citation_title") or _meta(soup, "dc.title")
        date = _date(_meta(soup, "citation_publication_date") or _meta(soup, "dc.issued"))
        for row in soup.select("dl.row_dl"):
            if _text(row.find("dt")).lower() == "abstract":
                description = _description(row.find("dd"), title)
                break
        pdf = _url(source, _meta(soup, "citation_pdf_url"), url)
    elif adapter == "kisti":
        title = _text(soup.select_one(".board_header h2"))
        date = _date(_text(soup.select_one(".board_header .icon_date")))
        description = _description(soup.select_one(".board_body"), title)
        # Download widgets require JS; the canonical detail remains the original link.
    elif adapter == "snu":
        title = _text(soup.select_one("h2.tit"))
        date = _date(_text(soup.select_one(".info1")))
        description = _description(soup.select_one("div.cont"), title)
        for script in soup.select("script[type='application/ld+json']"):
            try:
                data = json.loads(script.string or "")
            except (TypeError, ValueError):
                continue
            if isinstance(data, dict) and data.get("@type") == "ScholarlyArticle":
                title = str(data.get("headline") or title)
                date = _date(str(data.get("datePublished") or "")) or date
                raw_description = data.get("description")
                if isinstance(raw_description, str):
                    description = _description(_soup(raw_description), title) or description
                break
        for link in soup.select("a[href]"):
            raw = link.get("href", "")
            if urlsplit(raw).path.startswith("/clusterfile/") and urlsplit(raw).path.lower().endswith(".pdf"):
                pdf = _url(source, raw, url)
                break
    elif adapter == "kaist":
        title = _meta(soup, "title") or _meta(soup, "og:title")
        date = _date(_text(soup.select_one(".bbs-view-details")))
        description = _description(soup.select_one("#bbsContents"), title)
    else:
        raise ValueError("Unknown report adapter: " + str(adapter))
    return _item(_url(source, url), title, date, description, pdf_url=pdf)
