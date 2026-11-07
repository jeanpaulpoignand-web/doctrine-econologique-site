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

def button_visible_in_viewport(page,selector,label):
  page.wait_for_function("""selector=>{
    const el=document.querySelector(selector);
    if(!el || el.disabled) return false;
    const r=el.getBoundingClientRect(),h=window.visualViewport?.height||window.innerHeight;
    return r.top>=-3 && r.bottom<=h+4 && r.width>0 && r.height>0;
  }""",arg=selector,timeout=7000)
  assert page.locator(selector).is_visible(),(label,selector,"bouton non visible")


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
      # L'encart de transparence doit apparaitre haut dans l'accueil, sourcer
      # correctement l'article 15 et rester lisible sur iPhone/iPad.
      principle=page.locator("#transparence-citoyenne")
      assert principle.count()==1 and principle.is_visible(),(label,"principe de transparence absent")
      assert principle.evaluate("(el)=>el.previousElementSibling?.classList.contains('stats')"),(label,"encart mal place")
      assert principle.evaluate("(el)=>el.nextElementSibling?.id==='decouverte'"),(label,"decouverte deplacee")
      statement="La transparence démocratique ne se mesure pas au volume de documents que l'État publie, mais à la capacité réelle de chaque citoyen à comprendre, vérifier et suivre l'utilisation de l'argent public, sans devoir y consacrer des heures."
      assert principle.locator("blockquote").inner_text()==statement,(label,"principe modifie")
      article="La société a le droit de demander compte à tout agent public de son administration."
      assert article in principle.locator(".accountability-law-quote").inner_text(),(label,"article 15 altere")
      source=principle.locator("a.accountability-source")
      assert source.get_attribute("href")=="https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000006527442"
      assert source.get_attribute("rel")=="noopener noreferrer"
      assert principle.locator("a.accountability-pillar").get_attribute("href")=="/piliers/democratie-decisionnelle/"
      assert principle.evaluate("(el)=>{const r=el.getBoundingClientRect();return r.left>=-1&&r.right<=innerWidth+1;}"),(label,"encart deborde")
      assert page.locator("html").evaluate("(e)=>e.scrollWidth-e.clientWidth")<=3,(label,"largeur de page debordee")
      if label in ("desktop","iphone","iphone-small","ipad-paysage"):
        principle.screenshot(path=str(ART/f"{label}-encart-article15.png"))
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
      # Test de régression pour le défaut réel remonté sur iPhone : ASPA donnait 0.
      search.fill("ASPA")
      suggestions=page.locator("#search-suggestions")
      assert page.locator("#dossier-4").is_visible(),(label,"ASPA doit afficher le pilier IV")
      assert page.locator(".topic-card:visible").count()==1,(label,"ASPA devrait retourner un seul dossier")
      assert page.locator("#result-count").inner_text()=="1 dossier affiché"
      assert suggestions.is_visible(),(label,"acces direct invisible sous le champ")
      assert suggestions.locator(".search-hit").count()==1,(label,"acces direct unique ASPA")
      assert suggestions.locator(".search-hit-main").get_attribute("href")=="/piliers/reparation-des-retraites/"
      assert suggestions.locator(".search-hit-quiz").get_attribute("href")=="/qcm-aspa/"
      assert suggestions.locator(".search-hit-main").evaluate("(el)=>el.getBoundingClientRect().height")>=44,(label,"resultat difficile a toucher")
      assert all_topics.get_attribute("aria-pressed")=="true"
      if label in ("iphone","ipad-paysage"):
        suggestions.screenshot(path=str(ART/f"{label}-recherche-aspa-resultat.png"))
      # Accents, recherches a plusieurs mots, termes du dossier et URL de QCM.
      for word,expected in [
        ("aspa",4),("A SPA",4),("allocation solidarité personnes âgées",4),
        ("minimum vieillesse",4),("accord franco-algérien",4),("QCM ASPA",4),
        ("ZFE",11),("paiement carte",12),("EHPAD",5),("dette",14)
      ]:
        search.fill(word)
        assert page.locator(f"#dossier-{expected}").is_visible(),(label,word,"aucun resultat")
        assert suggestions.is_visible(),(label,word,"suggestion manquante")
      search.fill("ÉNERGIE")
      assert page.locator("#dossier-1").is_visible(),(label,"accent/casse")
      assert page.locator(".topic-card:visible").count()==1
      search.fill("fraude")
      assert page.locator("#dossier-15").is_visible(),(label,"autre groupe")
      search.fill("mottotalementabsent")
      assert page.locator(".topic-card:visible").count()==0,(label,"aucun resultat")
      assert page.locator("#empty").is_visible()
      assert "Aucun dossier trouvé" in suggestions.inner_text(),(label,"retour de recherche vide peu clair")
      page.locator('[data-filter="production"]').click()
      assert search.input_value()=="",(label,"un filtre efface la recherche")
      assert page.locator(".topic-card:visible").count()==5
      search.fill("agriculture")
      assert all_topics.get_attribute("aria-pressed")=="true"
      assert page.locator("#dossier-9").is_visible()
      search.fill("")
      assert page.locator(".topic-card:visible").count()==17,(label,"recherche effacee")
      assert page.locator("#empty").is_hidden()
      assert suggestions.is_hidden(),(label,"suggestions pas effacees")
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
          assert "dix ans de titre de séjour autorisant à travailler ne lui est pas opposable" in accord.inner_text()
          assert "pas un délai d’attente de neuf mois" in accord.inner_text()
          assert "mois suivant le dépôt de la demande" in accord.inner_text()
          assert accord.locator(".card p strong").first.evaluate("(el)=>getComputedStyle(el).display")=="inline",(label,"gras non inline")
          assert page.locator("a[href='../../fiches/pilier-04-aller-droit-au-but.pdf']").count()==1
          if label in ("iphone","ipad-paysage"):
            page.locator(".aspa-national").screenshot(path=str(ART/f"{label}-pilier4-budget-national.png"))
            accord.screenshot(path=str(ART/f"{label}-pilier4-accord-1968.png"))
          assert page.locator("#aspa-manques").inner_text()=="Ce qu’il reste à mesurer"
          assert evidence.nth(0).locator("p").count()==3
          assert evidence.nth(1).locator("p").count()==3
          assert page.locator(".aspa-evidence-summary").is_visible()
          integration=page.locator(".aspa-integration")
          assert integration.count()==1 and integration.is_visible(),(label,"section integration absente")
          assert integration.locator(".aspa-integration-item").count()==3,(label,"trois exceptions attendues")
          assert "6 709 ressortissants algériens" in integration.inner_text()
          assert "26 janvier 2024" in integration.inner_text()
          assert "ne s’appliquent pas aux ressortissants algériens" in integration.inner_text()
          assert "facultative pour les ressortissants algériens" in integration.inner_text()
          assert "Cette exemption de signature ne les dispense pas du respect des lois françaises" in integration.inner_text()
          if label in ("iphone","ipad-paysage"):
            integration.screenshot(path=str(ART/f"{label}-pilier4-integration.png"))
          vote=page.locator(".aspa-vote")
          assert vote.count()==1 and vote.is_visible(),(label,"vote parlementaire absent")
          assert "30 octobre 2025" in vote.inner_text()
          assert "Gabriel Attal" in vote.inner_text()
          assert "185" in vote.inner_text() and "184" in vote.inner_text() and "5" in vote.inner_text()
          assert "résolution non contraignante" in vote.inner_text()
          rapport=page.locator(".aspa-rapport")
          assert rapport.count()==1 and rapport.is_visible(),(label,"rapport Rodwell non visible")
          assert "2 milliards d’euros par an" in rapport.inner_text()
          assert "200 à 300 M€ / an" in rapport.inner_text()
          assert "1,5 à 2 Md€ / an" in rapport.inner_text()
          assert "Mathieu Lefèvre" in rapport.inner_text() and "Charles Rodwell" in rapport.inner_text()
          assert "ne peut pas être fiabilisé rigoureusement" in rapport.inner_text()
          assert "Philippe Brun" in rapport.inner_text()
          assert "ni avec les sommes effectivement versées aux allocataires de nationalité algérienne" in rapport.inner_text()
          if label in ("iphone","ipad-paysage"):
            rapport.screenshot(path=str(ART/f"{label}-pilier4-rapport-1963.png"))
          assert vote.locator('a[href="https://www.assemblee-nationale.fr/dyn/17/scrutins/3260"]').count()==2
          if label in ("iphone","ipad-paysage"):
            vote.screenshot(path=str(ART/f"{label}-pilier4-vote-3260.png"))

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
      # QCM général, question 6 illustrée par la capture iPhone : après
      # avoir voté, faire apparaître « Question suivante » sans l'activer.
      # Vérifier les deux modes, y compris l'explication pédagogique.
      for mode in ("fast","learn"):
        page.goto(BASE+f"qcm-general/index.html?mode={mode}&q=6",wait_until="domcontentloaded",timeout=30000)
        answer=page.locator("#answers button.answer").first
        answer.wait_for()
        assert page.locator("#stepLabel").inner_text()=="Question 6 / 10",(label,mode,"lien direct mal lu")
        assert page.locator("#nextBtn").is_disabled(),(label,mode,"suivant activé sans choix")
        answer.click()
        next_button=page.locator("#nextBtn")
        assert next_button.is_enabled(),(label,mode,"suivant doit être activé")
        # Un défilement doux peut prendre quelques centaines de ms.
        page.wait_for_function("""() => {
          const el=document.getElementById('nextBtn'),r=el.getBoundingClientRect();
          return !el.disabled && r.top>=-1 && r.bottom<=window.innerHeight+4;
        }""",timeout=7000)
        assert page.locator("#stepLabel").inner_text()=="Question 6 / 10",(label,mode,"passage automatique non demandé")
        assert page.locator("#answers .answer.selected").count()==1,(label,mode,"choix perdu")
        if mode=="learn":
          assert page.locator("#explanationBox").is_visible(),(label,"explication pédagogique disparue")
        if label in ("iphone","iphone-small","ipad-paysage") and mode=="fast":
          page.screenshot(path=str(ART/f"{label}-qcm-general-apres-vote-scroll.png"),full_page=False)
        next_button.click()
        assert page.locator("#stepLabel").inner_text()=="Question 7 / 10",(label,mode,"suivant ne fonctionne plus")
        assert page.locator("#nextBtn").is_disabled(),(label,mode,"question suivante activée avant vote")
      # Tout questionnaire doit présenter son action suivante après le vote,
      # sans passer à la question suivante à la place de l'utilisateur.
      if label in ("desktop","iphone","ipad-paysage"):
        cases=[
          ("qcm-general","normal"),
          ("qcm-general","pedagogique"),
          ("qcm-energie","rapide"),
          ("qcm-energie","approfondi"),
          ("qcm-aspa","rapide"),
          ("qcm-aspa","lente"),
          ("qcm-pilier-vi","lente"),
          ("qcm-textile","lente"),
          ("qcm-fraude-fiscale","long"),
          ("qcm-immigrants-journee","normal"),
          ("qcm-consigne-megots","normal"),
          ("qcm-democratie-decisionnelle","normal")
        ]
        for slug,mode in cases:
          page.goto(BASE+slug+"/index.html",wait_until="domcontentloaded")
          assert page.locator('script[src="../assets/qcm-scroll-after-answer.js"]').count()==1,(label,slug,"assistant de défilement non charge")
          if slug=="qcm-general":
            page.locator("#learnModeBtn" if mode=="pedagogique" else "#fastModeBtn").click()
            assert "Question 1 / 10" in page.locator("#stepLabel").inner_text()
            page.locator("#answers button.answer").first.click()
            button_visible_in_viewport(page,"#nextBtn",(label,slug,mode))
            assert page.locator("#stepLabel").inner_text()=="Question 1 / 10"
            assert page.locator("#answers .answer.selected").count()==1
            if mode=="pedagogique":
              assert page.locator("#explanationBox").is_visible(),(label,"le mode pedagogique n'affiche pas d'explication")
            page.locator("#nextBtn").click()
            assert page.locator("#stepLabel").inner_text()=="Question 2 / 10"
          elif slug=="qcm-energie":
            if mode=="approfondi":
              page.locator('button[onclick="showBriefing()"]').click()
              page.locator('button[onclick="startQuiz(\'approfondi\')"]').click()
            else:
              page.locator('button[onclick="startQuiz(\'rapide\')"]').click()
            page.locator("#answers button").first.click()
            button_visible_in_viewport(page,"#nextBtn",(label,slug,mode))
            assert "Question 1 /" in page.locator("#progressText").inner_text()
            if mode=="approfondi":
              assert page.locator("#explain").is_visible(),(label,"explication approfondie absente")
            else:
              page.wait_for_timeout(380)
              assert "Question 1 /" in page.locator("#progressText").inner_text(),(label,"passage automatique en mode rapide")
            page.locator("#nextBtn").click()
            assert "Question 2 /" in page.locator("#progressText").inner_text()
          elif slug in ("qcm-aspa","qcm-textile"):
            page.locator('button[onclick="demarrer(\''+mode+'\')"]').click()
            page.locator("#qbody button.opt").first.click()
            button_visible_in_viewport(page,"#nextBtn",(label,slug,mode))
            assert page.locator("#nextBtn").is_enabled()
            assert "Question 1 /" in page.locator("#progTxt").inner_text()
            page.locator("#nextBtn").click()
            assert "Question 2 /" in page.locator("#progTxt").inner_text()
          elif slug=="qcm-pilier-vi":
            page.locator('button[onclick="demarrer(\'lente\')"]').click()
            page.locator("#qbody button.opt").first.click()
            button_visible_in_viewport(page,"#validateBtn",(label,slug,"valider"))
            assert page.locator("#validateBtn").is_enabled()
            page.locator("#validateBtn").click()
            button_visible_in_viewport(page,"#nextBtn",(label,slug,"suivant"))
            assert page.locator("#fb").is_visible()
            page.locator("#nextBtn").click()
            assert page.locator("#validateBtn").is_disabled(),(label,slug,"nouvelle question non reinitalisee")
          elif slug=="qcm-fraude-fiscale":
            page.locator("#longModeBtn").click()
            page.locator("#answers button.answer-button").first.click()
            button_visible_in_viewport(page,"#nextBtn",(label,slug,mode))
            assert page.locator("#answers .selected").count()==1
            assert page.locator("#questionCounter").inner_text().startswith("Question 1")
            page.locator("#nextBtn").click()
            assert page.locator("#questionCounter").inner_text().startswith("Question 2")
          elif slug=="qcm-immigrants-journee":
            page.locator("#answers button.answer").first.click()
            button_visible_in_viewport(page,"#next",(label,slug,mode))
            assert page.locator("#qnum").inner_text().startswith("Question 1")
            page.locator("#next").click()
            assert page.locator("#qnum").inner_text().startswith("Question 2")
          elif slug=="qcm-consigne-megots":
            page.locator("#startBtn").click()
            for marker_num in (1,2):
              page.locator("#landmarkAnswers button.answer").first.click()
              button_visible_in_viewport(page,"#landmarkNextBtn",(label,slug,"repere "+str(marker_num)))
              page.locator("#landmarkNextBtn").click()
            page.locator("#answers button.answer").first.click()
            button_visible_in_viewport(page,"#nextBtn",(label,slug,mode))
            assert page.locator("#counter").inner_text().startswith("Question 1")
            page.locator("#nextBtn").click()
            assert page.locator("#counter").inner_text().startswith("Question 2")
          elif slug=="qcm-democratie-decisionnelle":
            page.locator('button[onclick="app.go(\'ideas\')"]').click()
            page.locator("#no-opinion").click()
            button_visible_in_viewport(page,"#next-question",(label,slug,"sans avis"))
            assert page.locator("#no-opinion").get_attribute("aria-pressed")=="true"
            page.locator("#next-question").click()
            page.locator("#answer-slider").fill("75")
            button_visible_in_viewport(page,"#next-question",(label,slug,"curseur"))
            assert page.locator("#next-question").is_enabled()
          if label=="iphone":
            page.screenshot(path=str(ART/f"iphone-vote-scroll-{slug}-{mode}.png"),full_page=False)
      assert not missing,(label,"missing assets",sorted(set(missing))[:10])
      assert not errors,(label,"JS error",errors[:8])
      print("PASS",label,"production links, menu, Perplexity icon on 27 pages, SEO, no JS errors or overflow")
      ctx.close()
    browser.close()

if __name__=="__main__":main()
