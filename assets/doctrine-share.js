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


/* Navigation de production — même menu pour accueil, piliers et questionnaires. */
(()=>{'use strict';
  const loader=document.currentScript;
  if(!loader || !loader.src)return;
  const root=new URL('../',loader.src).href;
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
    for(const href of [root+'assets/menu-global-v271.css',root+'assets/identite/logo-perplexity-v272.css']){
      if(!document.querySelector('link[rel="stylesheet"][href="'+href+'"]')){
        const sheet=document.createElement('link');sheet.rel='stylesheet';sheet.href=href;document.head.appendChild(sheet);
      }
    }
    if(!document.querySelector('link[rel="apple-touch-icon"]')){
      const apple=document.createElement('link');apple.rel='apple-touch-icon';
      apple.setAttribute('sizes','180x180');apple.href=root+'apple-touch-icon.png';document.head.appendChild(apple);
    }
    if(!document.querySelector('link[rel="icon"]')){
      const icon=document.createElement('link');icon.rel='icon';icon.type='image/png';
      icon.setAttribute('sizes','32x32');icon.href=root+'favicon-32.png';document.head.appendChild(icon);
    }
    const homepage=document.getElementById('menu-toggle');
    const existing=document.getElementById('nav-links');
    if(homepage&&existing){
      // L'accueil conserve son propre hamburger ; ne pas afficher deux menus.
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
    const mark=document.createElement('span');mark.className='dmenu-brandmark dlogo-mounted';
    const markImg=document.createElement('img');
    markImg.src=root+'assets/identite/symbole-perplexity.png';markImg.alt='';
    markImg.width=38;markImg.height=38;markImg.decoding='async';
    mark.appendChild(markImg);
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
    document.body.insertBefore(bar,document.body.firstChild);
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




/* Continuité des liens internes : une navigation sur le site ne doit pas ouvrir un
   nouvel onglet. Le balisage HTML des liens sources externes reste inchangé. */
(()=>{'use strict';
  function init(){
    document.querySelectorAll('a[href]').forEach(a=>{
      try{
        const url=new URL(a.getAttribute('href'),location.href);
        if(url.origin===location.origin && (a.target==='_blank'||a.target==='_top')){
          a.removeAttribute('target');
        }
      }catch{}
    });
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init,{once:true});else init();
})();


/* V2.8 — Couche réservée au miroir d'essai RawGitHack.
 * NE PAS transférer dans la branche release/v28-candidate ni dans main.
 * Sur l'hébergement officiel, aucun routage et aucune directive noindex.
 */
(()=>{'use strict';
  if(!['raw.githack.com','rawgit.com'].includes(location.hostname.toLowerCase()))return;
  const parts=location.pathname.split('/').filter(Boolean);
  if(parts.length<4||!['preview-v28-2026-11-07','preview-v28-hero-align-2026-11-07','preview-v283-qcm-relief-2026-11-07'].includes(parts[2]))return;
  const root='/'+parts.slice(0,3).join('/')+'/';
  function previewHref(raw){
    if(!raw||raw.startsWith('#')||/^(mailto|tel|sms|javascript):/i.test(raw))return null;
    let u;try{u=new URL(raw,location.href)}catch{return null;}
    const host=u.hostname.replace(/^www\./i,'').toLowerCase();
    let path=null;
    if(host==='doctrine-econologique.fr')path=u.pathname.replace(/^\/+/,'');
    else if(u.origin===location.origin){
      if(u.pathname.startsWith(root))path=u.pathname.slice(root.length);
      else path=u.pathname.replace(/^\/+/,'');
    }else return null;
    if(!path||path.endsWith('/'))path+='index.html';
    return location.origin+root+path+u.search+u.hash;
  }
  function rewrite(node){
    const els=[];
    if(node.nodeType===1&&node.matches&&node.matches('a[href]'))els.push(node);
    if(node.querySelectorAll)node.querySelectorAll('a[href]').forEach(x=>els.push(x));
    for(const a of els){
      const m=previewHref(a.getAttribute('href'));
      if(m&&a.href!==m){a.href=m;if(a.target==='_top'||a.target==='_blank')a.removeAttribute('target')}
    }
  }
  function init(){
    const robot=document.createElement('meta');
    robot.name='robots';robot.content='noindex,nofollow';document.head.appendChild(robot);
    const banner=document.createElement('aside');banner.id='preview-v28-banner';
    banner.setAttribute('role','note');
    banner.style.cssText='box-sizing:border-box;position:relative;z-index:120;padding:8px 12px;background:#f6f0e4;color:#17273e;text-align:center;border-bottom:1px solid #dddcd2;font:600 12px/1.45 system-ui,-apple-system,sans-serif';
    banner.innerHTML='CANDIDATE V2.8 — PRÉVISUALISATION, PAS LE SITE OFFICIEL · <a href="'+root+'index.html" style="color:#97452f;text-decoration:underline">Accueil de la candidate</a>';
    document.body.insertBefore(banner,document.body.firstChild);
    rewrite(document);
    new MutationObserver(records=>{
      for(const r of records)for(const n of r.addedNodes)if(n.nodeType===1)rewrite(n);
    }).observe(document.body,{subtree:true,childList:true});
    document.addEventListener('click',e=>{
      if(e.defaultPrevented||e.button!==0||e.ctrlKey||e.metaKey||e.altKey||e.shiftKey)return;
      const a=e.target.closest&&e.target.closest('a[href]');
      if(!a||a.hasAttribute('download'))return;
      const m=previewHref(a.href);if(m&&a.href!==m)a.href=m;
    },true);
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init,{once:true});else init();
})();
