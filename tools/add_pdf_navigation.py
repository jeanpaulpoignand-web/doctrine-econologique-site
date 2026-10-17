"""Ajoute les liens de navigation après export des PDF, sans recomposer leur contenu.

Usage : python tools/add_pdf_navigation.py --root .
À exécuter après toute régénération d'un PDF publié. Les PDF déjà équipés sont ignorés.
Pré-requis : PyMuPDF. Les archives ne sont jamais modifiées.
"""
from pathlib import Path
import argparse,json,re,tempfile,os
import fitz
MARK='doctrine-navigation-v1'
def add_navigation(path,manifest):
    path=Path(path);doc=fitz.open(path)
    if MARK in (doc.metadata.get('keywords') or ''):return None
    m=re.match(r'pilier-(\d+)-',path.name);n=int(m.group(1)) if m else None
    home=manifest['site_url']+(f'#pilier-{n}' if n else '')
    drive=manifest['pillars'][str(n)]['drive_url'] if n else manifest['root_drive_url']
    right='Approfondir ce pilier sur Drive' if n else 'Documents de la Doctrine sur Drive'
    records=[]
    for i,p in enumerate(doc):
        # Le XIV possède un en-tête et son retour site : compléter cette même ligne.
        special=n==14;y=33 if special else 21
        spans=[s for b in p.get_text('dict')['blocks'] if 'lines' in b for l in b['lines'] for s in l['spans']]
        texts=[] if special else [('Retour au site',30,home)]
        xr=p.rect.width-30-fitz.get_text_length(right,fontname='helv',fontsize=8.5)
        texts.append((right,xr,drive))
        for text,x,url in texts:
            rect=fitz.Rect(x,y-9.2,x+fitz.get_text_length(text,fontname='helv',fontsize=8.5),y+2.5)
            assert all(not rect.intersects(fitz.Rect(s['bbox'])) for s in spans),('Zone occupée',path.name,i+1,text)
            assert all(not rect.intersects(l['from']) for l in p.get_links()),('Lien existant recouvert',path.name,i+1)
            color=(1,1,1) if special else (0.06,0.25,0.43)
            p.insert_text((x,y),text,fontname='helv',fontsize=8.5,color=color)
            p.draw_line((x,y+1.5),(rect.x1,y+1.5),color=color,width=.35)
            p.insert_link({'kind':fitz.LINK_URI,'from':rect,'uri':url})
        records.append({'page':i+1,'band':[0,24 if special else 10,p.rect.width,37 if special else 25],'added_links':len(texts)})
    meta=doc.metadata;meta['keywords']=((meta.get('keywords') or '')+' '+MARK).strip();doc.set_metadata(meta)
    original_pages=len(doc);old_path=path.with_name(path.name+'.nav-tmp')
    doc.save(old_path,garbage=0,deflate=True);doc.close();os.replace(old_path,path)
    return {'path':str(path),'pillar':n,'pages':original_pages,'home_url':home,'drive_url':drive,'right_label':right,'page_records':records}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--root',default='.');ap.add_argument('--report');args=ap.parse_args();root=Path(args.root)
    manifest=json.loads((root/'tools/navigation-doctrine.json').read_text());results=[]
    for p in sorted(root.rglob('*.pdf')):
        if 'archives' in p.relative_to(root).parts:continue
        r=add_navigation(p,manifest)
        if r: r['path']=str(p.relative_to(root));results.append(r)
    if args.report:Path(args.report).write_text(json.dumps(results,ensure_ascii=False,indent=2))
    print(len(results),'PDF équipés de la navigation ; pagination conservée.')
if __name__=='__main__':main()
