/* Partage local : aucun stockage, aucune transmission des réponses. */
(()=>{'use strict';
 document.querySelectorAll('nav.doctrine-navigation').forEach(nav=>{
  const button=document.createElement('button'),menu=document.createElement('div'),live=document.createElement('span');
  button.type='button';button.className='doctrine-navigation-share';button.setAttribute('aria-haspopup','true');button.setAttribute('aria-expanded','false');
  button.innerHTML='<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M12 16V3m-5 5 5-5 5 5M4 14v7h16v-7"/></svg>Partager';
  menu.className='doctrine-share-menu';menu.hidden=true;menu.setAttribute('role','menu');menu.setAttribute('aria-label','Partager cette page');
  menu.innerHTML='<a role="menuitem">✉️ Envoyer par e-mail</a><a role="menuitem">💬 Envoyer par SMS</a><button type="button" role="menuitem">🔗 Copier le lien</button>';
  live.className='doctrine-share-live';live.setAttribute('aria-live','polite');
  nav.append(button,menu,live);
  const items=[...menu.children],copy=items[2];let timer;
  const data=()=>({title:document.title,text:document.querySelector('meta[name="doctrine-share-text"]')?.content||'À découvrir sur la Doctrine Éconologique : « '+document.title+' »',url:location.origin+location.pathname});
  function close(){if(menu.hidden)return;menu.hidden=true;button.setAttribute('aria-expanded','false');button.focus();}
  function open(){const d=data();items[0].href='mailto:?subject='+encodeURIComponent(d.title)+'&body='+encodeURIComponent(d.text+'\n\n'+d.url);items[1].href='sms:?&body='+encodeURIComponent(d.text+' '+d.url);menu.hidden=false;button.setAttribute('aria-expanded','true');const b=button.getBoundingClientRect(),w=menu.getBoundingClientRect().width;menu.style.left=Math.max(8,Math.min(innerWidth-w-8,b.left+(b.width-w)/2))+'px';menu.style.top=b.bottom+8+'px';items[0].focus();}
  button.addEventListener('click',async()=>{if(!menu.hidden){close();return;}if(typeof navigator.share==='function'){try{await navigator.share(data());return;}catch(e){if(e.name==='AbortError')return;}}open();});
  items.slice(0,2).forEach(item=>item.addEventListener('click',close));
  copy.addEventListener('click',async()=>{const url=data().url;try{try{await navigator.clipboard.writeText(url);}catch{const field=document.createElement('textarea');field.value=url;field.className='doctrine-share-live';document.body.append(field);field.select();let ok;try{ok=document.execCommand('copy');}finally{field.remove();}if(!ok)throw Error('copy');}copy.textContent='✓ Lien copié';live.textContent='✓ Lien copié';clearTimeout(timer);timer=setTimeout(()=>{copy.textContent='🔗 Copier le lien';live.textContent='';},2000);}catch{live.textContent='La copie du lien a échoué.';}close();});
  menu.addEventListener('keydown',e=>{if(e.key==='Escape'){e.preventDefault();close();}else if(e.key==='ArrowDown'||e.key==='ArrowUp'){e.preventDefault();items[(items.indexOf(document.activeElement)+(e.key==='ArrowDown'?1:2))%3].focus();}else if(e.key==='Tab')close();});
  document.addEventListener('click',e=>{if(!menu.contains(e.target)&&!button.contains(e.target))close();});
  window.addEventListener('resize',close);window.addEventListener('scroll',close,true);
 });
})();


/* === Prépublication V2.6, branche preview-v26-2026-11-07 uniquement. ===
 * Transforme les liens internes en liens propres au miroir RawGitHack,
 * sans toucher aux contenus, calculs, questionnaires ou au site de production.
 * L'exécution est strictement limitée à l'URL de prépublication. */
