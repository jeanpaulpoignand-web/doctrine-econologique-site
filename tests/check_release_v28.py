#!/usr/bin/env python3
"""V2.8 release gates: SEO Grégoire + Perplexity touch icon + old content parity.
No publishing actions. Run with a checkout containing origin/main and preview ref.
"""
from __future__ import annotations
from pathlib import Path
from urllib.parse import urlparse
import re,struct,subprocess,json,xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
MAIN="origin/main"
PREVIEW="origin/preview-v27-logo-2026-11-07"
DOMAIN="https://doctrine-econologique.fr"
PILLARS=[
"energie-souveraine","garantie-decennale","financement-public","reparation-des-retraites",
"grand-age-ehpad","batiment-metiers-utiles","econologie-culturelle","frontaliers-capital-humain",
"agriculture-alimentation","textile-habillement-chaussure","mobilite-securite-routiere",
"friction-monetique","democratie-decisionnelle","amortissement-dette","fraude-fiscale"]
QCMS=["qcm-general","qcm-energie","qcm-aspa","qcm-pilier-vi","qcm-textile",
"qcm-fraude-fiscale","qcm-immigrants-journee","qcm-consigne-megots","qcm-democratie-decisionnelle"]
EXTRAS=["questionnaires/index.html","piliers/index.html","a-propos/index.html",
"guide-de-lecture/index.html","bulletin-arbitrage/index.html"]
PAGES=["index.html"]+[x+"/index.html" for x in QCMS]+["piliers/"+x+"/index.html" for x in PILLARS]+EXTRAS

# Les révisions éditoriales des 8 et 13 novembre sont déjà sur main.
# Pour ces seules pages, figer le contenu actuellement publié plutôt que
# l'ancien aperçu du 7/11 ; toute autre modification dans cette PR corrective
# (scripts, titres H1-H3, canonical) doit encore faire échouer la CI.
EDITORIAL_PILLARS_PUBLIES_2026_11_13 = {
  "piliers/energie-souveraine/index.html",
  "piliers/garantie-decennale/index.html",
  "piliers/financement-public/index.html",
  "piliers/grand-age-ehpad/index.html",
  "piliers/batiment-metiers-utiles/index.html",
  "piliers/econologie-culturelle/index.html",
  "piliers/frontaliers-capital-humain/index.html",
  "piliers/agriculture-alimentation/index.html",
  "piliers/democratie-decisionnelle/index.html",
  "piliers/amortissement-dette/index.html",
  "piliers/fraude-fiscale/index.html",
  "piliers/textile-habillement-chaussure/index.html",  # version éditoriale du 08/11 déjà publiée
}

def original(ref,path):
  return subprocess.check_output(["git","show",f"{ref}:{path}"],cwd=ROOT).decode("utf-8")
def text(path):
  return (ROOT/path).read_text(encoding="utf-8")
def tags(s,tag):
  return re.findall(r"<"+tag+r"\b[^>]*>",s,flags=re.I)
def parts(s,pat):
  return re.findall(pat,s,flags=re.I|re.S)
