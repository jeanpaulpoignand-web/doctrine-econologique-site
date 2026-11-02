#!/usr/bin/env python3
"""Génère piliers/<slug>/index.html depuis le PDF « Aller droit au but » de chaque pilier.
Usage : python3 tools/build_piliers.py [slug ...]   (sans argument : tous les piliers publiés)
Dépendances : pdfplumber. Aucune étape de build n'est ajoutée à la publication : les pages générées sont commitées.
Le texte vient uniquement du PDF ; titre de page, accroche et résumé viennent de tools/piliers.json (à valider)."""
import json, os, re, subprocess, sys, html
import pdfplumber

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://jeanpaulpoignand-web.github.io/doctrine-econologique-site/"
TAGS = ("[FAIT]", "[CALCUL]", "[ANALYSE]", "[PROPOSITION]")
MOIS = ["janvier","février","mars","avril","mai","juin","juillet","août","septembre","octobre","novembre","décembre"]

def fr_date(iso):
    y, m, d = iso.split("-")
    return f"{int(d)} {MOIS[int(m)-1]} {y}"

def git_date(path, first):
    cmd = ["git", "log", "--follow", "--format=%cs"] + (["--diff-filter=A"] if first else ["-1"]) + ["--", path]
    out = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True).stdout.split()
    return (out[-1] if first else out[0]) if out else ""

def esc(s): return html.escape(s, quote=False)

def read_lines(pdf_path, fine=False):
    """Retourne, par page, des lignes {y, segs:[{x0,x1,text,size,font}]} (segments séparés par un grand blanc horizontal)."""
    pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for p in pdf.pages:
            words = p.extract_words(extra_attrs=["size", "fontname"], keep_blank_chars=False, use_text_flow=False)
            rows = []
            for w in sorted(words, key=lambda w: (round(w["top"]), w["x0"])):
                if rows and abs(rows[-1]["y"] - w["top"]) <= 3:
                    rows[-1]["w"].append(w)
                else:
                    rows.append({"y": w["top"], "w": [w]})
            lines = []
            for r in rows:
                segs = []
                for w in sorted(r["w"], key=lambda w: w["x0"]):
                    gap_limit = max(7, w["size"] * 0.9) if fine else max(14, w["size"] * 1.6)
                    if segs and w["x0"] - segs[-1]["x1"] <= gap_limit:
                        s = segs[-1]; s["text"] += " " + w["text"]; s["x1"] = w["x1"]
                        s["size"] = max(s["size"], w["size"])
                    else:
                        segs.append({"x0": w["x0"], "x1": w["x1"], "text": w["text"], "size": w["size"], "font": w["fontname"].split("+")[-1]})
                if fine:
                    k2 = []
                    for sg in segs:
                        if k2 and k2[-1]["text"].strip() in ("•", "–"):
                            k2[-1]["text"] = k2[-1]["text"].strip() + " " + sg["text"]; k2[-1]["x1"] = sg["x1"]; k2[-1]["size"] = max(k2[-1]["size"], sg["size"])
                        else: k2.append(sg)
                    segs = [x for x in k2 if x["text"].strip()]
                    if not segs: continue
                lines.append({"y": r["y"], "segs": segs, "page_h": p.height})
            pages.append(lines)
    return pages

def is_noise(line, pi, last):
    t = " ".join(s["text"] for s in line["segs"])
    y = line["y"]
    if y < 30: return True                                    # « Retour au site / Approfondir ce pilier sur Drive »
    if y > 780 and "Pilier" in t: return True                 # pied de page
    if re.match(r"^(←\s*)?Retour au site", t): return True
    if t.startswith("🎯") or t.strip() == "ALLER DROIT AU BUT": return True
    if re.match(r"^(ALLER DROIT AU BUT|DOCTRINE ÉCONOLOGIQUE)\b.*(PILIER|·)", t) and line["segs"][0]["size"] <= 10: return True
    if re.fullmatch(r"(DOCTRINE ÉCONOLOGIQUE|·|PILIER [IVXL]+)( · )?(PILIER [IVXL]+)?", t.strip()): return True
    if pi == last and t.startswith("Voir le site"): return True
    if re.fullmatch(r"[·\s]+", t): return True               # pointillés décoratifs
    return False

