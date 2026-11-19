#!/usr/bin/env python3
"""Builds public/{index,pt/index,es/index,404}.html from template.html + strings.py.
Run: python3 src/build.py"""
import html as H, json, pathlib, re
from strings import S
import maps as M

ROOT = pathlib.Path(__file__).resolve().parent.parent
PUB = ROOT / "public"
SITE = "https://www.elporvenir.farm"
TPL = (ROOT / "src" / "template.html").read_text()

def picture(name, widths, alt, sizes, cls="", eager=False, w=1672, h=941, rel=""):
    srcs = []
    for fmt in ("avif", "webp"):
        ss = ", ".join(f"{rel}assets/img/{name}-{x}.{fmt} {x}w" for x in widths)
        srcs.append(f'<source type="image/{fmt}" srcset="{ss}" sizes="{sizes}">')
    jpg = ", ".join(f"{rel}assets/img/{name}-{x}.jpg {x}w" for x in widths)
    load = 'fetchpriority="high" decoding="async"' if eager else 'loading="lazy" decoding="async"'
    return (f'<picture{(" class=" + chr(34) + cls + chr(34)) if cls else ""}>' + "".join(srcs) +
            f'<img src="{rel}assets/img/{name}-{widths[-1]}.jpg" srcset="{jpg}" sizes="{sizes}" '
            f'width="{w}" height="{h}" alt="{alt}" {load}></picture>')

def render(code):
    t = S[code]
    html = TPL
    rel = "" if code == "en" else "../"
    pics = {
        "PIC_HERO": picture("aerial", [640, 1024, 1600], t["alt_aerial"], "100vw", eager=True, rel=rel),
        "PIC_ROWS": picture("rows", [640, 1024, 1600], t["alt_rows"], "100vw", rel=rel),
        "PIC_LAKE": picture("aerial", [640, 1024, 1600], t["alt_lake"], "100vw", rel=rel),
    }
    langs = []
    for c, lab in (("en", "EN"), ("pt", "PT"), ("es", "ES")):
        cur = ' aria-current="true"' if c == code else ""
        href = (rel + S[c]["path"].lstrip("/")) or "./"
        langs.append(f'<a href="{href}" hreflang="{S[c]["lang"]}" lang="{S[c]["lang"]}"{cur}>{lab}</a>')
    alternates = "\n".join(
        f'<link rel="alternate" hreflang="{S[c]["lang"]}" href="{SITE}{S[c]["path"]}">' for c in S
    ) + f'\n<link rel="alternate" hreflang="x-default" href="{SITE}/">'
    ld = {
        "@context": "https://schema.org", "@type": "Organization",
        "name": "El Porvenir", "url": SITE + "/", "logo": SITE + "/assets/img/logo.png",
        "email": "info@elporvenir.farm", "telephone": "+39 345 005 4849",
        "sameAs": ["https://www.instagram.com/elporvenirfarm/"],
        "address": {"@type": "PostalAddress", "addressLocality": "Santa Cruz do Sul",
                    "addressRegion": "Rio Grande do Sul", "addressCountry": "BR"},
        "description": t["desc"],
    }
    extra = {
        "LANGS": "\n".join(langs), "ALTERNATES": alternates,
        "CANONICAL": SITE + t["path"], "LD": json.dumps(ld, ensure_ascii=False),
        "I18N": H.escape(json.dumps({k: t[k] for k in ("e_req", "e_mail", "ok", "fail", "f_sending", "c_copied")}, ensure_ascii=False)),
        "CODE": code, "REL": rel,
        "MAP_F": M.svg(M.FIG, "f", t["map_alt_f"]), "MAP_N": M.svg(M.NOG, "n", t["map_alt_n"]),
    }
    def sub(m):
        k = m.group(1)
        if k in pics: return pics[k]
        if k in extra: return extra[k]
        v = t[k]
        if re.fullmatch(r"st\d_n", k): v = v.replace(" kg", "<small>kg</small>")
        return v
    html = re.sub(r"\[\[([A-Za-z0-9_]+)\]\]", sub, html)
    leftover = re.findall(r"\[\[[^\]]+\]\]", html)
    assert not leftover, leftover
    return html

def page404(t=None, h=None, p=None, links=True, noindex=True):
    t = t or S["en"]
    return f"""<!DOCTYPE html><html lang="{t['lang']}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{h or 'Page not found'} — El Porvenir</title><meta name="robots" content="noindex"><link rel="icon" href="/favicon.png">
<style>@font-face{{font-family:"Inter Display";font-weight:300;src:url(/assets/fonts/InterDisplay-Light.woff) format("woff");font-display:swap}}
body{{margin:0;min-height:100vh;display:grid;place-items:center;background:#11150f;color:#e9e9e4;font:17px/1.6 system-ui,sans-serif;text-align:center;padding:24px}}
h1{{font:300 clamp(40px,7vw,80px)/1 "Inter Display",system-ui,sans-serif;letter-spacing:-.04em;margin:0}}p{{color:rgba(233,233,228,.72)}}a{{color:#c4a46a}}</style></head>
<body><main><h1>{h or t['notfound_h']}</h1><p>{p or t['notfound_p']}</p>
<p><a href="{t['path']}">{t['notfound_a']}</a>{(' · <a href="/pt/">Português</a> · <a href="/es/">Español</a>') if links else ''}</p></main></body></html>"""

if __name__ == "__main__":
    for code in S:
        out = PUB / S[code]["path"].strip("/") / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render(code))
        print("wrote", out.relative_to(ROOT))
    (PUB / "404.html").write_text(page404())
    for code in S:
        t = S[code]
        for slug, msg in (("sent", t["ok"]), ("not-sent", t["fail"])):
            d = PUB / t["path"].strip("/") / slug
            d.mkdir(parents=True, exist_ok=True)
            (d / "index.html").write_text(page404(t, t["c_h"].rstrip("."), msg, links=False))
    urls = "".join(
        f"<url><loc>{SITE}{S[c]['path']}</loc>" +
        "".join(f'<xhtml:link rel="alternate" hreflang="{S[d]["lang"]}" href="{SITE}{S[d]["path"]}"/>' for d in S) +
        "</url>" for c in S)
    (PUB / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        f'xmlns:xhtml="http://www.w3.org/1999/xhtml">{urls}</urlset>\n')
    (PUB / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
    print("done")
