#!/usr/bin/env python3
"""sahinkaradas.com blog oluşturucu (yalnızca standart Python; Netlify her yayında bunu çalıştırır).

Kaynaklar (bu dosyanın yanındaki klasörde):
  shell.json          üst menü, alt bilgi, favicon, WhatsApp bağlantısı (ana site derlemesinden gelir)
  posts/<adres>.json  her yazı bir dosya (yönetim panelinin yazdığı biçim):
                      title, date (YYYY-AA-GG), category, seo_title, description, lead, keywords, body (Markdown)
                      Dosya adı yazının adresidir: posts/instagram-reklam-ucretleri.json -> /blog/instagram-reklam-ucretleri/
                      Gövdede ana sayfaya bağlantı: (@@HOME@@#hesap), blog listesine: (@@BLOG@@)

Kullanım:
  python3 blog_build.py --site <site_klasörü> [--art <önizleme_klasörü>]
    <site_klasörü>   Yayınlanacak klasör. İçinde index.html ve assets/site.css zaten olmalı.
                     Yazar: blog/index.html, blog/<adres>/index.html, sitemap.xml, robots.txt
    <önizleme_klasörü> claude.ai önizlemesi için aynı sayfalar, göreli bağlantılarla (blog/...).
  python3 blog_build.py --check    sadece kontrol (eksik alan, yapay dil uyarıları)
"""
import argparse, datetime as dt, html, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
AYLAR = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
REQ = ["slug", "title", "description", "lead", "date", "category", "body"]
# yapay zekâ kokan kalıplar: bulunursa uyarı verir (yazıyı durdurmaz)
KALIP = ["günümüzde", "dijital dünya", "hayati önem", "kritik öneme", "sonuç olarak", "unutmayın ki", "oyunun kurallarını",
         "kapsamlı rehber", "kapsamlı bir rehber", "bu yazıda", "peki ya", "işte tam bu noktada", "bir adım öne", "fark yaratın",
         "potansiyelinizi", "en iyi şekilde", "son derece", "muazzam", "devrim niteliğinde", "her şeyden önce", "—"]

JS = """<script>
(function () {
  var root = document.documentElement;
  function get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function put(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  var theme = get('sk-theme');
  var mq = window.matchMedia ? window.matchMedia('(prefers-color-scheme: dark)') : null;
  function eff() { var t = root.getAttribute('data-theme'); if (t === 'dark' || t === 'light') return t; return 'light'; }
  function apply() {
    if (theme === 'dark' || theme === 'light') root.setAttribute('data-theme', theme);
    root.setAttribute('data-eff', eff());
    document.querySelectorAll('[data-act="theme"]').forEach(function (b) { b.setAttribute('aria-pressed', eff() === 'dark' ? 'true' : 'false'); });
  }
  if (mq && mq.addEventListener) mq.addEventListener('change', apply);
  document.addEventListener('click', function (e) {
    var b = e.target.closest && e.target.closest('[data-act="theme"]');
    if (b) { theme = eff() === 'dark' ? 'light' : 'dark'; put('sk-theme', theme); apply(); }
  });
  var y = String(new Date().getFullYear());
  document.querySelectorAll('[data-year]').forEach(function (el) { el.textContent = y; });
  var btn = document.getElementById('menu-btn'), panel = document.getElementById('mnav');
  function setMenu(open) { if (!btn || !panel) return; btn.setAttribute('aria-expanded', open ? 'true' : 'false'); panel.hidden = !open; }
  if (btn) btn.addEventListener('click', function () { setMenu(btn.getAttribute('aria-expanded') !== 'true'); });
  if (panel) panel.addEventListener('click', function (e) { if (e.target.closest('a')) setMenu(false); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && btn && btn.getAttribute('aria-expanded') === 'true') { setMenu(false); btn.focus(); } });
  document.addEventListener('click', function (e) { if (panel && !panel.hidden && !e.target.closest('.hdr')) setMenu(false); });
  window.addEventListener('resize', function () { if (window.innerWidth > 1100) setMenu(false); });
  apply();
})();
</script>"""


def e(s):
    return html.escape(s, quote=True)


def tarih(iso):
    d = dt.date.fromisoformat(iso)
    return f"{d.day} {AYLAR[d.month - 1]} {d.year}"


def dakika(body):
    words = len(re.sub(r"<[^>]+>", " ", body).split())
    return max(2, round(words / 200))