def classify(line):
    s0 = line["segs"][0]; t = " ".join(s["text"] for s in line["segs"])
    f, size = s0["font"], s0["size"]
    if len(line["segs"]) > 1: return "row"
    if t.lstrip().startswith(("•", "–")): return "li"
    if re.match(r"^\d+\.\s", t) and "Bold" in f: return "step"
    if "Serif" in f and "Bold" in f and size >= 19: return "h2"
    if "Serif" in f and "Bold" in f and size >= 12 and len(t) < 90: return "h3"
    if "Serif" in f and "Bold" in f and size >= 12: return "lead"
    if "Serif" in f and "Italic" in f and size >= 10: return "quote"
    if "Mono" in f and "Bold" in f and size <= 9 and not t.startswith(TAGS) and t.upper() == t: return "label"
    return "p"

def build_blocks(pages):
    last = len(pages) - 1
    blocks = []; prev = None; skip_more = False
    for pi, lines in enumerate(pages):
        prev = None
        for ln in lines:
            if is_noise(ln, pi, last): continue
            k = classify(ln)
            t = " ".join(s["text"] for s in ln["segs"])
            f, size = ln["segs"][0]["font"], ln["segs"][0]["size"]
            if k == "row":
                segs = ln["segs"]
                if re.fullmatch(r"\d", segs[0]["text"].strip()):      # étape numérotée « 1 | TITRE »
                    num = segs[0]["text"].strip(); rest = " ".join(x["text"] for x in segs[1:])
                    if blocks and blocks[-1]["k"] == "label" and ln["y"] - blocks[-1].get("y", -99) < 14:
                        lab = blocks.pop()["text"]
                        blocks.append({"k": "step", "text": f"{num}. {lab}"}); blocks.append({"k": "p", "text": rest})
                        prev = {"k": "p", "font": segs[1]["font"], "size": segs[1]["size"], "y": ln["y"]}
                    else:
                        blocks.append({"k": "step", "text": f"{num}. {rest}"}); prev = None
                    continue
                bk = blocks[-1] if blocks else None
                big = any(x["size"] >= 14 for x in segs)
                cont = (bk and bk["k"] == "cards" and ln["y"] - bk["y"] < 40 and len(segs) <= len(bk["cols"])
                        and not (big and bk["last_small"] and ln["y"] - bk["y"] >= 27)
                        and (len(segs) == len(bk["cols"]) or ln["y"] - bk["y"] <= 16))
                if cont:
                    for x in segs:
                        c = min(bk["cols"], key=lambda c: abs(c["cx"] - (x["x0"] + x["x1"]) / 2))
                        c["parts"].append((x["text"], x["size"]))
                    bk["y"] = ln["y"]; bk["last_small"] = not big
                else:
                    blocks.append({"k": "cards", "cols": [{"cx": (x["x0"] + x["x1"]) / 2, "parts": [(x["text"], x["size"])]} for x in segs], "y": ln["y"], "last_small": not big})
                prev = None; continue
            if blocks and blocks[-1]["k"] == "cards" and ln["y"] - blocks[-1]["y"] <= 16 and size <= 11:
                bk = blocks[-1]; sg = ln["segs"][0]
                c = min(bk["cols"], key=lambda c: abs(c["cx"] - (sg["x0"] + sg["x1"]) / 2)) if len(bk["cols"]) > 1 else bk["cols"][0]
                c["parts"].append((t, size)); bk["y"] = ln["y"]; continue
            if k == "label": blocks.append({"k": "label", "text": t, "y": ln["y"]}); prev = None; continue
            m = re.match(r"^(\[(?:FAIT|CALCUL|ANALYSE|PROPOSITION)\])\s+(.*)$", t)
            if m and m.group(2) and m.group(2).upper() == m.group(2) and len(m.group(2)) < 70:
                blocks.append({"k": "label", "text": m.group(2), "tag": m.group(1)}); prev = None; continue
            if k == "p" and re.search(r"[A-Za-zÀ-ÿ]", t) and prev and prev.get("num") and blocks[-1]["k"] == "step" and "Bold" not in f and False: pass
            mergeable = k in ("p", "quote", "lead", "h2", "h3", "step", "li")
            fontsame = (prev and (prev["font"] == f or (k == "p" and prev["k"] == "p")))
            if (mergeable and blocks and prev and prev["k"] == k and fontsame and abs(prev["size"] - size) < .3
                    and 0 < ln["y"] - prev["y"] <= size * 1.9 and not t.startswith(TAGS)):
                bk = blocks[-1]
                bk["text"] = (bk["text"][:-1] + t) if bk["text"].endswith("-") and not bk["text"].endswith(" -") else bk["text"] + " " + t
            else:
                blocks.append({"k": k, "text": t})
            prev = {"k": k, "font": f, "size": size, "y": ln["y"]}
    return blocks

