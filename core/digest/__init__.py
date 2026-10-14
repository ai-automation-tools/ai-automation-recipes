"""Shared pieces for the research-digest recipes (link lists, toolkits, repo digests).

Not a recipe: it has no run.py or cronsole.json. The nine digest recipes import it
for the parts that should behave identically across them:

* parse_digest()   — read a digest's markdown back into categories of entries.
                     Four on-disk shapes: the `### [Name](url)` link list, the
                     ranked `## N. Name` + `- **Repo:**` shape, the movers
                     `### N. [owner/repo](url)` shape, and the spotlight
                     `- **[Name](url)** (owner) — … — Significance:` bullets.
* featured()       — what earlier runs already listed, for the do-not-repeat check.
* fetch_candidates() — RSS/Atom feeds and github.com/trending pages → a ranked
                     candidate list. Star velocity can't be found by searching, so
                     it is measured here and the agent only ranks and writes.
* export_bookmarks() — browser-importable Netscape bookmark files (this run's and
                     the cumulative archive), plus an OPML feed bundle on request.
* digest_recipe()  — a Recipe with the shared defaults filled in.

ponytail: lives under recipes/ because core/ was out of scope when it was written;
move it to core/ once a second family of recipes needs any of it.
"""

from __future__ import annotations

import html
import json
import re
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
import xml.sax.saxutils as sax
from collections import OrderedDict
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent

from ..runner import Recipe, RecipeError, RunContext
from ..artifacts import MANIFEST

MAIN = "digest.md"
RULES = (HERE / "rules.md").read_text(encoding="utf-8")
UA = "Mozilla/5.0 (compatible; ai-automation-recipes/0.1; +https://github.com/ai-automation-tools/ai-automation-recipes)"
TIMEOUT = 30

Entry = dict  # {"name", "url", "desc", "cat"?}

# --- parsing -----------------------------------------------------------------

_CATEGORY_RE = re.compile(r"^##\s+(.*\S)\s*$")
_SITE_RE = re.compile(r"^###\s+\[(.+?)\]\(\s*(\S+?)\s*\)\s*$")
_RANKED_HEAD_RE = re.compile(r"^#{2,3}\s+\d+\.\s+(?:\[(.+?)\]\(\s*(\S+?)\s*\)|(.+\S))\s*$")
_BULLET_RE = re.compile(r"^\s*-\s+\*\*(Repo|Category)[:：]?\*\*\s*(.+\S)\s*$", re.I)
_SPOT_RE = re.compile(r"^\s*-\s+\*\*\[(.+?)\]\(\s*(\S+?)\s*\)\*\*\s*(?:\(([^)]*)\))?\s*[—-]?\s*(.*)$")
_LEADING_SYMBOLS_RE = re.compile(r"^[\s←-⇿⌀-➿⬀-⯿\U0001F000-\U0001FAFF️‍]+")
_SKIP_SECTIONS = {"overview", "sources", "honorable mentions", "also climbing"}


def _clean(label: str) -> str:
    return _LEADING_SYMBOLS_RE.sub("", label).strip()


def split_frontmatter(text: str) -> tuple[dict[str, str], str]:
    fm: dict[str, str] = {}
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            for line in text[3:end].splitlines():
                if ":" in line and not line.lstrip().startswith("#"):
                    k, _, v = line.partition(":")
                    fm[k.strip()] = v.strip().strip('"').strip("'")
            return fm, text[end + 4:]
    return fm, text


def _link_list(body: str) -> OrderedDict:
    cats: OrderedDict = OrderedDict()
    cat, cur = None, None
    for line in body.splitlines():
        if (m := _CATEGORY_RE.match(line)):
            cat, cur = _clean(m.group(1)), None
            continue
        if (m := _SITE_RE.match(line)):
            cur = {"name": m.group(1).strip(), "url": m.group(2).strip(), "desc": ""}
            if cat:
                cats.setdefault(cat, []).append(cur)
            continue
        if line.startswith("#"):
            cur = None
        elif cur is not None and line.strip():
            cur["desc"] = f"{cur['desc']} {line.strip()}".strip()
    return OrderedDict((c, e) for c, e in cats.items() if e)


