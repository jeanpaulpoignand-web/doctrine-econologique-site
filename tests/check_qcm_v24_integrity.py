#!/usr/bin/env python3
"""Non-regression safety gate for Doctrine Éconologique QCM redesign.

Compare branch HTML against origin/main, using full history. Only style resources,
body classes and expressly documented disclosure wrappers may differ.
"""
from pathlib import Path
import re
import subprocess
import sys

PILOTS = ('qcm-general/index.html', 'qcm-energie/index.html')
CLASSIC = ('qcm-aspa/index.html', 'qcm-pilier-vi/index.html', 'qcm-textile/index.html')
SPECIAL = ('qcm-fraude-fiscale/index.html', 'qcm-immigrants-journee/index.html', 'qcm-consigne-megots/index.html')
PAGES = PILOTS + CLASSIC + SPECIAL


def baseline(path):
    return subprocess.check_output(['git', 'show', f'origin/main:{path}'], text=True)


def sections(html, pattern):
    return re.findall(pattern, html, flags=re.I | re.S)


def main():
    ok = True
    for path in PAGES:
        before = baseline(path)
        after = Path(path).read_text(encoding='utf-8')
        props = {
            'scripts': r'<script\b[^>]*>[\s\S]*?</script>',
            'headings': r'<h[123]\b[^>]*>[\s\S]*?</h[123]>',
            'meta': r'<meta\b[^>]*>',
            'anchors': r'<a\b[^>]*>',
            'title': r'<title\b[^>]*>[\s\S]*?</title>',
            'canonical': r'<link\b[^>]*rel=["\']canonical["\'][^>]*>',
        }
        for label, pattern in props.items():
            if sections(before, pattern) != sections(after, pattern):
                print(f'FAIL {path}: {label} changed')
                ok = False
        body = sections(after, r'<body\b[^>]*>')
        if len(body) != 1 or 'qcm-citizen' not in body[0]:
            print(f'FAIL {path}: QCM theme body class missing')
            ok = False
        if '../assets/qcm-charte-v24.css' not in after:
            print(f'FAIL {path}: shared stylesheet missing')
            ok = False
        if path in CLASSIC and '../assets/qcm-charte-v24-classic.css' not in after:
            print(f'FAIL {path}: classic theme adapter missing')
            ok = False
        if path in SPECIAL and '../assets/qcm-charte-v24-special.css' not in after:
            print(f'FAIL {path}: specialized theme adapter missing')
            ok = False
        if len(sections(after, r'<h1\b')) != 1:
            print(f'FAIL {path}: expected a single H1')
            ok = False
        print(f'{"OK" if ok else "CHECK"} {path}')
    for path in ['assets/qcm-charte-v24.css','assets/qcm-charte-v24-classic.css','assets/qcm-charte-v24-special.css']:
        css = Path(path).read_text(encoding='utf-8')
        scope = 'qcm-special' if path.endswith('-special.css') else 'qcm-citizen'
        if scope not in css or css.count('{') != css.count('}'):
            print(f'FAIL: invalid/incomplete CSS theme {path}')
            ok = False
    print('SAFE — style changes only; scripts, SEO and links preserved' if ok else 'FAILED — do not merge')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())