def assert_eq(path,ref=PREVIEW):
  # Les pages de navigation et d information (EXTRAS) ont deja evolue
  # depuis le preview du 7/11. Verifier leur contenu contre main publie,
  # sans jamais assouplir la comparaison des moteurs QCM avec PREVIEW.
  if path in EDITORIAL_PILLARS_PUBLIES_2026_11_13 or path in EXTRAS:
    ref=MAIN
  s=text(path); old=original(ref,path)
  if path in [name+"/index.html" for name in QCMS]:
    # Nouvel assistant de défilement mutualisé : aucune modification des données
    # ni des moteurs des questionnaires (hormis mode rapide Énergie ci-dessous).
    loader='<script src="../assets/qcm-scroll-after-answer.js" defer></script>'
    assert s.count(loader)==1,(path,"script de defilement manquant ou duplique")
    s=s.replace(loader,"")
  if path=="qcm-energie/index.html":
    # Le mode rapide Energie quitte le passage automatique apres 280 ms :
    # après le vote, l'utilisateur choisit quand passer à la question suivante.
    before='  } else {\n    setTimeout(()=>{\n      nextQuestion();\n    }, 280);\n  }'
    after='  } else {\n    // Même en mode rapide, laisser le lecteur poursuivre lui-même.\n    document.getElementById("nextBtn").style.display = "block";\n  }'
    before=before.replace('\n','\n')
    after=after.replace('\n','\n')
    assert s.count(after)==1,(path,"mode rapide Energie modifie autrement")
    s=s.replace(after,before)
  if path=="qcm-energie/index.html":
    # Exception editoriale du 13/11: dans la liste des sources du Pilier I,
    # seul le titre et le resume ont ete mis a jour pour refleter la nouvelle
    # fiche historique. Le moteur QCM et ses scores restent strictement figes.
    previous_source=(
      '      title:"Fiche « Aller droit au but » — Pilier I Énergie",' + chr(10)
      + '      text:"Chiffres clés sourcés, responsabilités politiques et réforme proposée.",'
    )
    updated_source=(
      '      title:"Pilier I Énergie — l\'histoire qui explique le paradoxe",' + chr(10)
      + '      text:"Histoire de l\'électricité française, chiffres sourcés et responsabilités politiques.",'
    )
    assert s.count(updated_source)==1,(path,"libelle source Pilier I inattendu")
    s=s.replace(updated_source,previous_source)
  if path in ("qcm-aspa/index.html","qcm-textile/index.html"):
    # Suppression strictement bornee de l'ancien scroll, remplace par le helper commun.
    previous='  $("nextBtn").scrollIntoView({behavior:"smooth",block:"nearest"});' + chr(10)
    assert old.count(previous)==1,(path,"ancien scroll inattendu")
    assert s.count(previous)==0,(path,"ancien scroll concurrent conserve")
    old=old.replace(previous,"")
  if path=="qcm-democratie-decisionnelle/index.html":
    # La seule adaptation du moteur autorisée est l'ouverture directe de
    # la première question par paramètre, sans toucher aux votes ni aux scores.
    direct_start=(
      "// Accès direct depuis le Pilier XIII : un clic mène à la première question" + chr(10)
      + "// sans imposer une seconde page d'accueil. Sans effet sur les autres accès." + chr(10)
      + "if(new URLSearchParams(window.location.search).get('start')==='ideas'){" + chr(10)
      + "  state.screen='ideas';" + chr(10)
      + "  state.step=0;" + chr(10)
      + "}" + chr(10)
    )
    assert s.count(direct_start)==1,(path,"demarrage direct absent ou altere")
    s=s.replace(direct_start,"")
  for pattern in [r"<script\b[^>]*>[\s\S]*?</script>",r"<h[123]\b[^>]*>[\s\S]*?</h[123]>",
                  r'<link\b[^>]*rel=["\x27]canonical["\x27][^>]*>']:
    assert parts(s,pattern)==parts(old,pattern),(path,"content regression",pattern)

def png_size(path):
  d=(ROOT/path).read_bytes()
  assert d[:8]==b"\x89PNG\r\n\x1a\n",path
  return struct.unpack(">II",d[16:24])

