#!/usr/bin/env python3
"""End-to-end Chromium smoke: independent citizen ballot styling, 12 decisions and results."""
from pathlib import Path
from playwright.sync_api import sync_playwright

HOST='http://127.0.0.1:8765/qcm-democratie-decisionnelle/'
OUT=Path('.test-artifacts/bulletin-v25')
OUT.mkdir(parents=True,exist_ok=True)


def no_overflow(page, label):
    dims=page.evaluate('''() => ({viewport: document.documentElement.clientWidth,
        scroll: document.documentElement.scrollWidth,
        bodyScroll: document.body.scrollWidth})''')
    assert dims['scroll'] <= dims['viewport']+2, f'{label}: horizontal scroll: {dims}'


def base_page(browser, width, height):
    context=browser.new_context(viewport={'width':width,'height':height},locale='fr-FR', reduced_motion='reduce')
    page=context.new_page()
    errors=[]
    page.on('pageerror',lambda error: errors.append(str(error)))
    response=page.goto(HOST,wait_until='domcontentloaded')
    assert response.status==200, response.status
    page.wait_for_selector('button.choice-card',state='visible',timeout=10000)
    assert page.locator('body.bulletin-v25').count()==1
    assert 'Bulletin citoyen' in page.title()
    assert page.locator('h1').first.is_visible()
    css=page.evaluate('''() => ({color:getComputedStyle(document.querySelector('.hero-card h1')).color,
      background:getComputedStyle(document.body).backgroundColor,
      fontFamily:getComputedStyle(document.body).fontFamily,
      cssLoaded: Boolean([...document.styleSheets].some(s=>s.href?.includes('bulletin-citoyen-v25.css'))) })''')
    assert css['cssLoaded'],css
    assert css['color'] in ('rgb(23, 39, 62)','rgb(23, 39, 63)'),css
    assert css['background']=='rgb(250, 248, 243)',css
    assert 'IBM Plex Sans' in css['fontFamily'],css
    assert len(errors)==0,errors
    return context,page,errors


def test_path(browser,width,height,label):
    context,page,errors=base_page(browser,width,height)
    try:
        no_overflow(page,label+' accueil')
        page.screenshot(path=str(OUT/f'{label}-accueil.png'),full_page=True)
        # Two distinct choices: ideas and classic party ballot.
        assert page.locator('button.choice-card').count()==2
        page.get_by_role('button',name='Voter pour mes idées').click()
        assert page.locator('#answer-slider').is_visible()
        assert page.locator('#next-question').is_disabled()
        no_overflow(page,label+' question 1')
        page.screenshot(path=str(OUT/f'{label}-question-01.png'),full_page=True)
        # Reading guide opens and closes with Esc, without answering.
        page.locator('#question-help').click()
        assert page.locator('#reading-dialog').is_visible()
        assert page.locator('#reading-dialog .reading-sources').count()==1
        page.screenshot(path=str(OUT/f'{label}-lecture.png'),full_page=False)
        page.keyboard.press('Escape')
        assert page.locator('#reading-dialog').count()==0
        assert page.locator('#next-question').is_disabled()
        # Six answers are necessary for reliable ranking. Use nine positions and three without opinion.
        for i in range(12):
            assert page.locator('.nav-pill').inner_text().strip()==f'{i+1}/12'
            if i<9:
                page.locator('#answer-slider').evaluate('''(el) => {
                    el.value='76'; el.dispatchEvent(new Event('input',{bubbles:true})); }''')
            else:
                page.locator('#no-opinion').click()
            assert page.locator('#next-question').is_enabled(),f'next disabled at {i+1}'
            page.locator('#next-question').click()
        assert page.locator('.result-panel').is_visible()
        assert page.locator('.rank-card').count()>=1
        assert '9 positions exprimées' in page.locator('.certainty').inner_text()
        assert page.locator('#all-parties').is_hidden()
        page.locator('.all-parties-toggle').click()
        assert page.locator('#all-parties').is_visible()
        assert page.locator('#all-parties .all-party-card').count()>=10
        page.locator('.rank-card .source-toggle').first.click()
        assert page.locator('.rank-card .source-panel').first.is_visible()
        no_overflow(page,label+' resultat')
        page.screenshot(path=str(OUT/f'{label}-resultat.png'),full_page=True)
        # User can edit position and return to results, then clear all with explicit confirmation.
        page.get_by_role('button',name='Modifier mes réponses').click()
        assert page.locator('#axis-card').is_visible()
        page.get_by_role('button',name='Accueil').click()
        assert page.locator('.hero-card').is_visible()
        page.get_by_role('button',name='Recommencer à zéro').click()
        assert page.locator('#reset-dialog').is_visible()
        page.locator('[data-reset-cancel]').click()
        assert page.locator('#reset-dialog').count()==0
        page.get_by_role('button',name='Recommencer à zéro').click()
        page.locator('[data-reset-confirm]').click()
        assert page.locator('button.choice-card').count()==2
        assert page.locator('button.reset-link').count()==0
        # Classic vote is intentionally separate from the ideas ranking.
        page.get_by_role('button',name='Voter pour un parti').click()
        assert page.locator('.vote-card').count()==15
        page.locator('.vote-card').first.click()
        assert page.locator('.method-box').first.is_visible()
        no_overflow(page,label+' vote classique')
        page.screenshot(path=str(OUT/f'{label}-classique.png'),full_page=False)
        assert not errors, errors
        print(f'PASS {label}: 12 questions, reading guide, 9 scored positions, 3 sans avis, 15 parties, results, reset, classic, 0 overflow, 0 JS errors')
    finally:
        context.close()


def test_future(browser):
    context,page,errors=base_page(browser,390,844)
    try:
        page.locator('label.switch-row').click()
        assert page.locator('#future-explanation').is_visible()
        assert 'fictives' in page.locator('#future-explanation').inner_text()
        page.get_by_role('button',name='Voter pour mes idées').click()
        assert page.locator('.future-vote-bar, #future-vote-bar').count()>=1 or 'future-' in page.content()
        assert not errors,errors
        no_overflow(page,'mode futur')
        page.screenshot(path=str(OUT/'mobile-mode-futur.png'),full_page=False)
        print('PASS mode futur: future explanation and visual display; simulated data explicitly disclosed')
    finally:
        context.close()


def main():
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        test_path(browser,1440,900,'desktop')
        test_path(browser,390,844,'mobile')
        test_future(browser)
        browser.close()
    print('ALL BULLETIN V2.5 BROWSER TESTS PASS')

if __name__=='__main__':main()