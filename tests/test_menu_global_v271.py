#!/usr/bin/env python3
"""Browser acceptance tests of the global hamburger menu on prepublication V2.7.1."""
from pathlib import Path
from urllib.parse import urlparse, unquote
import mimetypes
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
PREFIX="/jeanpaulpoignand-web/doctrine-econologique-site/preview-v27-menu-2026-11-07/"
BASE="https://raw.githack.com"+PREFIX
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
ART=ROOT/".test-artifacts"/"preview-v271-menu"
ART.mkdir(parents=True,exist_ok=True)

def main():
  with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    for label,viewport in [("desktop",{"width":1440,"height":900}),("iphone",{"width":390,"height":844}),("iphone-small",{"width":320,"height":650})]:
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
      ctx.route("https://raw.githack.com/**",serve)
      page=ctx.new_page()
      errors=[]
      page.on("pageerror",lambda e:errors.append(str(e)))
      page.goto(BASE+"index.html",wait_until="domcontentloaded")
      page.locator("#preview-v26-notice").wait_for()
      assert page.locator("#dmenu-bar").count()==0,"Homepage should keep its own hamburger"
      if label!="desktop":
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
      assert page.locator("a.dmenu-brand").get_attribute("href")==BASE+"index.html"
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
        assert page.locator("a.dmenu-brand").get_attribute("href")==BASE+"index.html"
        assert "noindex" in page.locator('meta[name="robots"]').last.get_attribute("content"),(label,loc,"robots preview")
        if label!="desktop":
          spill=page.evaluate("document.documentElement.scrollWidth-document.documentElement.clientWidth")
          assert spill<=3,(label,loc,"horizontal overflow",spill)
      assert not missing,(label,"missing assets",sorted(set(missing))[:10])
      assert not errors,(label,"JS error",errors[:8])
      print("PASS",label,"homepage burger; menu + 26 pages; links, ESC, click, 0 console errors/overflows")
      ctx.close()
    browser.close()

if __name__=="__main__":main()
