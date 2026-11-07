#!/usr/bin/env python3
"""V2.8 prepublication mirror: links and Apple icon must remain within the preview."""
from pathlib import Path
from urllib.parse import urlparse, unquote
import mimetypes
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
PREFIX="/jeanpaulpoignand-web/doctrine-econologique-site/preview-v28-2026-11-07/"
BASE="https://raw.githack.com"+PREFIX
OUT=ROOT/".test-artifacts"/"preview-v28"
OUT.mkdir(parents=True,exist_ok=True)
def main():
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True)
  for name,viewport in [("iphone",{"width":390,"height":844}),("ipad",{"width":820,"height":1180}),("desktop",{"width":1440,"height":900})]:
   ctx=browser.new_context(viewport=viewport)
   ctx.route("https://fonts.googleapis.com/**",lambda route:route.abort())
   ctx.route("https://fonts.gstatic.com/**",lambda route:route.abort())
   missing=[]
   def serve(route):
    path=unquote(urlparse(route.request.url).path)
    if not path.startswith(PREFIX):return route.fulfill(status=404,body="Outside candidate")
    rel=path[len(PREFIX):];file=(ROOT/rel).resolve()
    if not file.is_relative_to(ROOT) or not file.is_file():
     missing.append(rel);return route.fulfill(status=404,body="Missing "+rel)
    return route.fulfill(status=200,path=str(file),content_type=mimetypes.guess_type(str(file))[0] or "application/octet-stream")
   ctx.route("https://raw.githack.com/**",serve)
   page=ctx.new_page();errors=[]
   page.on("pageerror",lambda e:errors.append(str(e)))
   page.goto(BASE+"index.html",wait_until="domcontentloaded")
   page.locator("#preview-v28-banner").wait_for()
   assert "noindex" in page.locator('meta[name="robots"]').last.get_attribute("content")
   assert page.locator('.site-header .brand-mark img').evaluate("(e)=>e.naturalWidth===192")
   assert page.locator('link[rel="apple-touch-icon"]').evaluate("(e)=>e.href")==BASE+"apple-touch-icon.png"
   assert page.locator('link[rel="canonical"]').get_attribute("href")=="https://doctrine-econologique.fr/"
   if name=="iphone":
    page.locator("#menu-toggle").click()
    page.locator('#nav-links a[href*="/piliers/index.html"]').click()
    assert page.url==BASE+"piliers/index.html",page.url
   else:
    page.goto(BASE+"piliers/index.html",wait_until="domcontentloaded")
   page.locator("#dmenu-toggle").wait_for()
   page.locator("#dmenu-toggle").click()
   assert page.locator("#dmenu-panel").is_visible()
   assert page.locator('#dmenu-panel a[href*="qcm-democratie-decisionnelle/index.html"]').count()==1
   page.screenshot(path=str(OUT/f"{name}-catalogue-menu.png"),full_page=False)
   page.locator('#dmenu-panel a[href*="qcm-democratie-decisionnelle/index.html"]').click()
   assert page.url==BASE+"qcm-democratie-decisionnelle/index.html",page.url
   assert page.locator('link[rel="apple-touch-icon"]').evaluate("(e)=>e.href")==BASE+"apple-touch-icon.png"
   assert "noindex" in page.locator('meta[name="robots"]').last.get_attribute("content")
   page.locator("#dmenu-toggle").click()
   page.screenshot(path=str(OUT/f"{name}-bulletin-menu.png"),full_page=False)
   page.locator('#dmenu-panel a[href*="index.html"]').first.click()
   assert page.url==BASE+"index.html",page.url
   assert not errors,(name,errors[:6])
   assert not missing,(name,missing[:12])
   print("PASS preview V2.8",name,"home -> 17 pillars -> Bulletin -> home, logo and static Apple icon")
   ctx.close()
  browser.close()
if __name__=="__main__":main()