def render_blocks(blocks, nom):
    out = []; in_list = False
    def close():
        nonlocal in_list
        if in_list: out.append("</ul>"); in_list = False
    def tagged(t):
        m = re.match(r"^(\[(?:FAIT|CALCUL|ANALYSE|PROPOSITION)\])\s*(.*)$", t)
        return (f'<span class="tag">{esc(m.group(1))}</span> {esc(m.group(2))}') if m else esc(t)
    for b in blocks:
        k = b["k"]
        if k == "li":
            if not in_list: out.append("<ul>"); in_list = True
            items = [x.strip() for x in re.split(r"\s*•\s*", b["text"]) if x.strip()]
            for it in items: out.append(f"<li>{esc(it)}</li>")
            continue
        close()
        if k == "cards":
            cards = []
            for c in b["cols"]:
                c = c["parts"]
                inner = []; buf = []
                def flush():
                    if buf: inner.append(f"<span>{tagged(re.sub(chr(92)+'s+', ' ', ' '.join(buf)).strip())}</span>"); buf.clear()
                for tx, sz in c:
                    if sz >= 14: flush(); inner.append(f"<strong>{esc(tx)}</strong>")
                    else: buf.append(tx)
                flush()
                cards.append('<div class="card">' + "".join(inner) + "</div>")
            out.append('<div class="cards">' + "".join(cards) + "</div>")
        elif k == "h2" and b["text"].startswith("«"): out.append(f'<p class="hero">{esc(b["text"])}</p>')
        elif k == "h2": out.append(f"<h2>{esc(b['text'])}</h2>")
        elif k == "h3": out.append(f"<h3>{esc(b['text'])}</h3>")
        elif k == "label":
            tg = f'<span class="tag">{esc(b["tag"])}</span> ' if b.get("tag") else ""
            out.append(f'<h3 class="label">{tg}{esc(b["text"])}</h3>')
        elif k == "step": out.append(f'<h3 class="step">{tagged(b["text"])}</h3>')
        elif k == "quote": out.append(f'<p class="lead">{esc(b["text"])}</p>')
        elif k == "lead": out.append(f'<p class="question">{esc(b["text"])}</p>')
        else:
            t = b["text"]
            cls = ' class="legend"' if t.startswith("[FAIT] donnée sourcée") else ""
            out.append(f"<p{cls}>{tagged(t)}</p>")
    close()
    return "\n".join(out)

