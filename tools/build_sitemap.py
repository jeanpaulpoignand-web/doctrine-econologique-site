#!/usr/bin/env python3
"""Génère sitemap.xml à partir des pages HTML publiées.

Règles : exclut ce que _config.yml exclut, les pages noindex, 404.html et les
fichiers de vérification Google ; <loc> = URL canonique lue dans la page ;
<lastmod> = date du dernier commit du fichier (pour une page pilier générée :
date du dernier commit du PDF source) ; pas de priority ni de changefreq ;
tri par chemin. Usage : python3 tools/build_sitemap.py
"""
import datetime, json, os, re, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://jeanpaulpoignand-web.github.io/doctrine-econologique-site/"
AUJOURDHUI = datetime.date.today().isoformat()


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True).stdout.strip()


def exclusions():
    ex, on = [], False
    for l in open(os.path.join(ROOT, "_config.yml"), encoding="utf-8"):
        if l.startswith("exclude:"):
            on = True
        elif on and l.strip().startswith("- "):
            ex.append(l.strip()[2:].strip())
        elif on and l.strip() and not l.startswith("#"):
            on = False
    return ex


def exclu(rel, ex):
    return any(rel == e or (e.endswith("/") and rel.startswith(e)) for e in ex)


def lastmod(rel, sources, sales):
    src = sources.get(rel, rel)
    if src in sales:
        return AUJOURDHUI
    d = git("log", "-1", "--format=%cs", "--", src)
    return d or AUJOURDHUI


def main():
    ex = exclusions()
    sources = {}
    pj = os.path.join(ROOT, "tools", "piliers.json")
    if os.path.exists(pj):
        for p in json.load(open(pj, encoding="utf-8")):
            sources[f"piliers/{p['slug']}/index.html"] = p["pdf"]
    sales = {l.strip().split(None, 1)[1].split(" -> ")[-1].strip('"') for l in git("status", "--porcelain").splitlines() if l.strip()}
    urls = []
    for dp, dn, fn in os.walk(ROOT):
        dn[:] = [d for d in dn if not d.startswith(".")]
        for f in fn:
            if not f.endswith(".html"):
                continue
            rel = os.path.relpath(os.path.join(dp, f), ROOT).replace(os.sep, "/")
            if exclu(rel, ex) or rel == "404.html" or re.match(r"google[0-9a-f]+\.html$", f):
                continue
            h = open(os.path.join(ROOT, rel), encoding="utf-8").read()
            if re.search(r'<meta[^>]+name=["\']robots["\'][^>]*noindex', h, re.I):
                continue
            m = re.search(r'<link[^>]+rel=["\']canonical["\'][^>]*href=["\']([^"\']+)', h, re.I)
            if m:
                loc = m.group(1)
            else:
                loc = SITE + (rel[:-10] if rel.endswith("index.html") else rel)
            urls.append((rel, loc, lastmod(rel, sources, sales)))
    urls.sort()
    out = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for rel, loc, lm in urls:
        out.append(f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{lm}</lastmod>\n  </url>")
    out.append("</urlset>")
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write("\n".join(out) + "\n")
    print(len(urls), "URL")


if __name__ == "__main__":
    main()
