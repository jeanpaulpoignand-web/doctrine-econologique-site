#!/usr/bin/env python3
"""V2.8.3 tactile depth: protect selected answer feedback and the General radio label gap.
Tests real styles on the nine QCM in a Chromium-controlled GitHub preview mirror.
"""
from pathlib import Path
from urllib.parse import unquote,urlparse
import json,mimetypes,subprocess
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
PREFIX="/jeanpaulpoignand-web/doctrine-econologique-site/preview-v283-qcm-relief-2026-11-07/"
BASE="https://raw.githack.com"+PREFIX
OUT=ROOT/".test-artifacts"/"qcm-relief-v283"
OUT.mkdir(parents=True,exist_ok=True)
QCMS=["qcm-general","qcm-energie","qcm-aspa","qcm-pilier-vi","qcm-textile",
      "qcm-fraude-fiscale","qcm-immigrants-journee","qcm-consigne-megots",
      "qcm-democratie-decisionnelle"]
STYLES=["assets/qcm-charte-v24.css","assets/qcm-charte-v24-classic.css",
        "assets/qcm-charte-v24-special.css","assets/bulletin-citoyen-v25.css"]

def static_check():
    # This change is only CSS. All question texts, matrix data and JS stay exactly as main.
    for slug in QCMS:
        path=f"{slug}/index.html"
        old=subprocess.check_output(["git","show",f"origin/main:{path}"],cwd=ROOT)
        new=(ROOT/path).read_bytes()
        assert new==old,f"NOT ALLOWED: HTML/JS changed: {path}"
    for path in STYLES:
        assert "V2.8.3" in (ROOT/path).read_text(encoding="utf8"),path