# ---------- küçük Markdown çevirici (yönetim panelinin yazdığı metin için) ----------
_ESC = re.compile(r"\\([\\`*_{}\[\]()#+\-.!<>|~\"'=:])")
_INLINE_TAG = re.compile(r"</?(strong|em|b|i|a|br|small|code|span|mark|s|u)(\s[^<>]*)?/?>", re.I)
_BLOCK_HTML = re.compile(r"^\s*<(div|p|ul|ol|aside|figure|table|blockquote|h[2-6]|section|details|hr|img|iframe)\b", re.I)


def inline(t):
    keep = []

    def hold(x):
        keep.append(x)
        return f"\x00{len(keep) - 1}\x00"

    t = _ESC.sub(lambda m: hold(html.escape(m.group(1))), t)
    t = re.sub(r"`([^`]+)`", lambda m: hold("<code>" + html.escape(m.group(1)) + "</code>"), t)
    t = _INLINE_TAG.sub(lambda m: hold(m.group(0)), t)
    t = re.sub(r"&(?!#?\w+;)", "&amp;", t).replace("<", "&lt;").replace(">", "&gt;")
    t = re.sub(r"!\[([^\]]*)\]\(([^)\s]+)\)", lambda m: hold(f'<img src="{html.escape(m.group(2))}" alt="{html.escape(m.group(1))}" loading="lazy">'), t)

    def link(m):
        url = m.group(2)
        ext = url.startswith("http") and "sahinkaradas.com" not in url
        return f'<a href="{html.escape(url)}"' + (' target="_blank" rel="noopener"' if ext else "") + f">{m.group(1)}</a>"
    t = re.sub(r"\[([^\]]+)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)", link, t)
    t = re.sub(r"\*\*(?=\S)(.+?)(?<=\S)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![\w])__(?=\S)(.+?)(?<=\S)__(?![\w])", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![*\w])\*(?=\S)(.+?)(?<=\S)\*(?![*\w])", r"<em>\1</em>", t)
    t = re.sub(r"(?<![_\w])_(?=\S)(.+?)(?<=\S)_(?![_\w])", r"<em>\1</em>", t)
    t = re.sub(r"( {2,}|\\)\n", "<br>\n", t)
    for _ in range(3):
        t = re.sub(r"\x00(\d+)\x00", lambda m: keep[int(m.group(1))], t)
    return t.strip()