def _ranked(body: str) -> OrderedDict:
    """`## 3. Name` + `- **Repo:** url` (top-10), or `### 3. [owner/repo](url)` (movers)."""
    cats: OrderedDict = OrderedDict()
    cur = None

    def close():
        if cur and cur.get("url"):
            cats.setdefault(cur.pop("cat") or "Repos", []).append(cur)

    for line in body.splitlines():
        if (m := _RANKED_HEAD_RE.match(line)):
            close()
            cur = {"name": (m.group(1) or m.group(3)).strip(), "url": (m.group(2) or "").strip(), "desc": "", "cat": None}
            continue
        if line.startswith("#"):
            close()
            cur = None
            continue
        if cur is None:
            continue
        if (b := _BULLET_RE.match(line)):
            key, val = b.group(1).lower(), b.group(2).strip()
            if key == "repo" and not cur["url"]:
                cur["url"] = val.strip("<>").split()[0]
            elif key == "category":
                cur["cat"] = _clean(val)
        elif line.strip() and not line.lstrip().startswith("-"):
            text = re.sub(r"^\*\*[^*]+:\*\*\s*", "", line.strip())
            cur["desc"] = f"{cur['desc']} {text}".strip()
    close()
    return cats


def _spotlight(body: str) -> OrderedDict:
    cats: OrderedDict = OrderedDict()
    cat = None
    for line in body.splitlines():
        if (m := _CATEGORY_RE.match(line)):
            cat = _clean(m.group(1))
            continue
        if cat and cat.lower() not in _SKIP_SECTIONS and (m := _SPOT_RE.match(line)):
            name, url, _owner, rest = m.groups()
            desc = re.sub(r"[—-]?\s*Significance:\s*\w+\s*$", "", rest).strip(" —-\t")
            cats.setdefault(cat, []).append({"name": name.strip(), "url": url.strip(), "desc": desc})
    return cats


def parse_digest(text: str) -> tuple[dict[str, str], OrderedDict]:
    """(frontmatter, categories). Tries each on-disk shape until one yields entries."""
    fm, body = split_frontmatter(text)
    for parser in (_link_list, _ranked, _spotlight):
        cats = parser(body)
        if cats:
            return fm, cats
    return fm, OrderedDict()


def domain(url: str) -> str:
    net = urllib.parse.urlparse(url).netloc.lower()
    return net[4:] if net.startswith("www.") else net


def dedupe_key(url: str) -> str:
    """A domain for link streams; owner/repo on a code host, where every entry shares the domain."""
    dom = domain(url)
    if dom in ("github.com", "gitlab.com", "codeberg.org", "bitbucket.org", "huggingface.co"):
        m = re.search(r"^https?://[^/]+/([^/?#]+/[^/?#]+)", url, re.I)
        if m:
            return f"{dom}/{m.group(1).rstrip('/').removesuffix('.git').lower()}"
    return dom


# --- history -----------------------------------------------------------------

def past_digests(collection_dir: Path) -> list[tuple[str, OrderedDict]]:
    """(date, categories) for every published run, oldest first."""
    out = []
    for path in sorted(collection_dir.glob(f"*/*/{MAIN}")):
        fm, cats = parse_digest(path.read_text(encoding="utf-8"))
        out.append((fm.get("date") or path.parent.name[:10], cats))
    out.sort(key=lambda d: d[0])
    return out


def featured(collection_dir: Path, limit: int = 400) -> str:
    """Everything earlier runs listed, newest last: `- date · name — url`."""
    rows = [f"- {d} · {e['name']} — {e['url']}"
            for d, cats in past_digests(collection_dir) for es in cats.values() for e in es]
    return "\n".join(rows[-limit:]) if rows else "(nothing yet — this is the first run)"


def archive_size(collection_dir: Path) -> int:
    return len({dedupe_key(e["url"]) for _, cats in past_digests(collection_dir)
                for es in cats.values() for e in es})