def main():
    static_check()
    with sync_playwright() as p:
      browser=p.chromium.launch(headless=True)
      for label,w,h in [("iphone",390,844),("ipad",820,1180),("desktop",1440,900)]:
        ctx=browser.new_context(viewport={"width":w,"height":h},device_scale_factor=1)
        ctx.route("https://fonts.googleapis.com/**",lambda route:route.abort())
        ctx.route("https://fonts.gstatic.com/**",lambda route:route.abort())
        missing=[]
        def serve(route):
          path=unquote(urlparse(route.request.url).path)
          if not path.startswith(PREFIX):return route.fulfill(status=404,body="Outside preview")
          rel=path[len(PREFIX):];fp=(ROOT/rel).resolve()
          if not fp.is_relative_to(ROOT) or not fp.is_file():
            missing.append(rel);return route.fulfill(status=404,body="Missing "+rel)
          return route.fulfill(status=200,path=str(fp),content_type=mimetypes.guess_type(str(fp))[0] or "application/octet-stream")
        ctx.route("https://raw.githack.com/**",serve)
        page=ctx.new_page()
        errors=[]
        page.on("pageerror",lambda err:errors.append(str(err)))

        def visit(slug):
          page.goto(BASE+slug+"/index.html",wait_until="domcontentloaded",timeout=30000)
          page.locator("#preview-v28-banner").wait_for()
          assert page.evaluate("document.documentElement.scrollWidth-document.documentElement.clientWidth")<=3,(label,slug,"horizontal overflow")

        def depth(selector):
          el=page.locator(selector).first
          el.wait_for(state="visible",timeout=8000)
          return el.evaluate("""e=>({
              paddingLeft:parseFloat(getComputedStyle(e).paddingLeft),
              shadow:getComputedStyle(e).boxShadow,
              animation:getComputedStyle(e).animationName,
              bg:getComputedStyle(e).backgroundImage,
              border:getComputedStyle(e).borderWidth,
              rect:e.getBoundingClientRect().toJSON()
            })""")

        visit("qcm-general")
        page.locator("#fastModeBtn").click()
        q1=depth("#answers button.answer")
        assert q1["paddingLeft"]>=58,(label,"General text overlaps radio circle",q1)
        assert "rgba" in q1["shadow"] and q1["shadow"]!="none",(label,"General card flat",q1)
        assert q1["animation"]=="none",(label,"unwanted animated push",q1)
        radio=page.locator("#answers button.answer").first.evaluate("""e=>{
          const s=getComputedStyle(e,'::before');
          return {left:parseFloat(s.left),width:parseFloat(s.width),border:parseFloat(s.borderLeftWidth)}
        }""")
        assert radio["left"]+radio["width"]+radio["border"]+10<q1["paddingLeft"],(label,"radio overlaps lettering",q1,radio)
        page.locator("#answers button.answer").first.scroll_into_view_if_needed()
        page.screenshot(path=str(OUT/f"{label}-general-choix-relief.png"),full_page=False)
        page.locator("#answers button.answer").first.click()
        assert page.locator("#answers button.answer.selected, #answers button.answer[aria-pressed='true']").count()>=1,(label,"selection lost")
        chosen=page.locator("#answers button.answer.selected, #answers button.answer[aria-pressed='true']").first.evaluate("e=>getComputedStyle(e).boxShadow")
        assert "inset" in chosen,(label,"no persistent selected marker",chosen)

        visit("qcm-energie")
        page.get_by_role("button",name="Commencer en mode rapide").first.click()
        energy=depth("#answers button")
        assert energy["shadow"]!="none",(label,"Energy QCM flat",energy)
        page.locator("#answers button").first.scroll_into_view_if_needed()
        page.screenshot(path=str(OUT/f"{label}-energie-choix-relief.png"),full_page=False)

        visit("qcm-aspa")
        page.locator(".modes .mode.rapide").click()
        classic=depth(".opts .opt")
        assert classic["shadow"]!="none",(label,"Classic QCM flat",classic)
        page.locator(".opts .opt").first.scroll_into_view_if_needed()
        page.screenshot(path=str(OUT/f"{label}-aspa-choix-relief.png"),full_page=False)
        page.locator(".opts .opt").first.click()
        page.wait_for_timeout(220)  # CSS border-color transition must complete before color assertion.
        good=page.locator(".opts .opt.bonne").first
        good.wait_for()
        good_style=good.evaluate("e=>({bg:getComputedStyle(e).backgroundImage,shadow:getComputedStyle(e).boxShadow,color:getComputedStyle(e).borderTopColor})")
        assert good_style["bg"]=="none",(label,"correct factual answer background overwritten",good_style)
        assert "inset" in good_style["shadow"],(label,"correct factual answer indicator hidden",good_style)
        if page.locator(".opts .opt.mauvaise").count():
          wrong_style=page.locator(".opts .opt.mauvaise").first.evaluate("e=>({bg:getComputedStyle(e).backgroundImage,shadow:getComputedStyle(e).boxShadow,color:getComputedStyle(e).borderTopColor})")
          assert wrong_style["bg"]=="none",(label,"incorrect factual answer overwritten",wrong_style)
          assert wrong_style["color"]!=good_style["color"],(label,"correct and incorrect colors identical")


        visit("qcm-fraude-fiscale")
        page.locator("#quickModeBtn").click()
        fraud=depth(".answers .answer-button")
        assert fraud["shadow"]!="none",(label,"Fraud QCM flat",fraud)
        page.locator(".answers .answer-button").first.scroll_into_view_if_needed()
        page.screenshot(path=str(OUT/f"{label}-fraude-choix-relief.png"),full_page=False)

        visit("qcm-democratie-decisionnelle")
        ballot=depth(".choice-card")
        assert ballot["shadow"]!="none",(label,"Citizen ballot choices flat",ballot)
        page.locator(".choice-card").first.scroll_into_view_if_needed()
        page.screenshot(path=str(OUT/f"{label}-bulletin-choix-relief.png"),full_page=False)
        for slug in QCMS:
          if slug in ("qcm-general","qcm-energie","qcm-aspa","qcm-fraude-fiscale","qcm-democratie-decisionnelle"):continue
          visit(slug)
        assert not errors,(label,"JS exceptions",errors[:8])
        assert not missing,(label,"missing resources",sorted(set(missing))[:10])
        print("PASS",label,"9 QCM unchanged; General radio/text separated; cards raised and selectable; no errors")
        ctx.close()
      browser.close()
    print("SUCCESS V2.8.3 — purely visual QCM improvement")

if __name__=="__main__":main()
