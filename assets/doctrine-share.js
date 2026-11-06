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
  if(chunks.length<4 || chunks[2]!=='preview-v26-2026-11-07') return;
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
    notice.innerHTML='Prépublication V2.6 — site d’essai, non officiel <span aria-hidden="true">·</span> <a href="'+base+'index.html" style="color:#97452f;text-decoration:underline">Accueil de la prépublication</a>';
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