CSS = """:root{--rouge:#8B2C1E;--or:#6B5520;--nuit:#0E1B2E;--fond:#f5f0e5;--ligne:#d4c8b5;--texte:#1d2430;--doux:#4a5160}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--fond);color:var(--texte);font:18px/1.65 Georgia,'Iowan Old Style',serif}
main{max-width:760px;margin:0 auto;padding:28px 20px 60px}
.crumbs{font:600 14px/1.4 system-ui,-apple-system,sans-serif;color:var(--doux);margin:0 0 18px}.crumbs a{color:var(--nuit)}
h1{font-size:clamp(30px,6vw,44px);line-height:1.15;margin:0 0 10px;color:var(--nuit)}
.meta{font:14px/1.5 system-ui,-apple-system,sans-serif;color:var(--doux);margin:0 0 22px}
.resume{font-size:20px;color:var(--nuit);border-left:4px solid var(--rouge);padding:4px 0 4px 16px;margin:0 0 28px}
h2{font-size:clamp(24px,4.5vw,30px);line-height:1.25;color:var(--nuit);margin:44px 0 12px;border-top:1px solid var(--ligne);padding-top:24px}
h3{font-size:20px;line-height:1.3;color:var(--nuit);margin:28px 0 8px}
h3.label{font:700 13px/1.4 system-ui,-apple-system,sans-serif;letter-spacing:.08em;text-transform:uppercase;color:var(--or);margin:30px 0 6px}
h3.step{font-size:19px}
p{margin:0 0 14px}.lead{font-size:22px;font-style:italic;color:var(--nuit)}.question{font-weight:700;font-size:20px}
.tag{display:inline-block;font:700 12px/1.6 system-ui,-apple-system,sans-serif;letter-spacing:.04em;color:var(--rouge);border:1px solid var(--rouge);border-radius:4px;padding:0 6px;margin-right:4px}
ul{padding-left:22px;margin:0 0 16px}li{margin:0 0 6px}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;margin:14px 0 20px}.card{background:#fff;border:1px solid var(--ligne);border-radius:8px;padding:14px 16px;font:15px/1.5 system-ui,-apple-system,sans-serif}.card>span{display:block}.card .row{display:flex;justify-content:space-between;align-items:baseline;gap:14px;padding:6px 0;border-top:1px solid var(--ligne)}.card .row b{font:700 20px/1.2 Georgia,serif;color:var(--rouge);white-space:nowrap}.card .stat-ligne{font:700 28px/1.2 Georgia,serif;color:var(--rouge);margin-bottom:6px}.card .gros{font:700 18px/1.35 system-ui,-apple-system,sans-serif;margin-bottom:8px}.card .row.fort{background:#f6e3df;border-radius:6px;padding:10px;margin-top:6px;border-top:0;font-weight:700}.card .row.fort span b{font:700 16px/1.4 system-ui,-apple-system,sans-serif;color:var(--texte);white-space:normal}.card .note{font-size:13px;color:var(--doux);margin-top:8px}.card .reste{margin-top:6px;font-weight:700}.card strong{display:block;font:700 28px/1.2 Georgia,serif;color:var(--rouge);margin-bottom:4px}.hero{font-size:clamp(26px,5vw,34px);line-height:1.25;font-style:italic;font-weight:700;color:var(--rouge);margin:6px 0 16px}.tablewrap{overflow-x:auto;margin:14px 0 20px}table{border-collapse:collapse;width:100%;font:15px/1.5 system-ui,-apple-system,sans-serif;background:#fff}th{background:var(--rouge);color:#fff;text-align:left;padding:8px 10px}td{border:1px solid var(--ligne);padding:8px 10px;vertical-align:top}.legend{font:14px/1.5 system-ui,-apple-system,sans-serif;color:var(--doux)}.sr{position:absolute;left:-9999px}
.more{margin-top:44px;padding:20px;background:#fff;border:1px solid var(--ligne);border-radius:10px;font:16px/1.6 system-ui,-apple-system,sans-serif}
.more h2{font-size:22px;margin:0 0 10px;border:0;padding:0}.more ul{list-style:none;padding:0}.more li{margin:0 0 8px}
.actions{display:flex;flex-direction:column;gap:12px}.actions a{text-decoration:none;color:var(--touch-fg);margin:0}.actions .btn-touch--soft{color:var(--rouge)}
.pager{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;margin-top:28px;font:600 15px/1.4 system-ui,-apple-system,sans-serif}
.pager a{color:var(--nuit)}
@media print{.doctrine-navigation,.pager{display:none}}"""

AUTEUR = "Jean Paul Poignand"
CONTACT = "contactdoctrineeconologique@gmail.com"

