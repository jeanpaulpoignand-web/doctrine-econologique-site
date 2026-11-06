#!/usr/bin/env python3
"""Live browser smoke test for Doctrine Éconologique QCM V2.4.
Runs against a local HTTP server started by GitHub Actions; no real visitors/data.
"""
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = os.environ.get('QCM_TEST_BASE', 'http://127.0.0.1:8765')
OUT = Path('.test-artifacts/qcm-v24-screens')
OUT.mkdir(parents=True, exist_ok=True)
PAGES = (
    'qcm-general/', 'qcm-energie/', 'qcm-aspa/', 'qcm-pilier-vi/',
    'qcm-textile/', 'qcm-fraude-fiscale/', 'qcm-immigrants-journee/',
    'qcm-consigne-megots/',
)


def open_qcm(browser, path, width=1440, height=900):
    page = browser.new_page(viewport={'width': width, 'height': height}, device_scale_factor=1)
    errors = []
    page.on('pageerror', lambda exc: errors.append(str(exc)))
    response = page.goto(BASE + '/' + path, wait_until='domcontentloaded', timeout=30000)
    assert response and response.status == 200, (path, 'HTTP status', response and response.status)
    page.locator('h1').first.wait_for(timeout=8000)
    assert page.locator('h1').count() == 1, (path, 'H1 count', page.locator('h1').count())
    assert 'qcm-citizen' in page.locator('body').get_attribute('class'), (path, 'theme body class')
    page.wait_for_function("getComputedStyle(document.body).backgroundColor === 'rgb(250, 248, 243)'", timeout=12000)
    assert not errors, (path, 'JS page errors', errors)
    return page, errors


def general_qcm(browser):
    page, errors = open_qcm(browser, 'qcm-general/')
    page.screenshot(path=str(OUT / 'general-desktop-accueil.png'), full_page=True)
    page.locator('#fastModeBtn').click()
    page.locator('#answers button.answer').first.wait_for(timeout=8000)
    page.screenshot(path=str(OUT / 'general-desktop-question.png'), full_page=True)
    for i in range(10):
        page.locator('#answers button.answer').first.click()
        page.locator('#nextBtn').click()
        if i < 9:
            page.wait_for_function('(n) => document.querySelector("#stepLabel").textContent.includes(`Question ${n} / 10`)', arg=i + 2)
    page.locator('#results').wait_for(state='visible', timeout=10000)
    assert page.locator('#resultTitle').inner_text().strip(), 'general missing result title'
    assert page.locator('#bars').count() == 1, 'general result scores absent'
    page.screenshot(path=str(OUT / 'general-desktop-resultat.png'), full_page=True)
    assert not errors, ('general JS errors', errors)
    page.close()


def energie_qcm(browser):
    page, errors = open_qcm(browser, 'qcm-energie/')
    page.screenshot(path=str(OUT / 'energie-desktop-accueil.png'), full_page=True)
    page.locator('button[onclick="startQuiz(\'rapide\')"]').first.click()
    page.locator('#answers button').first.wait_for(timeout=8000)
    page.screenshot(path=str(OUT / 'energie-desktop-question.png'), full_page=True)
    for i in range(19):
        page.locator('#answers button').first.click()
        if i < 18:
            page.wait_for_function('(n) => document.querySelector("#progressText").textContent.includes(`Question ${n} / 19`)', arg=i + 2, timeout=8000)
    page.locator('#result').wait_for(state='visible', timeout=10000)
    assert page.locator('#profileTitle').inner_text().strip(), 'energy result missing'
    page.screenshot(path=str(OUT / 'energie-desktop-resultat.png'), full_page=True)
    assert not errors, ('energy JS errors', errors)
    page.close()


def mobile_smoke(browser, path, out):
    page, errors = open_qcm(browser, path, width=390, height=844)
    page.screenshot(path=str(OUT / out), full_page=True)
    overflow = page.evaluate('document.documentElement.scrollWidth - window.innerWidth')
    assert overflow <= 3, (path, 'horizontal overflow', overflow)
    assert not errors, (path, 'mobile JS errors', errors)
    page.close()


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
        try:
            for path in PAGES:
                page, errors = open_qcm(browser, path)
                assert not errors
                page.close()
                print('OK page', path)
            general_qcm(browser)
            print('OK parcours complet QCM général : 10 réponses et résultat')
            energie_qcm(browser)
            print('OK parcours complet QCM Énergie : 19 réponses et résultat')
            mobile_smoke(browser, 'qcm-general/', 'general-mobile-accueil.png')
            mobile_smoke(browser, 'qcm-energie/', 'energie-mobile-accueil.png')
            mobile_smoke(browser, 'qcm-aspa/', 'aspa-mobile-accueil.png')
            print('OK vues mobiles 390px (aucun débordement horizontal détecté)')
        finally:
            browser.close()
    print('QA PASSED — browser smoke test complete')


if __name__ == '__main__':
    main()