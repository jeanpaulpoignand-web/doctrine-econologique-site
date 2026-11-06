#!/usr/bin/env python3
"""Guarantee V2.7 modifies only presentation on the 15 published pillars and catalogue."""
import re
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
BASE="origin/preview-v26-2026-11-07"
PILLARS=[
    "energie-souveraine","garantie-decennale","financement-public",
    "reparation-des-retraites","grand-age-ehpad","batiment-metiers-utiles",
    "econologie-culturelle","frontaliers-capital-humain","agriculture-alimentation",
    "textile-habillement-chaussure","mobilite-securite-routiere",
    "friction-monetique","democratie-decisionnelle","amortissement-dette","fraude-fiscale",
]

def unchanged(source:str, changed:str, catalogue=False):
    # Remove ONLY presentation additions made in this branch; no changes to textual content.
    body="<body class=\"piliers-index-v27\">" if catalogue else "<body class=\"pilier-v27\">"
    changed=changed.replace(body,"<body>")
    assert "<body>" in changed
    pattern=[
        r'<link rel="preconnect" href="https://fonts\.googleapis\.com">\n',
        r'<link rel="preconnect" href="https://fonts\.gstatic\.com" crossorigin>\n',
        r'<link href="https://fonts\.googleapis\.com/css2\?family=Cormorant\+Garamond[^"\n]*" rel="stylesheet">\n',
        r'<link rel="stylesheet" href="(?:\.\./){1,2}assets/pilier-charte-v27\.css">\n',
    ]
    for p in pattern:
        changed,n=re.subn(p,"",changed)
        assert n <= 1,(p,n)
    if catalogue:
        changed=changed.replace('<script src="../assets/doctrine-share.js" defer></script>\n',"")
    return source==changed

def main():
    assert len(PILLARS)==15
    names=[f"piliers/{x}/index.html" for x in PILLARS]+["piliers/index.html"]
    for path in names:
        original=subprocess.check_output(["git","show",f"{BASE}:{path}"],cwd=ROOT).decode("utf-8")
        updated=(ROOT/path).read_text(encoding="utf-8")
        assert unchanged(original,updated,path=="piliers/index.html"),f"UNAUTHORIZED CONTENT CHANGE IN {path}"
        assert updated.count('href="https://doctrine-econologique.fr/piliers/')>=1,path
        assert updated.lower().count("<h1")==1,path
        print("PASS exact original content preserved:",path)
    for name in PILLARS:
        assert (ROOT/"piliers"/name/"index.html").is_file()
    index=(ROOT/"piliers"/"index.html").read_text()
    assert "Pilier XIV · non audité" in index
    assert "Pilier XVI · en chantier" in index and "Pilier XVII · en chantier" in index
    assert index.count('class="pil"')==17
    print("SUCCESS V2.7: 15 sources preserved byte-for-byte after removal of presentation links; 2 workstreams remain clearly marked.")
if __name__=="__main__": main()