def page(p, body, pdf_kb, d_pub, d_maj, prev=None, nxt=None):
    url = f"{SITE}piliers/{p['slug']}/"
    titre = f"{p['titre_page']} | Doctrine Éconologique"
    desc = f"{p['resume']} {p['accroche']}."
    jsonld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "headline": p["titre_page"], "description": desc, "datePublished": d_pub, "dateModified": d_maj,
         "inLanguage": "fr-FR", "mainEntityOfPage": url,
         "author": {"@type": "Person", "name": AUTEUR, "url": SITE + "a-propos/"},
         "publisher": {"@type": "Organization", "name": "Doctrine Éconologique", "url": SITE}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Accueil", "item": SITE},
            {"@type": "ListItem", "position": 2, "name": "Piliers", "item": SITE + "#piliers"},
            {"@type": "ListItem", "position": 3, "name": p["nom"], "item": url}]}]}
    qcm = "".join(f'<a class="btn-touch btn-touch--fluid" href="../../{q["url"]}">{esc(q["nom"])}</a>' for q in p["questionnaires"])
    annexes = "".join(f'<a class="btn-touch btn-touch--soft btn-touch--fluid" href="../../{a["url"]}">{esc(a["nom"])} (PDF)</a>\n' for a in p["annexes"])
    pager = '<nav class="pager" aria-label="Autres piliers">' + (f'<a href="../{prev["slug"]}/">← Pilier {prev["romain"]} · {esc(prev["nom"])}</a>' if prev else "<span></span>") + (f'<a href="../{nxt["slug"]}/">Pilier {nxt["romain"]} · {esc(nxt["nom"])} →</a>' if nxt else "<span></span>") + "</nav>"
    return f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(titre)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article">
<meta property="og:title" content="{html.escape(titre)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}assets/partage-doctrine.jpg">
<link rel="stylesheet" href="../../assets/doctrine-navigation.css">
<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>
<style>{CSS}</style>
</head>
<body>
<nav class="doctrine-navigation" aria-label="Navigation de la Doctrine">
  <a href="../../#pilier-{p['numero']}">Retour au site de la Doctrine</a>
  <a class="doctrine-navigation-drive" href="{p['drive']}" target="_blank" rel="noopener">Approfondir ce pilier sur Drive</a>