# --- candidate feeds (ported from the original fetch_feeds.py) ---------------

_NS_RE = re.compile(r"\{[^}]*\}")
_TAG_RE = re.compile(r"<[^>]+>")
_TOKEN_RE = re.compile(r"[a-z0-9+#.]+")
_STARS_WEEK_RE = re.compile(r"([\d,]+)\s+stars?\s+this\s+week", re.I)
_STARS_TOTAL_RE = re.compile(r"([\d,]+)\s+stars?\b(?!\s+this)", re.I)
_TR_ROW_RE = re.compile(r"<article\b.*?</article>", re.S)
_TR_REPO_RE = re.compile(r'<h2[^>]*>\s*<a[^>]*href="/([^"]+)"', re.S)
_TR_DESC_RE = re.compile(r'<p class="col-9[^"]*"[^>]*>\s*(.*?)\s*</p>', re.S)
_TR_LANG_RE = re.compile(r'itemprop="programmingLanguage">([^<]+)<')
_TR_TOTAL_RE = re.compile(r'href="/[^"]+/stargazers"[^>]*>\s*(?:<svg.*?</svg>)?\s*([\d,]+)', re.S)


def _text(raw: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(_TAG_RE.sub(" ", raw or ""))).strip()


def _int(m: re.Match | None) -> int | None:
    digits = m.group(1).replace(",", "") if m else ""  # "[\d,]+" can match a lone comma
    return int(digits) if digits else None


def keyword_match(text: str, keywords: list[str]) -> bool:
    """Token-aware: 'ai' must match the word, never the inside of 'email'."""
    if not keywords:
        return True
    low = text.lower()
    toks = set(_TOKEN_RE.findall(low))
    return any((k in low) if (" " in k or "-" in k) else (k in toks)
               for k in (kw.lower().strip() for kw in keywords) if k)


def parse_feed(data: bytes, source: str) -> list[dict]:
    items = []
    for el in ET.fromstring(data).iter():
        if _NS_RE.sub("", el.tag) not in ("item", "entry"):
            continue
        fields: dict[str, str] = {}
        link = ""
        for child in el:
            tag = _NS_RE.sub("", child.tag)
            if tag == "link":
                link = link or (child.get("href") or (child.text or "")).strip()
            elif tag in ("title", "description", "summary", "content", "pubDate", "updated", "published"):
                fields[tag] = (child.text or "") + "".join(ET.tostring(g, encoding="unicode") for g in child)
        if not link:
            continue
        title = _text(fields.get("title", ""))
        desc = _text(fields.get("description") or fields.get("summary") or fields.get("content", ""))
        items.append({
            "title": title, "url": link, "source": source, "description": desc,
            "published": (fields.get("pubDate") or fields.get("updated") or fields.get("published") or "").strip(),
            "starsThisWeek": _int(_STARS_WEEK_RE.search(f"{title} {desc}")),
            "stars": _int(_STARS_TOTAL_RE.search(f"{title} {desc}")),
        })
    return items


def parse_trending(data: bytes, source: str) -> list[dict]:
    """github.com/trending — the only source that still prints 'N stars this week'."""
    items = []
    for blk in _TR_ROW_RE.findall(data.decode("utf-8", "replace")):
        repo = _TR_REPO_RE.search(blk)
        if not repo:
            continue
        slug = repo.group(1).strip().strip("/")
        desc, lang = _TR_DESC_RE.search(blk), _TR_LANG_RE.search(blk)
        items.append({
            "title": slug, "url": f"https://github.com/{slug}", "source": source,
            "description": _text(desc.group(1)) if desc else "",
            "language": lang.group(1).strip() if lang else None,
            "starsThisWeek": _int(_STARS_WEEK_RE.search(blk)),
            "stars": _int(_TR_TOTAL_RE.search(blk)),
        })
    return items


