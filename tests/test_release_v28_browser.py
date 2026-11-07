#!/usr/bin/env python3
"""V2.8 release candidate — production-origin browser acceptance incl. iPhone/iPad icon."""
from pathlib import Path
import os
from urllib.parse import urlparse, unquote
import mimetypes
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
PREFIX="/"
BASE="https://doctrine-econologique.fr/"
PILLARS=[
    "energie-souveraine","garantie-decennale","financement-public",
    "reparation-des-retraites","grand-age-ehpad","batiment-metiers-utiles",
    "econologie-culturelle","frontaliers-capital-humain","agriculture-alimentation",
    "textile-habillement-chaussure","mobilite-securite-routiere","friction-monetique",
    "democratie-decisionnelle","amortissement-dette","fraude-fiscale"
]
QCMS=["qcm-general","qcm-energie","qcm-aspa","qcm-pilier-vi",
      "qcm-textile","qcm-fraude-fiscale","qcm-immigrants-journee",
      "qcm-consigne-megots","qcm-democratie-decisionnelle"]
ART=ROOT/".test-artifacts"/"release-v28"
ART.mkdir(parents=True,exist_ok=True)

def main():
  with sync_playwright() as p:
    engine=os.getenv("BROWSER_ENGINE","chromium").lower()
    assert engine in ("chromium","webkit"),engine
    browser=(p.webkit if engine=="webkit" else p.chromium).launch(headless=True)
    for label,viewport in [("desktop",{"width":1440,"height":900}),("iphone",{"width":390,"height":844}),("iphone-small",{"width":320,"height":650}),("ipad",{"width":820,"height":1180}),("ipad-paysage",{"width":1180,"height":820})]:
      ctx=browser.new_context(viewport=viewport,device_scale_factor=1)
      ctx.route("https://fonts.googleapis.com/**",lambda route:route.abort())
      ctx.route("https://fonts.gstatic.com/**",lambda route:route.abort())
      missing=[]
      def serve(route):
        path=unquote(urlparse(route.request.url).path)
        if not path.startswith(PREFIX):return route.fulfill(status=404,body="Outside preview")
        filename=path[len(PREFIX):]
        fp=(ROOT/filename).resolve()
        if not fp.is_relative_to(ROOT) or not fp.is_file():
          missing.append(filename)
          return route.fulfill(status=404,body="Missing "+filename)
        return route.fulfill(status=200,path=str(fp),content_type=mimetypes.guess_type(str(fp))[0] or "application/octet-stream")
      ctx.route("https://doctrine-econologique.fr/**",serve)
      page=ctx.new_page()
      errors=[]
      page.on("pageerror",lambda e:errors.append(str(e)))
      page.goto(BASE+"index.html",wait_until="domcontentloaded")
      page.locator("h1").first.wait_for()
      assert page.locator("#dmenu-bar").count()==0,"Homepage should keep its own hamburger"
      assert page.locator('.site-header .brand-mark img').count()==1
      assert page.locator('.site-header .brand-mark img').evaluate("(im)=>im.naturalWidth===192")
      assert page.locator('link[rel="apple-touch-icon"]').evaluate("(a)=>new URL(a.href).pathname")=="/apple-touch-icon.png"
      assert page.locator('link[rel="canonical"]').get_attribute("href")=="https://doctrine-econologique.fr/"
      assert page.locator('meta[name="google-site-verification"]').count()==1
      assert page.locator('meta[name="robots"]').count()==0
      # Recherche globale : la categorie active ne doit jamais masquer un autre sujet pertinent.
      search=page.locator("#topic-search")
      all_topics=page.locator('[data-filter="all"]')
      finances=page.locator('[data-filter="finances"]')
      # Les filtres sont de vrais boutons tactiles, pas des etiquettes plates.
      relief=all_topics.evaluate("(el)=>{const s=getComputedStyle(el);return {height:el.getBoundingClientRect().height,shadow:s.boxShadow,texture:s.backgroundImage,transition:s.transitionDuration}}")
      assert relief["height"]>=44,(label,"cible tactile inferieure a 44 px",relief)
      assert relief["shadow"]!="none" and relief["texture"]!="none",(label,"relief/texture absents",relief)
      active_style=all_topics.evaluate("(el)=>getComputedStyle(el).backgroundColor")
      finances_style=finances.evaluate("(el)=>getComputedStyle(el).backgroundColor")
      assert active_style!=finances_style,(label,"onglet selectionne non distinct")
      finances.click()
      assert finances.get_attribute("aria-pressed")=="true"
      assert page.locator(".topic-card:visible").count()==3,(label,"filtre argent public")
      search.fill("retraite")
      assert all_topics.get_attribute("aria-pressed")=="true",(label,"recherche globale")
      assert page.locator("#dossier-4").is_visible(),(label,"retraite hors du filtre argent public")
      assert page.locator(".topic-card:visible").count()==1
      assert page.locator("#result-count").inner_text()=="1 dossier affiché"
      search.fill("ÉNERGIE")
      assert page.locator("#dossier-1").is_visible(),(label,"accent/casse")
      assert page.locator(".topic-card:visible").count()==1
      search.fill("fraude")
      assert page.locator("#dossier-15").is_visible(),(label,"autre groupe")
      search.fill("mottotalementabsent")
      assert page.locator(".topic-card:visible").count()==0,(label,"aucun resultat")
      assert page.locator("#empty").is_visible()
      page.locator('[data-filter="production"]').click()
      assert search.input_value()=="",(label,"un filtre efface la recherche")
      assert page.locator(".topic-card:visible").count()==5
      search.fill("agriculture")
      assert all_topics.get_attribute("aria-pressed")=="true"
      assert page.locator("#dossier-9").is_visible()
      search.fill("")
      assert page.locator(".topic-card:visible").count()==17,(label,"recherche effacee")
      assert page.locator("#empty").is_hidden()
      if label=="ipad-paysage":
        search.fill("retraite")
        page.locator("#explorer").scroll_into_view_if_needed()
        page.screenshot(path=str(ART/"ipad-paysage-recherche-retraite.png"),full_page=False)
        search.fill("")
      # Le panneau bleu de l'accueil doit rester parfaitement droit, y compris sur iPad paysage.
      assert page.locator(".question-board").count()==1
      assert page.locator(".question-board").evaluate("(el)=>getComputedStyle(el).transform")=="none",(label,"panneau bleu incline")

      if viewport["width"]<=700:
        toggle=page.locator("#menu-toggle")
        assert toggle.is_visible(),"Homepage hamburger missing"
        toggle.click()
        assert toggle.get_attribute("aria-expanded")=="true"
        assert page.locator('#nav-links a[href*="/piliers/index.html"]').is_visible()
        assert page.locator('#nav-links a[href*="/questionnaires/index.html"]').is_visible()
        assert page.locator('#nav-links a[href*="/qcm-democratie-decisionnelle/index.html"]').is_visible()
        assert page.locator("html").evaluate("(e)=>e.scrollWidth-e.clientWidth")<=3
        page.screenshot(path=str(ART/f"{label}-accueil-menu-ouvert.png"),full_page=False)
        page.keyboard.press("Escape")
        assert toggle.get_attribute("aria-expanded")=="false"
        toggle.click()
        page.locator('#nav-links a[href*="/piliers/index.html"]').click()
        assert page.url.startswith(BASE+"piliers/index.html"),page.url
      else:
        assert page.locator("#menu-toggle").is_hidden()
        page.goto(BASE+"piliers/index.html",wait_until="domcontentloaded")
      page.locator("#dmenu-toggle").wait_for()
      assert page.locator("a.dmenu-brand").evaluate("(a)=>a.href")==BASE+"index.html"
      assert page.locator("#dmenu-panel").is_hidden()
      assert page.locator("#dmenu-toggle").get_attribute("aria-expanded")=="false"
      page.locator("#dmenu-toggle").click()
      assert page.locator("#dmenu-panel").is_visible()
      assert page.locator("#dmenu-toggle").get_attribute("aria-expanded")=="true"
      assert page.locator("#dmenu-panel a.dmenu-link").count()==6
      assert page.locator('#dmenu-panel a[href*="/piliers/index.html"]').count()==1
      assert page.locator('#dmenu-panel a[href*="/questionnaires/index.html"]').count()==1
      assert page.locator('#dmenu-panel a[href*="/qcm-democratie-decisionnelle/index.html"]').count()==1
      page.screenshot(path=str(ART/f"{label}-17-piliers-menu-ouvert.png"),full_page=False)
      page.keyboard.press("Escape")
      assert page.locator("#dmenu-panel").is_hidden()
      assert page.locator("#dmenu-toggle").get_attribute("aria-expanded")=="false"
      assert page.locator("#dmenu-toggle").evaluate("(el)=>document.activeElement===el")
      page.locator("#dmenu-toggle").click()
      page.locator('#dmenu-panel a[href*="/questionnaires/index.html"]').click()
      assert page.url.startswith(BASE+"questionnaires/index.html"),page.url
      page.locator("#dmenu-toggle").wait_for()
      page.locator("#dmenu-toggle").click()
      page.locator('#dmenu-panel a[href*="/qcm-democratie-decisionnelle/index.html"]').click()
      assert page.url.startswith(BASE+"qcm-democratie-decisionnelle/index.html"),page.url
      page.locator("#dmenu-toggle").wait_for()
      page.locator("#dmenu-toggle").click()
      page.screenshot(path=str(ART/f"{label}-bulletin-menu-ouvert.png"),full_page=False)
      page.locator("#dmenu-close").count()==0 # class name only
      page.locator("#dmenu-panel button.dmenu-close").click()
      assert page.locator("#dmenu-panel").is_hidden()
      # Coverage: the same accessible menu appears on every QCM + every published pillar.
      for loc in ["questionnaires/index.html","piliers/index.html"] + [name+"/index.html" for name in QCMS] + ["piliers/"+name+"/index.html" for name in PILLARS]:
        page.goto(BASE+loc,wait_until="domcontentloaded",timeout=30000)
        page.locator("#dmenu-toggle").wait_for()
        assert page.locator("#dmenu-toggle").count()==1,(label,loc,"duplicate or missing menu")
        # Static iPhone/iPad shortcut icon — must resolve to the same root PNG.
        icon=page.locator('link[rel="apple-touch-icon"]')
        assert icon.count()==1,(label,loc,"touch icon count")
        assert icon.evaluate("(a)=>new URL(a.href).pathname")=="/apple-touch-icon.png",(label,loc,"wrong Apple shortcut icon")
        assert page.locator('meta[name="apple-mobile-web-app-title"]').count()==1,(label,loc,"home-screen label")
        img=page.locator("#dmenu-bar img")
        assert img.count()==1,(label,loc,"Perplexity brand")
        assert img.evaluate("(a)=>a.naturalWidth===192"),(label,loc,"original logo missing")

        assert page.locator("a.dmenu-brand").evaluate("(a)=>a.href")==BASE+"index.html"
        if loc=="piliers/reparation-des-retraites/index.html":
          # Regles de lecture : les deux colonnes sont de vraies cartes autonomes.
          evidence=page.locator(".aspa-evidence-card")
          assert evidence.count()==2,(label,"deux encadres ASPA attendus")
          assert page.locator("#aspa-faits").inner_text()=="Ce qui est établi"
          assert page.locator(".aspa-national-hero").is_visible()
          assert "5,182 milliards d’euros" in page.locator(".aspa-national-hero").inner_text()
          assert "4,868 Md€" in page.locator(".aspa-national-grid").inner_text()
          assert "108,7 M€" in page.locator(".aspa-national-grid").inner_text()
          accord=page.locator(".aspa-1968-cards")
          assert accord.locator(".card").count()==3,(label,"resume de l'accord incomplet")
          assert "65 ans" in accord.inner_text()
          assert "jamais cotisé" in accord.inner_text()
          assert "n’est pas attribuée simplement à l’arrivée en France" in accord.inner_text()
          assert accord.locator(".card p strong").first.evaluate("(el)=>getComputedStyle(el).display")=="inline",(label,"gras non inline")
          assert page.locator("a[href='../../fiches/pilier-04-aller-droit-au-but.pdf']").count()==1
          if label in ("iphone","ipad-paysage"):
            page.locator(".aspa-national").screenshot(path=str(ART/f"{label}-pilier4-budget-national.png"))
            accord.screenshot(path=str(ART/f"{label}-pilier4-accord-1968.png"))
          assert page.locator("#aspa-manques").inner_text()=="Ce qu’il reste à mesurer"
          assert evidence.nth(0).locator("p").count()==3
          assert evidence.nth(1).locator("p").count()==3
          assert page.locator(".aspa-evidence-summary").is_visible()
          assert "ANCIENNES FORMULATIONS À ABANDONNER" not in page.locator("main").inner_text()
          assert "Les ressortissants algériens relèvent d’un régime de séjour [HYPOTHÈSE]" not in page.locator("main").inner_text()
          # Chaque paragraphe doit rester dans son encadre, sans texte orphelin.
          assert evidence.evaluate_all("""(cards)=>cards.every(card=>[...card.querySelectorAll('p')].every(p=>{
             const a=card.getBoundingClientRect(),b=p.getBoundingClientRect();
             return b.left>=a.left-1 && b.right<=a.right+1 && b.top>=a.top-1 && b.bottom<=a.bottom+1
          }))"""),(label,"paragraphe hors de son encadre")
          xs=evidence.evaluate_all("(cards)=>cards.map(c=>Math.round(c.getBoundingClientRect().left))")
          if viewport["width"]<=700:
            assert abs(xs[0]-xs[1])<=2,(label,"cartes non empilees en mobile")
          else:
            assert abs(xs[0]-xs[1])>=20,(label,"colonnes non distinctes")
          if label in ("iphone","ipad-paysage"):
            page.locator(".aspa-evidence").screenshot(path=str(ART/f"{label}-pilier4-encadres.png"))
        if loc!="qcm-consigne-megots/index.html":
          assert "noindex" not in " ".join([v or "" for v in page.locator('meta[name="robots"]').evaluate_all("(els)=>els.map(e=>e.content)")]),(label,loc,"unexpected noindex")
        if viewport["width"]<=820:
          spill=page.evaluate("document.documentElement.scrollWidth-document.documentElement.clientWidth")
          assert spill<=3,(label,loc,"horizontal overflow",spill)
      assert not missing,(label,"missing assets",sorted(set(missing))[:10])
      assert not errors,(label,"JS error",errors[:8])
      print("PASS",label,"production links, menu, Perplexity icon on 27 pages, SEO, no JS errors or overflow")
      ctx.close()
    browser.close()

if __name__=="__main__":main()