(()=>{'use strict';
  const host=location.hostname.toLowerCase();
  if(host!=='raw.githack.com' && host!=='rawgit.com') return;
  const chunks=location.pathname.split('/').filter(Boolean);
  if(chunks.length<4 || !/^preview-v2[67]-2026-11-07$|^preview-v27-(menu|logo)-2026-11-07$/.test(chunks[2])) return;
  const base='/'+chunks.slice(0,3).join('/')+'/';
  function toPreview(href){
    if(!href||href.startsWith('mailto:')||href.startsWith('tel:')||href.startsWith('sms:')||href.startsWith('javascript:')) return null;
    let u;try{u=new URL(href,location.href);}catch{return null;}
    const hostname=u.hostname.toLowerCase().replace(/^www\./,'');
    let relative;
    if(hostname==='doctrine-econologique.fr'){
      relative=u.pathname.replace(/^\/+/,'');
    }else if(u.origin===location.origin && u.pathname.startsWith(base)){
      relative=u.pathname.slice(base.length);
    }else return null;
    if(relative===''||relative.endsWith('/')) relative+='index.html';
    return location.origin+base+relative+u.search+u.hash;
  }
  function rewriteLinks(root){
    const anchors=[];
    if(root.nodeType===1&&root.matches&&root.matches('a[href]')) anchors.push(root);
    if(root.querySelectorAll) root.querySelectorAll('a[href]').forEach(a=>anchors.push(a));
    for(const a of anchors){
      const mapped=toPreview(a.getAttribute('href'));
      if(!mapped||a.href===mapped) continue;
      a.href=mapped;
      if(a.getAttribute('target')==='_blank'||a.getAttribute('target')==='_top'){
        a.removeAttribute('target');
      }
    }
  }
  function activate(){
    const meta=document.createElement('meta');
    meta.name='robots';meta.content='noindex,nofollow';
    document.head.appendChild(meta);
    const notice=document.createElement('div');
    notice.id='preview-v26-notice';
    notice.setAttribute('role','note');
    notice.style.cssText='box-sizing:border-box;display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:9px;padding:7px 12px;background:#f6f0e4;color:#17273e;border-bottom:1px solid #dddcd2;text-align:center;font:600 12px/1.45 system-ui,-apple-system,sans-serif;position:relative;z-index:40';
    notice.innerHTML='Prépublication V2.7 — site d’essai, non officiel <span aria-hidden="true">·</span> <a href="'+base+'index.html" style="color:#97452f;text-decoration:underline">Accueil de la prépublication</a>';
    document.body.insertBefore(notice,document.body.firstChild);
    rewriteLinks(document);
    new MutationObserver(records=>{
      for(const record of records)for(const node of record.addedNodes)if(node.nodeType===1)rewriteLinks(node);
    }).observe(document.body,{childList:true,subtree:true});
    document.addEventListener('click',e=>{
      if(e.defaultPrevented||e.button!==0||e.ctrlKey||e.metaKey||e.altKey||e.shiftKey) return;
      const a=e.target.closest&&e.target.closest('a[href]');
      if(!a||a.hasAttribute('download'))return;
      const mapped=toPreview(a.href);
      if(!mapped)return;
      if(a.href!==mapped) a.href=mapped;
    },true);
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',activate,{once:true});
  else activate();
})();


/* V2.7.1 — Menu universel « hamburger » de prépublication.
 * Uniquement actif sur preview-v27-menu-2026-11-07, jamais sur main.
 * L'accueil garde son propre hamburger ; les autres pages gagnent un en-tête léger.
 */
(()=>{'use strict';
  if(!['raw.githack.com','rawgit.com'].includes(location.hostname.toLowerCase()))return;
  const parts=location.pathname.split('/').filter(Boolean);
  if(parts.length<4||!['preview-v27-menu-2026-11-07','preview-v27-logo-2026-11-07'].includes(parts[2]))return;
  const root='/'+parts.slice(0,3).join('/')+'/';
  const entries=[
    ['Accueil',root+'index.html'],
    ['Les 17 piliers',root+'piliers/index.html'],
    ['Les 9 questionnaires',root+'questionnaires/index.html'],
    ['Bulletin citoyen',root+'qcm-democratie-decisionnelle/index.html'],
    ['Guide de lecture',root+'guide-de-lecture/index.html'],
    ['À propos',root+'a-propos/index.html']
  ];
  function init(){
    if(document.getElementById('dmenu-panel'))return;
    const style=document.createElement('link');
    style.rel='stylesheet';style.href=root+'assets/menu-global-v271.css';
    document.head.appendChild(style);
    const homepage=document.getElementById('menu-toggle');
    const existing=document.getElementById('nav-links');
    if(homepage&&existing){
      // Accueil V2.3 possède déjà un hamburger fonctionnel : ne pas en afficher deux.
      for(const [i,[label,url]] of entries.entries()){
        const a=document.createElement('a');
        a.href=url;a.textContent=label;
        a.className='dmenu-home-mobile'+(i===3?' dmenu-home-action':'');
        a.addEventListener('click',()=>{
          existing.classList.remove('open');homepage.setAttribute('aria-expanded','false');
          homepage.setAttribute('aria-label','Ouvrir le menu de navigation');
        });
        existing.appendChild(a);
      }
      homepage.setAttribute('aria-label','Ouvrir le menu de navigation');
      homepage.addEventListener('click',()=>{
        homepage.setAttribute('aria-label',homepage.getAttribute('aria-expanded')==='true'?'Fermer le menu de navigation':'Ouvrir le menu de navigation');
      });
      document.addEventListener('keydown',e=>{
        if(e.key==='Escape'&&existing.classList.contains('open')){
          existing.classList.remove('open');homepage.setAttribute('aria-expanded','false');
          homepage.setAttribute('aria-label','Ouvrir le menu de navigation');homepage.focus();
        }
      });
      return;
    }
    const bar=document.createElement('div');bar.id='dmenu-bar';
    const brand=document.createElement('a');brand.href=root+'index.html';brand.className='dmenu-brand';
    brand.setAttribute('aria-label','Doctrine Éconologique — retour à l’accueil');
    const mark=document.createElement('span');mark.className='dmenu-brandmark';mark.textContent='é.';
    const name=document.createElement('span');name.className='dmenu-brandname';name.textContent='Doctrine Éconologique';
    brand.append(mark,name);
    const toggle=document.createElement('button');toggle.type='button';toggle.className='dmenu-button';
    toggle.id='dmenu-toggle';toggle.setAttribute('aria-controls','dmenu-panel');
    toggle.setAttribute('aria-expanded','false');
    toggle.setAttribute('aria-label','Ouvrir le menu de navigation');
    toggle.innerHTML='<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round"><path d="M4 6h16M4 12h16M4 18h16"/></svg>';
    bar.append(brand,toggle);
    const overlay=document.createElement('div');overlay.id='dmenu-overlay';overlay.hidden=true;
    const panel=document.createElement('nav');panel.id='dmenu-panel';panel.hidden=true;
    panel.setAttribute('aria-label','Navigation générale de la Doctrine');
    const heading=document.createElement('div');heading.className='dmenu-panel-head';
    const title=document.createElement('span');title.className='dmenu-panel-title';title.textContent='Explorer la Doctrine';
    const closeBtn=document.createElement('button');closeBtn.type='button';closeBtn.className='dmenu-close';
    closeBtn.setAttribute('aria-label','Fermer le menu');closeBtn.textContent='×';
    heading.append(title,closeBtn);panel.appendChild(heading);
    const links=document.createElement('div');links.className='dmenu-list';
    for(const [i,[label,url]] of entries.entries()){
      if(i===4){const sep=document.createElement('div');sep.className='dmenu-separator';sep.setAttribute('aria-hidden','true');links.append(sep);}
      const a=document.createElement('a');a.href=url;a.textContent=label;a.className='dmenu-link'+(i===3?' dmenu-primary':'');
      links.appendChild(a);
    }
    panel.appendChild(links);
    const foot=document.createElement('p');foot.className='dmenu-foot';
    foot.textContent='Une démarche citoyenne indépendante · Les documents et les sources restent accessibles.';
    panel.appendChild(foot);
    const notice=document.getElementById('preview-v26-notice');
    if(notice)notice.insertAdjacentElement('afterend',bar);else document.body.insertBefore(bar,document.body.firstChild);
    document.body.append(overlay,panel);
    function setOpen(open,restoreFocus){
      if(open){
        const top=Math.min(Math.max(65,bar.getBoundingClientRect().bottom+8),Math.max(65,innerHeight-180));
        panel.style.top=top+'px';panel.style.maxHeight='calc(100dvh - '+(top+8)+'px)';
      }
      panel.hidden=!open;overlay.hidden=!open;toggle.setAttribute('aria-expanded',String(open));
      toggle.setAttribute('aria-label',open?'Fermer le menu de navigation':'Ouvrir le menu de navigation');
      document.body.classList.toggle('dmenu-open',open);
      if(open)panel.querySelector('a').focus();
      else if(restoreFocus)toggle.focus();
    }
    toggle.addEventListener('click',()=>setOpen(panel.hidden,true));
    closeBtn.addEventListener('click',()=>setOpen(false,true));
    overlay.addEventListener('click',()=>setOpen(false,true));
    panel.addEventListener('click',e=>{if(e.target.closest('a'))setOpen(false,false);});
    document.addEventListener('keydown',e=>{
      if(panel.hidden)return;
      if(e.key==='Escape'){e.preventDefault();setOpen(false,true);return;}
      if(e.key!=='Tab')return;
      const focusables=[...panel.querySelectorAll('a[href],button:not([disabled])')];
      const first=focusables[0],last=focusables[focusables.length-1];
      if(e.shiftKey&&document.activeElement===first){e.preventDefault();last.focus();}
      else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus();}
    });
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init,{once:true});
  else init();
})();