def _fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/xml, text/xml, */*"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return resp.read()


def fetch_candidates(cfg: dict) -> dict:
    """Fetch every source, dedupe, keyword-filter, sort, cap. One dead source never kills the run.

    cfg: feeds, trending, keywords, match_chars (400), sort ("stars"|"none"), limit (40).
    Returns {"candidates", "feeds_ok", "feeds_failed"}; candidates is empty if everything failed.
    """
    sources = [(u, parse_feed) for u in cfg.get("feeds", [])] + [(u, parse_trending) for u in cfg.get("trending", [])]
    raw, ok, failed = [], [], []
    for url, parser in sources:
        try:
            got = parser(_fetch(url), url)
            if not got:  # empty page = markup moved, not an empty week
                raise ValueError("parsed to zero items")
            raw.extend(got)
            ok.append(url)
        except (urllib.error.URLError, ET.ParseError, OSError, ValueError) as exc:
            failed.append(f"{url}: {type(exc).__name__}: {exc}")

    seen, kept = set(), []
    for item in raw:
        key = re.split(r"[#?]", item["url"].strip(), maxsplit=1)[0].rstrip("/").lower()
        if key in seen or not keyword_match(
                f"{item['title']} {item['description'][:cfg.get('match_chars', 400)]}", cfg.get("keywords", [])):
            continue
        seen.add(key)
        kept.append(item)
    if cfg.get("sort") == "stars":
        kept.sort(key=lambda i: (i["starsThisWeek"] or 0, i["stars"] or 0), reverse=True)
    return {"candidates": kept[: cfg.get("limit", 40)], "feeds_ok": ok, "feeds_failed": failed}


def candidates_block(payload: dict, desc_chars: int = 280) -> str:
    """The candidate list as compact JSON for the prompt, with a fetch report on top."""
    if not payload["candidates"]:
        why = "; ".join(payload["feeds_failed"]) or "no candidates survived the filter"
        return f"**The candidate fetch failed this run** ({why}). There is no candidate list."
    rows = [{k: (v[:desc_chars] if k == "description" and isinstance(v, str) else v)
             for k, v in c.items() if v not in (None, "")} for c in payload["candidates"]]
    report = (f"Sources OK: {len(payload['feeds_ok'])}. Failed: "
              + ("; ".join(payload["feeds_failed"]) if payload["feeds_failed"] else "none") + ".")
    return f"{report}\n\n```json\n{json.dumps(rows, indent=1, ensure_ascii=False)}\n```"


# --- bookmark + OPML export ---------------------------------------------------

def _epoch(date_str: str) -> int:
    try:
        return int(datetime.strptime(date_str.strip(), "%Y-%m-%d").replace(tzinfo=timezone.utc).timestamp())
    except ValueError:
        return 0


def render_bookmarks(title: str, cats: OrderedDict, epoch: int) -> str:
    esc = html.escape
    out = ["<!DOCTYPE NETSCAPE-Bookmark-file-1>",
           "<!-- This is an automatically generated file. DO NOT EDIT! -->",
           '<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">',
           "<TITLE>Bookmarks</TITLE>", "<H1>Bookmarks</H1>", "<DL><p>",
           f'    <DT><H3 ADD_DATE="{epoch}" LAST_MODIFIED="{epoch}">{esc(title)}</H3>', "    <DL><p>"]
    for cat, entries in cats.items():
        out += [f'        <DT><H3 ADD_DATE="{epoch}">{esc(cat)}</H3>', "        <DL><p>"]
        for e in entries:
            out.append(f'            <DT><A HREF="{esc(e["url"], quote=True)}" ADD_DATE="{epoch}">{esc(e["name"])}</A>')
            if e.get("desc"):
                out.append(f"            <DD>{esc(e['desc'])}")
        out.append("        </DL><p>")
    out += ["    </DL><p>", "</DL><p>"]
    return "\n".join(out) + "\n"


def _merge(digests: list[tuple[str, OrderedDict]]) -> OrderedDict:
    """All runs in one tree, first occurrence wins (keeps its category)."""
    merged: OrderedDict = OrderedDict()
    seen: set[str] = set()
    for _, cats in digests:
        for cat, entries in cats.items():
            for e in entries:
                if (k := dedupe_key(e["url"])) not in seen:
                    seen.add(k)
                    merged.setdefault(cat, []).append(e)
    return merged


_FEED_RE = re.compile(r"\*{0,2}Feed\*{0,2}\s*:\s*\*{0,2}\s*(\S+)", re.I)
_CADENCE_RE = re.compile(r"\*{0,2}Cadence\*{0,2}\s*:\s*\*{0,2}\s*([^.*]+?)\s*(?:[.]|$|\*\*)", re.I)


def render_opml(title: str, digests: list[tuple[str, OrderedDict]]) -> tuple[str, int]:
    """Cumulative OPML from each entry's `**Feed:** <url>` clause; entries with no feed are skipped."""
    q = sax.quoteattr
    cats: OrderedDict = OrderedDict()
    seen: set[str] = set()
    for _, dcats in digests:
        for cat, entries in dcats.items():
            for e in entries:
                m = _FEED_RE.search(e.get("desc", ""))
                raw = m.group(1) if m else ""
                link = re.match(r"^\[.*?\]\((\S+?)\)", raw)
                feed = (link.group(1) if link else raw).lstrip("<`([\"'*").rstrip(">`)]\"'*.,;:")
                if not re.match(r"^https?://", feed, re.I) or feed.rstrip("/").lower() in seen:
                    continue
                seen.add(feed.rstrip("/").lower())
                cadence = _CADENCE_RE.search(e.get("desc", ""))
                prose = re.sub(r"\*{0,2}(?:Cadence|Feed)\*{0,2}\s*:.*", "", e.get("desc", ""), flags=re.I | re.S).strip()
                desc = f"{prose} ({cadence.group(1).strip()})" if cadence else prose
                cats.setdefault(cat, []).append(
                    f'      <outline type="rss" text={q(e["name"])} title={q(e["name"])} '
                    f'xmlUrl={q(feed)} htmlUrl={q(e["url"])}' + (f" description={q(desc)}" if desc else "") + "/>")
    epoch = max((_epoch(d) for d, _ in digests), default=0)
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<opml version="2.0">', "  <head>",
             f"    <title>{sax.escape(title)}</title>"]
    if epoch:
        lines.append(f"    <dateCreated>{datetime.fromtimestamp(epoch, timezone.utc):%a, %d %b %Y %H:%M:%S +0000}</dateCreated>")
    lines += ["  </head>", "  <body>"]
    for cat, rows in cats.items():
        lines += [f"    <outline text={q(cat)} title={q(cat)}>", *rows, "    </outline>"]
    lines += ["  </body>", "</opml>", ""]
    return "\n".join(lines), sum(len(r) for r in cats.values())


def export_bookmarks(ctx: RunContext, final: Path, archive_title: str, opml_title: str | None = None) -> None:
    """Write this run's bookmarks.html, regenerate the cumulative files at the collection root,
    and record them in artifact.json."""
    fm, cats = parse_digest((final / MAIN).read_text(encoding="utf-8"))
    (final / "bookmarks.html").write_text(
        render_bookmarks(fm.get("title") or final.name, cats, _epoch(fm.get("date", ""))), encoding="utf-8", newline="\n")

    digests = past_digests(ctx.collection_dir)
    epoch = max((_epoch(d) for d, _ in digests), default=0)
    (ctx.collection_dir / "all-bookmarks.html").write_text(
        render_bookmarks(archive_title, _merge(digests), epoch), encoding="utf-8", newline="\n")
    if opml_title:
        text, _count = render_opml(opml_title, digests)
        (ctx.collection_dir / "feeds.opml").write_text(text, encoding="utf-8", newline="\n")

    manifest_path = final / MANIFEST
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    data["files"]["bookmarks"] = "bookmarks.html"
    manifest_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


# --- the recipe ----------------------------------------------------------------

def require_entries(staging: Path, minimum: int = 1) -> OrderedDict:
    """Reject a digest the bookmark export can't parse — its shape is the contract."""
    _, cats = parse_digest((staging / MAIN).read_text(encoding="utf-8"))
    count = sum(len(e) for e in cats.values())
    if count < minimum:
        raise RecipeError(f"{MAIN} parsed to {count} entries (need {minimum}); the entry shape was not followed")
    return cats


def digest_recipe(*, name: str, collection: str, archive_title: str, prepare_extra=None,
                  validate_extra=None, opml_title: str | None = None, cover: bool = True,
                  fields: tuple[str, ...] = ("site_count",), timeout_s: int = 2400) -> Recipe:
    """A digest Recipe: shared rules, the do-not-repeat list, bookmark export after publish."""
    def prepare(ctx: RunContext) -> dict[str, str]:
        tokens = {"DIGEST_RULES": RULES, "FEATURED": featured(ctx.collection_dir)}
        if prepare_extra:
            tokens.update(prepare_extra(ctx))
        return tokens

    def validate(staging: Path, manifest: dict[str, object]) -> None:
        cats = require_entries(staging)
        if validate_extra:
            validate_extra(staging, manifest, cats)

    def finish(ctx: RunContext, final: Path, manifest: dict[str, object]) -> None:
        export_bookmarks(ctx, final, archive_title, opml_title)

    return Recipe(
        name=name,
        collection=collection,
        version="0.1.0",
        prompt_path=HERE.parents[1] / "recipes" / name / "prompt.md",
        files=(MAIN,),
        skills=("llm-writing", "humanizer", "image-prompt-craft") if cover else ("llm-writing", "humanizer"),
        tools=("Read", "Write", "Edit", "Glob", "Grep", "Skill", "WebSearch", "WebFetch"),
        fields=fields,
        cover_aspect="16:9" if cover else None,
        default_model="sonnet",
        timeout_s=timeout_s,
        prepare=prepare,
        validate=validate,
        finish=finish,
    )


def _self_check() -> None:
    link = "---\ntitle: T\ndate: 2026-10-01\n---\n## 🔐 Sec\n### [A](https://a.com)\nDoes a. **Pricing:** free.\n"
    fm, cats = parse_digest(link)
    assert fm["date"] == "2026-10-01" and cats["Sec"][0]["url"] == "https://a.com", cats
    ranked = "## 1. Foo\n- **Repo:** https://github.com/o/foo\n- **Category:** CLI\n\nDoes foo.\n"
    assert parse_digest(ranked)[1]["CLI"][0]["url"] == "https://github.com/o/foo"
    movers = "## The Leaderboard\n### 1. [o/bar](https://github.com/o/bar)\n- **Stars this week:** +1,200\n- **Category:** Web\n"
    assert parse_digest(movers)[1]["Web"][0]["name"] == "o/bar"
    spot = "## Hidden Gems\n- **[Baz](https://baz.dev)** (baz) — Small and good. — Significance: Low\n"
    assert parse_digest(spot)[1]["Hidden Gems"][0]["desc"] == "Small and good."
    assert keyword_match("An AI agent", ["ai"]) and not keyword_match("Send email", ["ai"])
    assert dedupe_key("https://github.com/O/Repo/") == dedupe_key("https://github.com/o/repo")
    feed = "---\ndate: 2026-10-01\n---\n## Blogs\n### [X](https://x.dev)\nGood. **Cadence:** weekly. **Feed:** https://x.dev/rss.xml\n"
    text, n = render_opml("S", [("2026-10-01", parse_digest(feed)[1])])
    assert n == 1 and 'xmlUrl="https://x.dev/rss.xml"' in text, text
    page = (b'<article class="Box-row"><h2 class="h3"><a href="/o/r">o / r</a></h2>'
            b'<p class="col-9 x">A db.</p><a href="/o/r/stargazers"><svg></svg> 29,144</a>'
            b"<span>2,285 stars this week</span></article>")
    tr = parse_trending(page, "t")[0]
    assert tr["starsThisWeek"] == 2285 and tr["stars"] == 29144, tr
    print("digest self-check OK")


if __name__ == "__main__":
    _self_check()
