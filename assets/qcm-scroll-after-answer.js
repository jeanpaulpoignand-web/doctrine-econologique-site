/* Confort de navigation des QCM — 7 novembre 2026.
 * Après une réponse, afficher le contrôle de validation / suite.
 * Sans modification des questions, des scores ni du rythme du lecteur.
 */
(function(){
  "use strict";
  var slug=window.location.pathname.split("/").filter(Boolean)[0];
  var flows={
    "qcm-general":[["#answers button.answer","#nextBtn"]],
    "qcm-energie":[["#answers button","#nextBtn"]],
    "qcm-aspa":[["#qbody button.opt","#nextBtn"]],
    "qcm-pilier-vi":[["#qbody button.opt","#validateBtn"],["#validateBtn","#nextBtn"]],
    "qcm-textile":[["#qbody button.opt","#nextBtn"]],
    "qcm-fraude-fiscale":[["#answers button.answer-button","#nextBtn"]],
    "qcm-immigrants-journee":[["#answers button.answer","#next"]],
    "qcm-consigne-megots":[["#landmarkAnswers button.answer","#landmarkNextBtn"],["#answers button.answer","#nextBtn"]],
    "qcm-democratie-decisionnelle":[["#no-opinion","#next-question"]]
  };
  var rules=flows[slug];
  if(!rules)return;
  document.documentElement.dataset.qcmScrollReady=slug;
  var reduced=window.matchMedia("(prefers-reduced-motion: reduce)");
  function visible(el){
    if(!el || el.hidden || el.disabled || el.closest("[hidden],.hidden"))return false;
    var style=window.getComputedStyle(el);
    return style.display!=="none" && style.visibility!=="hidden" && el.getClientRects().length>0;
  }
  var scrollGeneration=0;
  function centerAction(targetSelector){
    var action=document.querySelector(targetSelector);
    if(!visible(action))return;
    var rect=action.getBoundingClientRect();
    var viewportHeight=window.visualViewport?window.visualViewport.height:window.innerHeight;
    // Ne pas décaler la lecture lorsque le bouton est déjà entièrement visible.
    if(rect.top>=12 && rect.bottom<=viewportHeight-12)return;
    var wanted=window.scrollY+rect.top-(viewportHeight-rect.height)*0.61;
    var limit=Math.max(0,document.documentElement.scrollHeight-window.innerHeight);
    window.scrollTo({top:Math.min(limit,Math.max(0,wanted)),behavior:reduced.matches?"auto":"smooth"});
  }
  function reveal(targetSelector){
    var generation=++scrollGeneration;
    document.documentElement.dataset.qcmScrollTarget=targetSelector;
    // Le DOM de la réponse peut être réécrit. Les animations de feedback
    // durent jusqu'à 400 ms sur ASPA/textile : revérifier à 600 ms.
    window.requestAnimationFrame(function(){
      window.requestAnimationFrame(function(){
        if(generation!==scrollGeneration)return;
        centerAction(targetSelector);
        window.setTimeout(function(){
          if(generation!==scrollGeneration)return;
          centerAction(targetSelector);
        },600);
      });
    });
  }
  document.addEventListener("click",function(event){
    var element=event.target;
    if(!(element instanceof Element))return;
    // Une navigation volontaire annule une correction de scroll en attente.
    if(element.closest("#nextBtn,#next,#next-question,#validateBtn,#landmarkNextBtn"))scrollGeneration++;
    for(var i=0;i<rules.length;i++){
      var selector=rules[i][0];
      if(element.closest(selector)){reveal(rules[i][1]);return;}
    }
  },true);
  // Le bulletin décisionnel se remplit au curseur : déplacer le curseur
  // doit rester possible sans scroll intempestif. Défiler au relâchement.
  if(slug==="qcm-democratie-decisionnelle"){
    document.addEventListener("change",function(event){
      if(event.target instanceof Element && event.target.matches("#answer-slider")){
        reveal("#next-question");
      }
    },true);
  }
})();
