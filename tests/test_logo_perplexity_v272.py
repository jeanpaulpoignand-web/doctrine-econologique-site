#!/usr/bin/env python3
"""V2.7.2: original Perplexity logo appears in site header, global hamburger and favicon.
Runs the same preview navigation tests on desktop and iPhone widths, no site deployment."""
from pathlib import Path
from urllib.parse import urlparse,unquote
import mimetypes
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
PREFIX="/jeanpaulpoignand-web/doctrine-econologique-site/preview-v27-logo-2026-11-07/"
BASE="https://raw.githack.com"+PREFIX
LOGO="assets/identite/symbole-perplexity.png"
ART=ROOT/".test-artifacts"/"preview-v272-logo"
ART.mkdir(parents=True,exist_ok=True)
PILLARS=[
"energie-souveraine","garantie-decennale","financement-public",
"reparation-des-retraites","grand-age-ehpad","batiment-metiers-utiles",
"econologie-culturelle","frontaliers-capital-humain","agriculture-alimentation",
"textile-habillement-chaussure","mobilite-securite-routiere","friction-monetique",
"democratie-decisionnelle","amortissement-dette","fraude-fiscale"
]
QCMS=["qcm-general","qcm-energie","qcm-aspa","qcm-pilier-vi","qcm-textile",
"qcm-fraude-fiscale","qcm-immigrants-journee","qcm-consigne-megots",
"qcm-democratie-decisionnelle"]

def main():
  assert (ROOT/LOGO).is_file() and (ROOT/LOGO).stat().st_size>2500
  with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    for device,width,height in [("desktop",1440,900),("iphone",390,844),("iphone-small",320,650)]:
      ctx=browser.new_context(viewport={"width":width,"height":height},device_scale_factor=1)
      ctx.route("https://fonts.googleapis.com/**",lambda route:route.abort())
      ctx.route("https://fonts.gstatic.com/**",lambda route:route.abort())
      missing=[]
      def serve(route):
        path=unquote(urlparse(route.request.url).path)
        if not path.startswith(PREFIX):return route.fulfill(status=404,body="Outside preview")
        item=path[len(PREFIX):]
        file=(ROOT/item).resolve()
        if not file.is_relative_to(ROOT) or not file.is_file():
          missing.append(item)
          return route.fulfill(status=404,body="Missing "+item)
        return route.fulfill(status=200,path=str(file),content_type=mimetypes.guess_type(str(file))[0] or "application/octet-stream")
      ctx.route("https://raw.githack.com/**",serve)
      page=ctx.new_page()
      errors=[]
      page.on("pageerror",lambda exc: errors.append(str(exc)))
      paths=["index.html","piliers/index.html","questionnaires/index.html"]+[f"piliers/{v}/index.html" for v in PILLARS]+[f"{v}/index.html" for v in QCMS]
      for route in paths:
        page.goto(BASE+route,wait_until="domcontentloaded",timeout=30000)
        page.locator("#preview-v26-notice").wait_for()
        selector=".site-header .brand-mark.dlogo-mounted img" if route=="index.html" else "#dmenu-bar .dmenu-brandmark.dlogo-mounted img"
        icon=page.locator(selector)
        icon.wait_for()
        icon.evaluate("(el)=>el.decode()")
        assert icon.get_attribute("src")==BASE+LOGO,(device,route,"logo source")
        assert icon.evaluate("(el)=>el.naturalWidth===192 && el.naturalHeight===192"),(device,route,"logo pixels")
        assert page.locator('link[rel="icon"]').count()==1,(device,route,"favicon")
        assert page.locator('link[rel="icon"]').get_attribute("href")==BASE+LOGO
        assert page.locator('link[rel="apple-touch-icon"]').count()==1
        assert page.locator('link[href*="logo-perplexity-v272.css"]').count()==1
        assert page.locator("body").count()==1
        assert "noindex" in page.locator('meta[name="robots"]').last.get_attribute("content")
        if route=="index.html":
          assert page.locator("#dmenu-toggle").count()==0
          if width<=700:
            page.locator("#menu-toggle").click()
            assert page.locator("#menu-toggle").get_attribute("aria-expanded")=="true"
            page.screenshot(path=str(ART/f"{device}-accueil-logo-menu.png"),full_page=False)
            page.keyboard.press("Escape")
        else:
          assert page.locator("#dmenu-toggle").count()==1
        if width<=700:
          overflow=page.evaluate("document.documentElement.scrollWidth-document.documentElement.clientWidth")
          assert overflow<=3,(device,route,"overflow",overflow)
        if route in ["piliers/index.html","piliers/energie-souveraine/index.html","qcm-democratie-decisionnelle/index.html"]:
          page.screenshot(path=str(ART/f"{device}-{route.replace('/','-').replace('.html','')}-logo.png"),full_page=False)
      assert not missing,(device,"missing",sorted(set(missing)))
      assert not errors,(device,"javascript errors",errors[:8])
      print("PASS",device,len(paths),"pages with original Perplexity logo + favicon + navigation, no errors")
      ctx.close()
    browser.close()

if __name__=="__main__":main()