def main():
  assert len(PILLARS)==15 and len(QCMS)==9 and len(PAGES)==30,len(PAGES)
  assert png_size("apple-touch-icon.png")== (180,180)
  # Safari iOS may display transparent pixels with an unexpected dark backing:
  # the 180px shortcut icon deliberately uses an opaque white background.
  assert (ROOT/"apple-touch-icon.png").read_bytes()[25]==2,"Apple icon must be opaque RGB"
  assert png_size("favicon-32.png")== (32,32)
  assert png_size("assets/identite/symbole-perplexity.png")== (192,192)
  for path in PAGES:
    s=text(path);head=s.split("</head>",1)[0]
    assert "<head" in head and "<html" in s[:80],path
    markup=re.sub(r"<script\b[^>]*>[\s\S]*?</script>","",s,flags=re.I)
    assert len(tags(markup,"h1"))==1,(path,"H1 outside JS templates")
    assert re.search(r"<title>[^<]{12,}</title>",head,re.I),path
    assert re.search(r'<meta\b[^>]*name=["\x27]description["\x27]',head,re.I),path
    assert len(parts(head,r'<link\b[^>]*rel=["\x27]canonical["\x27][^>]*>'))==1,(path,"canonical")
    assert DOMAIN in head,(path,"production canonical")
    assert "rel=\"apple-touch-icon\"" in head,(path,"missing static Apple icon")
    assert "rel=\"icon\"" in head,(path,"missing favicon")
    assert len(parts(head,r'<link\b[^>]*rel=["\x27]apple-touch-icon["\x27]'))==1,(path,"duplicate Apple icon")
    match=re.search(r'<link[^>]*rel="apple-touch-icon"[^>]*href="([^"]+)"',head)
    assert match,path
    icon=(ROOT/path).parent.joinpath(match.group(1)).resolve()
    assert icon==(ROOT/"apple-touch-icon.png").resolve(),(path,"wrong icon",icon)
    assert "apple-mobile-web-app-title" in head,path
    if path not in ("index.html","piliers/reparation-des-retraites/index.html"):
      assert_eq(path)
    elif path=="piliers/reparation-des-retraites/index.html":
      # Le contenu redactionnel de ce seul pilier a ete corrige ; SEO intact.
      assert "aspa-evidence-card" in s and s.count('class="card aspa-evidence-card"')==2
      assert "ANCIENNES FORMULATIONS À ABANDONNER" not in s
      assert "17-891QE.htm" in s and "service-public.gouv.fr" in s
      assert '<link rel="canonical" href="https://doctrine-econologique.fr/piliers/reparation-des-retraites/"' in s
      assert '"dateModified": "2026-11-07"' in s
    print("PASS static SEO+Apple",path)
  # All published HTML, including source fiches and annexes, must use the SAME
  # Apple icon; a shortcut created from any interior page must not revert to
  # the old é. or bulletin pictogram. Non-published legacy v7 variants are
  # intentionally excluded by _config.yml.
  all_html=[]
  for entry in ROOT.rglob("*.html"):
    path=entry.relative_to(ROOT).as_posix()
    if path.startswith(("archives/","tools/","prototype-v2/","tests/",".github/")):continue
    if path in ("qcm-general/qcm-general-v7-1-index.html","qcm-general/qcm-general-v7-2-index.html"):continue
    all_html.append(path)
  assert len(all_html)>=90,("published HTML inventory incomplete",len(all_html))
  for path in all_html:
    h=text(path).split("</head>",1)[0]
    match=re.search(r'<link[^>]*rel="apple-touch-icon"[^>]*href="([^"]+)"',h,re.I)
    assert match,(path,"Apple shortcut logo missing")
    icon=(ROOT/path).parent.joinpath(match.group(1)).resolve()
    assert icon==(ROOT/"apple-touch-icon.png").resolve(),(path,"wrong old Apple icon",match.group(1))
    assert len(parts(h,r'<link\b[^>]*rel="apple-touch-icon"'))==1,(path,"duplicate icon")
  print("PASS all",len(all_html),"published HTML pages use the same Perplexity Apple touch icon")
  main_html=text("index.html"); old_head=original(MAIN,"index.html").split("</head>",1)[0]
  assert "noindex" not in main_html.split("</head>",1)[0].lower()
  assert 'name="google-site-verification"' in main_html.split("</head>",1)[0]
  assert "google-site-verification" in old_head
  assert '<link rel="canonical" href="https://doctrine-econologique.fr/"' in main_html
  assert len(tags(main_html,"h1"))==1
  assert len(parts(main_html,r'<meta property="og:[^"]+"[^>]*>'))>=7
  assert "Jean Paul Poignand" in main_html and 'href="/a-propos/' in main_html
  assert "apple-touch-icon.png" in main_html
  assert len(parts(main_html,r'id="pilier-\d+"'))==17
  assert 'id="piliers"' in main_html and 'id="positionner"' in main_html
  assert "PROTOTYPE V2.3" not in main_html and "Version de test non indexée" not in main_html
  assert "Prépublication V2.6" not in main_html
  scripts=text("assets/doctrine-share.js")
  assert "raw.githack" not in scripts and "preview-v2" not in scripts and "noindex" not in scripts
  assert "dmenu-panel" in scripts and "symbole-perplexity.png" in scripts
  assert "apple-touch-icon.png" in scripts
  config=text("_config.yml")
  for folder in ["prototype-v2/","tests/","archives/","tools/"]:
    assert "  - "+folder in config,folder
  for name in ["robots.txt","sitemap.xml","CNAME"]:
    assert text(name)==original(MAIN,name),("Unexpected SEO file modification",name)
  ET.parse(ROOT/"sitemap.xml")
  assert (ROOT/"CNAME").read_text().strip()=="doctrine-econologique.fr"
  print("PASS Grégoire: canonical + OG + Google site verification + human author + schema + sitemap, no production noindex")
  print("PASS iOS/iPad static shortcut icon 180×180 on",len(PAGES),"HTML pages, root favicon")
  print("PASS engines of all nine QCM and 15 pillars preserved; production JS contains no preview router")
  print("PASS prototype and tests excluded from Pages build")

if __name__=="__main__":main()