def _li_re(line):
    return re.match(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$", line)


def md(src):
    lines = src.replace("\r\n", "\n").replace("\t", "    ").split("\n")
    out, para, i = [], [], 0

    def flush():
        if para:
            out.append("<p>" + inline("\n".join(para)) + "</p>")
            para.clear()

    while i < len(lines):
        ln = lines[i]
        s = ln.strip()
        if not s:
            flush(); i += 1; continue
        if s.startswith("```"):
            flush(); j = i + 1; code = []
            while j < len(lines) and not lines[j].strip().startswith("```"):
                code.append(lines[j]); j += 1
            out.append("<pre><code>" + html.escape("\n".join(code)) + "</code></pre>"); i = j + 1; continue
        if _BLOCK_HTML.match(ln) and not para:
            blk = []
            if re.match(r"^\s*<div\b", ln, re.I):
                depth = 0
                while i < len(lines):
                    blk.append(lines[i])
                    depth += len(re.findall(r"<div\b", lines[i], re.I)) - len(re.findall(r"</div>", lines[i], re.I))
                    i += 1
                    if depth <= 0:
                        break
            else:
                while i < len(lines) and lines[i].strip():
                    blk.append(lines[i]); i += 1
            out.append("\n".join(blk)); continue
        m = re.match(r"^(#{1,6})\s+(.*?)\s*#*\s*$", s)
        if m:
            flush(); lvl = max(2, min(4, len(m.group(1)) if len(m.group(1)) > 1 else 2))
            out.append(f"<h{lvl}>{inline(m.group(2))}</h{lvl}>"); i += 1; continue
        if re.match(r"^(\*\s*){3,}$|^(-\s*){3,}$|^(_\s*){3,}$", s):
            flush(); out.append("<hr>"); i += 1; continue
        if s.startswith(">"):
            flush(); q = []
            while i < len(lines) and lines[i].strip() and (lines[i].strip().startswith(">") or q):
                q.append(re.sub(r"^\s*>\s?", "", lines[i])); i += 1
            out.append('<div class="note">' + md("\n".join(q)) + "</div>"); continue
        if _li_re(ln) and (not para or not _li_re(ln).group(2)[0].isdigit() or _li_re(ln).group(2)[0] == "1"):
            flush()
            html_list, i = _list(lines, i)
            out.append(html_list); continue
        para.append(ln.lstrip()); i += 1
    flush()
    return "\n".join(out)


def _list(lines, i):
    first = _li_re(lines[i])
    base = len(first.group(1))
    ordered = first.group(2)[0].isdigit()
    items, cur = [], None
    while i < len(lines):
        ln = lines[i]
        m = _li_re(ln)
        if m and len(m.group(1)) <= base + 1 and m.group(2)[0].isdigit() == ordered:
            cur = [m.group(3)]; items.append(cur); i += 1; continue
        if not ln.strip():
            nxt = next((l for l in lines[i + 1:] if l.strip()), "")
            nm = _li_re(nxt)
            if nm and len(nm.group(1)) <= base + 1 and nm.group(2)[0].isdigit() == ordered:
                i += 1; continue
            if nxt.startswith(" " * (base + 2)) and cur is not None:
                cur.append(""); i += 1; continue
            break
        if ln.startswith(" " * (base + 2)) or (cur is not None and not m and not ln.lstrip().startswith(("#", ">")) and not _BLOCK_HTML.match(ln)):
            cur.append(ln[base + 2:] if ln.startswith(" " * (base + 2)) else ln.strip()); i += 1; continue
        break
    tag = "ol" if ordered else "ul"
    parts = []
    for it in items:
        body = "\n".join(it).strip("\n")
        sub = md(body)
        if sub.startswith("<p>") and sub.count("<p>") == 1 and sub.endswith("</p>"):
            sub = sub[3:-4]
        elif sub.startswith("<p>") and "\n" in sub:
            first_p, rest = sub.split("\n", 1)
            if first_p.endswith("</p>"):
                sub = first_p[3:-4] + "\n" + rest
        parts.append(f"<li>{sub}</li>")
    return f"<{tag}>" + "".join(parts) + f"</{tag}>", i


def load():
    shell = json.load(open(os.path.join(HERE, "shell.json"), encoding="utf-8"))
    posts = []
    folder = os.path.join(HERE, "posts")
    for f in sorted(os.listdir(folder)):
        if not f.endswith(".json"):
            continue
        p = json.load(open(os.path.join(folder, f), encoding="utf-8"))
        p["slug"] = f[:-5]
        for k in ("title", "seo_title", "description", "lead", "category", "body"):
            p[k] = (p.get(k) or "").strip() if isinstance(p.get(k), str) else p.get(k)
        p["seo_title"] = p.get("seo_title") or p.get("title")
        p["date"] = str(p.get("date") or "")[:10]
        if isinstance(p.get("keywords"), str):
            p["keywords"] = [k.strip() for k in p["keywords"].split(",") if k.strip()]
        miss = [k for k in REQ if not p.get(k)]
        if miss:
            sys.exit(f"{f}: eksik alan {miss}")
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", p["slug"]):
            sys.exit(f"{f}: dosya adı (adres) yalnızca küçük harf, rakam ve tire olmalı")
        dt.date.fromisoformat(p["date"])
        p["md"] = p["body"]
        p["body"] = md(p["body"])
        p["min"] = dakika(p["body"])
        if p.get("draft"):
            continue
        posts.append(p)
    posts.sort(key=lambda p: (p["date"], p["slug"]), reverse=True)
    return shell, posts


def check(posts):
    warn = 0
    for p in posts:
        txt = (p["title"] + " " + p["lead"] + " " + p["description"] + " " + re.sub(r"<[^>]+>", " ", p["body"])).lower()
        for k in KALIP:
            if k in txt:
                print(f"UYARI {p['slug']}: '{k}' geçiyor, doğal bir ifadeyle değiştirin")
                warn += 1
        if not 110 <= len(p["description"]) <= 165:
            print(f"UYARI {p['slug']}: açıklama {len(p['description'])} karakter (110-165 iyi)")
            warn += 1
        if len(p["seo_title"]) > 62:
            print(f"UYARI {p['slug']}: seo_title {len(p['seo_title'])} karakter (62'yi geçmesin)")
            warn += 1
        if re.search(r"^# ", p["md"], re.M):
            print(f"UYARI {p['slug']}: gövdede tek # başlık var; ## kullanın (sayfa başlığı şablondan gelir)")
            warn += 1
    print(f"{len(posts)} yazı, {warn} uyarı")
    return warn


class Paths:
    """site: temiz adresler (/blog/slug/). art: claude.ai önizlemesi için göreli dosya yolları."""

    def __init__(self, kind, depth):
        self.kind, self.depth = kind, depth

    def up(self):
        return "../" * self.depth

    def home(self):
        return "/" if self.kind == "site" else self.up() + "index.html"

    def blog(self):
        return "/blog/" if self.kind == "site" else self.up() + "blog/index.html"

    def post(self, slug):
        return f"/blog/{slug}/" if self.kind == "site" else self.up() + f"blog/{slug}/index.html"

    def asset(self, name):
        return "/" + name if self.kind == "site" else self.up() + name


def head(shell, P, title, desc, url, extra, ld):
    icon = P.asset("apple-touch-icon.png")
    return f"""<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:locale" content="tr_TR">
<meta property="og:site_name" content="Şahin Karadaş">
<meta property="og:url" content="{url}">
<meta property="og:description" content="{e(desc)}">
{extra}
<meta name="twitter:card" content="summary">
<meta name="theme-color" content="#151412">
{shell['favicon']}
<link rel="apple-touch-icon" href="{icon}">
<link rel="stylesheet" href="{P.asset(shell['css'])}">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
"""


def top(shell, P, current):
    h = shell["header"].replace("@@HOME@@", P.home()).replace("@@BLOG@@", P.blog())
    return h.replace("@@CUR@@", 'aria-current="page"' if current else 'aria-current="true"')


def cta(shell, P, p):
    t = p.get("cta_title") or "Mesajlarınıza birlikte bakalım"
    x = p.get("cta_text") or ("WhatsApp'tan yazın, son gelen mesajlarınıza birlikte bakalım: hangileri cevapsız kalmış, "
                              "hangileri randevuya ya da satışa dönebilirdi. 10 dakika sürer. İşinize uymuyorsa açıkça söylerim.")
    return f"""<aside class="post-cta" aria-labelledby="cta-h">
<h2 id="cta-h">{t}</h2>
<p>{x}</p>
<div class="cta-row"><a class="btn btn-wa" href="{shell['wa_blog']}" target="_blank" rel="noopener">{shell['i_chat']}<span>WhatsApp'tan yazın</span></a><a class="btn btn-night" href="{P.home()}#ornek">Asistanı deneyin</a></div>
</aside>"""


def post_page(shell, posts, p, kind):
    P = Paths(kind, 2)
    url = f"{shell['site']}/blog/{p['slug']}/"
    upd = p.get("updated") or p["date"]
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "BlogPosting", "headline": p["title"], "description": p["description"], "inLanguage": "tr-TR",
         "datePublished": p["date"], "dateModified": upd, "mainEntityOfPage": url, "url": url,
         "keywords": ", ".join(p.get("keywords", [])),
         "author": {"@type": "Person", "name": "Şahin Karadaş", "url": shell["site"] + "/"},
         "publisher": {"@type": "Person", "name": "Şahin Karadaş", "url": shell["site"] + "/"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Ana sayfa", "item": shell["site"] + "/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": shell["site"] + "/blog/"},
            {"@type": "ListItem", "position": 3, "name": p["title"], "item": url}]}]}
    extra = (f'<meta property="og:type" content="article">\n<meta property="og:title" content="{e(p["title"])}">\n'
             f'<meta property="article:published_time" content="{p["date"]}">\n<meta property="article:modified_time" content="{upd}">')
    others = [o for o in posts if o["slug"] != p["slug"]][:3]
    more = ""
    if others:
        more = ('<nav class="post-more" aria-labelledby="more-h"><h2 id="more-h">Diğer yazılar</h2><ul>'
                + "".join(f'<li><a href="{P.post(o["slug"])}">{o["title"]}</a></li>' for o in others) + "</ul></nav>")
    return (head(shell, P, f"{p['seo_title']} | Şahin Karadaş", p["description"], url, extra, ld) + top(shell, P, False) + f"""
<main id="icerik" class="b-main">
<div class="wrap">
<article class="post">
<nav class="crumbs" aria-label="Sayfa yolu"><ol><li><a href="{P.home()}">Ana sayfa</a></li><li><a href="{P.blog()}">Blog</a></li></ol></nav>
<header class="post-hd">
<p><span class="eye">{p['category']}</span></p>
<h1 class="post-h1">{p['title']}</h1>
<p class="post-lead">{p['lead']}</p>
<p class="post-meta"><span>Şahin Karadaş</span><span class="dot" aria-hidden="true"></span><time datetime="{p['date']}">{tarih(p['date'])}</time><span class="dot" aria-hidden="true"></span><span>{p['min']} dk okuma</span></p>
</header>
<div class="prose">
{p['body'].replace('@@HOME@@', P.home()).replace('@@BLOG@@', P.blog())}
</div>
{cta(shell, P, p)}
{more}
</article>
</div>
</main>
{shell['footer']}
{JS}
</body>
</html>
""")


