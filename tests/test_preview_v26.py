#!/usr/bin/env python3
"""V2.6 navigation of the actual preview file structure, using a mock CDN origin."""
from pathlib import Path
from urllib.parse import urlparse, unquote
import json, mimetypes
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
PREFIX="/jeanpaulpoignand-web/doctrine-econologique-site/preview-v26-2026-11-07/"
BASE="https://raw.githack.com"+PREFIX
QCMS=["qcm-general","qcm-energie","qcm-aspa","qcm-pilier-vi","qcm-textile","qcm-fraude-fiscale","qcm-immigrants-journee","qcm-consigne-megots","qcm-democratie-decisionnelle"]
ART=ROOT/".test-artifacts"/"preview-v26"
ART.mkdir(parents=True,exist_ok=True)

def main():
    failures=[]
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        for kind,width,height in [("desktop",1440,900),("mobile",390,844)]:
            ctx=browser.new_context(viewport={"width":width,"height":height},device_scale_factor=1)
            ctx.route("https://fonts.googleapis.com/**",lambda route:route.abort())
            ctx.route("https://fonts.gstatic.com/**",lambda route:route.abort())
            missing=[]
            def serve(route):
                u=urlparse(route.request.url)
                path=unquote(u.path)
                if not path.startswith(PREFIX):
                    return route.fulfill(status=404,body="Outside preview")
                rel=path[len(PREFIX):]
                fp=(ROOT/rel).resolve()
                if not fp.is_relative_to(ROOT) or not fp.is_file():
                    missing.append(rel)
                    return route.fulfill(status=404,body="Missing "+rel)
                typ=mimetypes.guess_type(str(fp))[0] or "application/octet-stream"
                return route.fulfill(status=200,path=str(fp),content_type=typ)
            ctx.route("https://raw.githack.com/**",serve)
            page=ctx.new_page()
            errors=[]
            page.on("pageerror",lambda e:errors.append(str(e)))
            resp=page.goto(BASE+"index.html",wait_until="domcontentloaded",timeout=30000)
            page.locator("#preview-v26-notice").wait_for()
            assert resp.status==200,resp.status
            assert page.locator("h1").count()==1
            assert "noindex" in page.locator('meta[name="robots"]').last.get_attribute("content")
            for q in QCMS:
                n=page.locator('a[href*="/'+q+'/index.html"]').count()
                assert n>0,(kind,"Landing misses",q)
            assert page.locator('a[href*="/questionnaires/index.html"]').count()>0
            page.screenshot(path=str(ART/f"{kind}-accueil.png"),full_page=True)
            # Real browser link click, not just static URL inspection
            page.locator('a[href*="/qcm-energie/index.html"]:visible').first.click()
            assert page.url.startswith(BASE+"qcm-energie/index.html"),page.url
            page.locator("#preview-v26-notice a").click()
            assert page.url.startswith(BASE+"index.html"),page.url
            page.locator('a[href*="/questionnaires/index.html"]:visible').first.click()
            assert page.url.startswith(BASE+"questionnaires/index.html"),page.url
            for q in QCMS:
                assert page.locator('a[href*="/'+q+'/index.html"]').count()>0,(kind,"Directory misses",q)
            page.screenshot(path=str(ART/f"{kind}-catalogue.png"),full_page=True)
            for q in QCMS:
                page.goto(BASE+q+"/index.html",wait_until="domcontentloaded",timeout=30000)
                page.locator("#preview-v26-notice").wait_for()
                assert page.title(),q
                assert "noindex" in page.locator('meta[name="robots"]').last.get_attribute("content"),q
                spill=page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
                if spill>3: failures.append((kind,q,"horizontal-overflow",spill))
                if q in ("qcm-general","qcm-democratie-decisionnelle","qcm-energie"):
                    page.screenshot(path=str(ART/f"{kind}-{q}.png"),full_page=True)
            assert not errors,(kind,"JavaScript exceptions",errors[:5])
            assert not missing,(kind,"missing resources",sorted(set(missing))[:15])
            ctx.close()
            print("PASS",kind,"landing -> QCM -> landing -> directory -> 9 QCM; noindex, links, assets, JS")
        browser.close()
    assert not failures,failures
    (ART/"result.json").write_text(json.dumps({"preview":BASE+"index.html","qcm_count":len(QCMS),"results":"PASS","tested":["desktop 1440x900","mobile 390x844"],"screenshots":"local Chromium preview origin simulation"},ensure_ascii=False,indent=2))
    print("SUCCESS — V2.6 navigation, 9 QCM, local mirror preview.")
if __name__=="__main__":main()