/* V2.7.2 — identité Perplexity, symbole issu de l'original PNG utilisateur.
 * Uniquement dans la branche de prépublication dédiée ; jamais en production.
 */
(()=>{'use strict';
  if(!['raw.githack.com','rawgit.com'].includes(location.hostname.toLowerCase()))return;
  const p=location.pathname.split('/').filter(Boolean);
  if(p.length<4||p[2]!=='preview-v27-logo-2026-11-07')return;
  const base='/'+p.slice(0,3).join('/')+'/';
  const image=location.origin+base+'assets/identite/symbole-perplexity.png';
  function init(){
    if(!document.querySelector('link[href*="logo-perplexity-v272.css"]')){
      const css=document.createElement('link');css.rel='stylesheet';
      css.href=base+'assets/identite/logo-perplexity-v272.css';document.head.appendChild(css);
    }
    // Un favicon unique, identique au symbole choisi.
    document.querySelectorAll('link[rel="icon"],link[rel="shortcut icon"],link[rel="apple-touch-icon"]').forEach(el=>el.remove());
    for(const [rel,sizes] of [['icon','192x192'],['apple-touch-icon','192x192']]){
      const ico=document.createElement('link');ico.rel=rel;ico.type='image/png';
      ico.sizes=sizes;ico.href=image;document.head.appendChild(ico);
    }
    function mount(){
      for(const selector of ['.site-header .brand-mark','#dmenu-bar .dmenu-brandmark']){
        for(const slot of document.querySelectorAll(selector)){
          if(slot.classList.contains('dlogo-mounted'))continue;
          slot.classList.add('dlogo-mounted');
          const img=document.createElement('img');img.src=image;img.width=44;img.height=44;
          img.alt='';img.decoding='async';img.title='Symbole de la Doctrine Éconologique — création Perplexity';
          slot.replaceChildren(img);
        }
      }
    }
    mount();
    const mo=new MutationObserver(mount);
    mo.observe(document.body,{childList:true,subtree:true});
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init,{once:true});
  else init();
})();