def list_page(shell, posts, kind):
    P = Paths(kind, 1)
    url = shell["site"] + "/blog/"
    desc = ("Instagram ve WhatsApp mesajları, Meta reklamları ve otomasyon üzerine işletme sahipleri için sade, "
            "uygulanabilir yazılar. Şahin Karadaş'ın blogu.")
    ld = {"@context": "https://schema.org", "@type": "Blog", "name": "Şahin Karadaş Blog", "url": url, "inLanguage": "tr-TR",
          "author": {"@type": "Person", "name": "Şahin Karadaş", "url": shell["site"] + "/"},
          "blogPost": [{"@type": "BlogPosting", "headline": p["title"], "url": f"{shell['site']}/blog/{p['slug']}/",
                        "datePublished": p["date"]} for p in posts]}
    extra = '<meta property="og:type" content="website">\n<meta property="og:title" content="Blog | Şahin Karadaş">'
    cards = "".join(f"""
<li class="b-card">
<p class="post-meta"><time datetime="{p['date']}">{tarih(p['date'])}</time><span class="dot" aria-hidden="true"></span><span>{p['category']}</span><span class="dot" aria-hidden="true"></span><span>{p['min']} dk okuma</span></p>
<h2><a href="{P.post(p['slug'])}">{p['title']}</a></h2>
<p>{p['description']}</p>
<span class="more" aria-hidden="true">Yazıyı okuyun {shell['i_arrow']}</span>
</li>""" for p in posts)
    return (head(shell, P, "Blog | Şahin Karadaş", desc, url, extra, ld) + top(shell, P, True) + f"""
<main id="icerik" class="b-main">
<div class="wrap">
<div class="b-wrap">
<nav class="crumbs" aria-label="Sayfa yolu"><ol><li><a href="{P.home()}">Ana sayfa</a></li></ol></nav>
<header class="b-hd">
<p><span class="eye">Blog</span></p>
<h1 class="post-h1">Reklam, mesaj ve otomasyon üzerine notlar</h1>
<p class="post-lead">İşletme sahipleri için Instagram ve WhatsApp mesajları, Meta reklamları ve otomasyon üzerine sade, hemen uygulanabilir yazılar.</p>
</header>
<ul class="b-list">{cards}
</ul>
</div>
</div>
</main>
{shell['footer']}
{JS}
</body>
</html>
""")


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write(text)


