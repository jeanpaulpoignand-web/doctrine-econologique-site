#!/usr/bin/env python3
"""Bulletin 2.5: only a body class and one CSS link may change the official HTML."""
from pathlib import Path
import subprocess
import sys

PATH='qcm-democratie-decisionnelle/index.html'
LINK='    <!-- Bulletin citoyen V2.5 : présentation uniquement ; calculs et SEO préservés -->\n    <link rel="stylesheet" href="../assets/bulletin-citoyen-v25.css">\n  </head>'

def main():
    original=subprocess.check_output(['git','show',f'origin/main:{PATH}']).decode('utf-8')
    changed=Path(PATH).read_text(encoding='utf-8')
    normalized=changed.replace('<body class="bulletin-v25">','<body>').replace(LINK,'</head>')
    if normalized != original:
        print('FAIL: Bulletin HTML differs from main beyond approved cosmetic changes')
        sys.exit(1)
    css=Path('assets/bulletin-citoyen-v25.css').read_text(encoding='utf-8')
    if 'body.bulletin-v25' not in css or len(css)<9000:
        print('FAIL: missing/incomplete scoped V2.5 style')
        sys.exit(1)
    print('PASS: original JS, 12 questions, political matrix, result methods, SEO, links and copy all byte-for-byte preserved')
    print('PASS: only new body class and new style asset linked')
    return 0

if __name__=='__main__':sys.exit(main())