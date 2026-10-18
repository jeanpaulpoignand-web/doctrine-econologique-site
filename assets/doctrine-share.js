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