def build(shell, posts, out, kind):
    import shutil
    shutil.rmtree(os.path.join(out, "blog"), ignore_errors=True)   # silinen yazılar sitede kalmasın
    write(os.path.join(out, "blog", "index.html"), list_page(shell, posts, kind))
    for p in posts:
        write(os.path.join(out, "blog", p["slug"], "index.html"), post_page(shell, posts, p, kind))
    if kind == "site":
        today = dt.date.today().isoformat()
        last = max([p.get("updated") or p["date"] for p in posts] or [today])
        urls = [(shell["site"] + "/", today), (shell["site"] + "/blog/", last)]
        urls += [(f"{shell['site']}/blog/{p['slug']}/", p.get("updated") or p["date"]) for p in posts]
        write(os.path.join(out, "sitemap.xml"), '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
              + "".join(f"  <url><loc>{u}</loc><lastmod>{d}</lastmod></url>\n" for u, d in urls) + "</urlset>\n")
        write(os.path.join(out, "robots.txt"), f"User-agent: *\nAllow: /\nDisallow: /yonetim/\n\nSitemap: {shell['site']}/sitemap.xml\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--site")
    ap.add_argument("--art")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    shell, posts = load()
    check(posts)
    if a.check:
        sys.exit(0)
    if a.site:
        for need in ("index.html", shell["css"]):
            if not os.path.exists(os.path.join(a.site, need)):
                sys.exit(f"{a.site} içinde {need} yok")
        build(shell, posts, a.site, "site")
    if a.art:
        build(shell, posts, a.art, "art")
    print("tamam:", ", ".join(p["slug"] for p in posts))