</nav>
<main>
<p class="crumbs"><a href="../../">Accueil</a> › <a href="../../#piliers">Piliers</a> › {esc(p['nom'])}</p>
<h1>{esc(p['nom'])}</h1>
<p class="meta">Pilier {p['romain']} · Publié le {fr_date(d_pub)} · Mis à jour le {fr_date(d_maj)} · Par <a href="../../a-propos/">{AUTEUR}</a></p>
<p class="resume">{esc(p['resume'])}</p>
{body}
<aside class="more" aria-labelledby="plus">
<h2 id="plus">Ressources liées</h2>
<div class="actions">
{qcm}
<a class="btn-touch btn-touch--soft btn-touch--fluid" href="../../{p['pdf']}">Version PDF ({pdf_kb} Ko)</a>
{annexes}
<a class="btn-touch btn-touch--soft btn-touch--fluid" href="{p['drive']}" target="_blank" rel="noopener">Dossier Drive du pilier <span class="sr">(s'ouvre dans un nouvel onglet)</span></a>
</div>
</aside>
{pager}
</main>
<script src="../../assets/doctrine-share.js" defer></script>
</body>
</html>
"""

def apropos():
    url = SITE + "a-propos/"
    titre = "À propos : qui porte la Doctrine Éconologique | Doctrine Éconologique"
    desc = "La Doctrine Éconologique est portée par Jean Paul Poignand. Qui il est, pourquoi cette doctrine, comment elle est construite avec cinq intelligences artificielles et arbitrée par un humain."
    jsonld = {"@context": "https://schema.org", "@graph": [
        {"@type": "AboutPage", "name": "À propos de la Doctrine Éconologique", "description": desc, "url": url, "inLanguage": "fr-FR",
         "mainEntity": {"@type": "Person", "name": AUTEUR, "url": url, "email": CONTACT}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Accueil", "item": SITE},
            {"@type": "ListItem", "position": 2, "name": "À propos", "item": url}]}]}
    ias = [("Claude","Anthropic","architecte, intégrateur"),("ChatGPT","OpenAI","rigueur institutionnelle"),("Gemini","Google","corrélations macro"),("Grok","xAI","données de terrain"),("Perplexity","Perplexity AI","sourcing systématique")]
    li = "".join(f"<li><b>{n}</b> ({e}) : {r}.</li>" for n,e,r in ias)
    return f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(titre)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:title" content="{html.escape(titre)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}assets/partage-doctrine.jpg">
<link rel="stylesheet" href="../assets/doctrine-navigation.css">
<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>
<style>{CSS}</style>
</head>
<body>
<nav class="doctrine-navigation" aria-label="Navigation de la Doctrine">
  <a href="../">Retour au site de la Doctrine</a>
</nav>
<main>
<p class="crumbs"><a href="../">Accueil</a> › À propos</p>
<h1>À propos de la Doctrine Éconologique</h1>
<h2>Qui porte la doctrine</h2>
<p>La Doctrine Éconologique est portée par {AUTEUR}. Ingénieur des techniques et industries agroalimentaires, il a commencé ce travail en janvier 2026. Il tranche les arbitrages et en assume le contenu sous son nom.</p>
<h2>Pourquoi cette doctrine</h2>
<p>Le mot « éconologie » réunit économie et écologie. L’écologie dit surtout ce qu’il ne faut pas faire ; l’éconologie propose des solutions, dans le sens de la souveraineté et de la production locale.</p>
<p>Une société prospère ne peut pas durablement dissimuler ce qu’elle produit, ce qu’elle consomme, et qui paie réellement.</p>
<h2>Comment elle est construite</h2>
<p>La doctrine est construite par <em>triangulation contradictoire</em>. Chaque thèse est soumise à cinq intelligences artificielles aux biais et architectures distincts. Leurs désaccords révèlent les angles morts. Les arbitrages restent humains : {AUTEUR} tranche.</p>
<p>Les intelligences artificielles sont des outils de travail, avec chacune un rôle :</p>
<ul>{li}</ul>
<p>Anthropic, OpenAI, Google, xAI et Perplexity AI sont des marques de leurs propriétaires respectifs. Leur mention ne suggère aucun partenariat ni endossement.</p>
<h2>Comment lire les chiffres</h2>
<p>Chaque affirmation importante porte une étiquette : [FAIT] pour une donnée sourcée, [CALCUL] pour un calcul reproductible, [HYPOTHÈSE] pour ce qui reste à démontrer, [ANALYSE] pour une lecture de la doctrine, [PROPOSITION] pour une mesure proposée. Les faits sont ainsi distingués des propositions.</p>
<h2>Contact</h2>
<p>Pour une question, une correction ou une source à signaler : <a href="mailto:{CONTACT}">{CONTACT}</a>.</p>
<p><a class="btn-touch btn-touch--soft btn-touch--fluid" href="../#piliers">Voir les piliers</a></p>
</main>
</body>
</html>
"""

def main(slugs):
    piliers = json.load(open(os.path.join(ROOT, "tools/piliers.json"), encoding="utf-8"))
    pub = [x for x in piliers if x["statut"] != "chantier"]
    for i, p in enumerate(pub):
        if slugs and p["slug"] not in slugs: continue
        prev = pub[i-1] if i > 0 else None; nxt = pub[i+1] if i < len(pub)-1 else None
        pdf = os.path.join(ROOT, p["pdf"])
        blocks = build_blocks(read_lines(pdf, p.get("colonnes_fines", False)))
        body = render_blocks(blocks, p["nom"])
        man = os.path.join(ROOT, "tools", "corps", p["slug"] + ".html")
        if p.get("corps_manuel") and os.path.exists(man):      # corps corrigé à la main à partir du PDF (mise en page complexe)
            body = open(man, encoding="utf-8").read().strip()
        words_pdf = len(subprocess.run(["pdftotext", pdf, "-"], capture_output=True, text=True).stdout.split())
        words_html = len(re.sub(r"<[^>]+>", " ", body).split())
        d_pub, d_maj = git_date(p["pdf"], True), git_date(p["pdf"], False)
        out = os.path.join(ROOT, "piliers", p["slug"], "index.html")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(page(p, body, round(os.path.getsize(pdf) / 1024), d_pub, d_maj, prev, nxt))
        print(f"{p['slug']}: PDF {words_pdf} mots (brut) / page {words_html} mots (corps) / publié {d_pub} / maj {d_maj}")

if __name__ == "__main__":
    main(sys.argv[1:])
    if not sys.argv[1:]:
        os.makedirs(os.path.join(ROOT, "a-propos"), exist_ok=True)
        open(os.path.join(ROOT, "a-propos", "index.html"), "w", encoding="utf-8").write(apropos())
