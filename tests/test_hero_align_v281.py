#!/usr/bin/env python3
"""V2.8.1 hero visual regression: straight and top-aligned navy start panel."""
from pathlib import Path
from urllib.parse import urlparse,unquote
import mimetypes
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
PREFIX="/jeanpaulpoignand-web/doctrine-econologique-site/preview-v28-hero-align-2026-11-07/"
BASE="https://raw.githack.com"+PREFIX
OUT=ROOT/".test-artifacts"/"hero-align"
OUT.mkdir(parents=True,exist_ok=True)

def main():
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True)
  for label,w,h in [("desktop",1485,1024),("desktop-mid",1024,768),("ipad-portrait",820,1180),("iphone",390,844),("iphone-small",320,650)]:
   ctx=browser.new_context(viewport={"width":w,"height":h},device_scale_factor=1)
   ctx.route("https://fonts.googleapis.com/**",lambda route:route.abort())
   ctx.route("https://fonts.gstatic.com/**",lambda route:route.abort())
   missing=[]
   def serve(route):
    path=unquote(urlparse(route.request.url).path)
    if not path.startswith(PREFIX):return route.fulfill(status=404,body="Outside preview")
    rel=path[len(PREFIX):];file=(ROOT/rel).resolve()
    if not file.is_relative_to(ROOT) or not file.is_file():
     missing.append(rel);return route.fulfill(status=404,body="Missing "+rel)
    return route.fulfill(status=200,path=str(file),content_type=mimetypes.guess_type(str(file))[0] or "application/octet-stream")
   ctx.route("https://raw.githack.com/**",serve)
   page=ctx.new_page();errors=[]
   page.on("pageerror",lambda e:errors.append(str(e)))
   page.goto(BASE+"index.html",wait_until="domcontentloaded",timeout=30000)
   page.locator("#preview-v28-banner").wait_for()
   geom=page.evaluate("""() => {
      let text=document.querySelector('.hero .eyebrow').getBoundingClientRect();
      let board=document.querySelector('.hero .question-board').getBoundingClientRect();
      let grid=document.querySelector('.hero-grid');
      return {textTop:text.top,boardTop:board.top,angle:getComputedStyle(document.querySelector('.hero .question-board')).transform,
              cols:getComputedStyle(grid).gridTemplateColumns,
              spill:document.documentElement.scrollWidth-document.documentElement.clientWidth};
   }""")
   assert geom["angle"]=="none",(label,geom)
   assert geom["spill"]<=3,(label,"horizontal overflow",geom)
   if w>950:
    assert abs(geom["textTop"]-geom["boardTop"])<=3,(label,"misaligned hero",geom)
   assert "noindex" in page.locator('meta[name="robots"]').last.get_attribute("content")
   assert not errors,(label,"JS errors",errors[:5])
   assert not missing,(label,"missing assets",missing[:10])
   page.screenshot(path=str(OUT/f"{label}-accueil-panneau-aligne.png"),full_page=False)
   print("PASS",label,geom,flush=True)
   ctx.close()
  browser.close()

if __name__=="__main__":main()
