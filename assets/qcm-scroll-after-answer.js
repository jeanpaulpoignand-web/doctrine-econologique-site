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
  function reveal(targetSelector){
    document.documentElement.dataset.qcmScrollTarget=targetSelector;
    // Attendre la reconstruction des cartes et l'apparition d'un éventuel
    // texte pédagogique : un scroll exécuté pendant le rendu se perd sur iOS.
    window.requestAnimationFrame(function(){
      window.requestAnimationFrame(function(){
        var action=document.querySelector(targetSelector);
        if(!visible(action))return;
        // Les longs retours pédagogiques peuvent perturber scrollIntoView
        // sous Safari : calculer directement la position de destination.
        var rect=action.getBoundingClientRect();
        var viewportHeight=window.visualViewport?window.visualViewport.height:window.innerHeight;
        var wanted=window.scrollY+rect.top-(viewportHeight-rect.height)*0.61;
        var limit=Math.max(0,document.documentElement.scrollHeight-window.innerHeight);
        var destination=Math.min(limit,Math.max(0,wanted));
        window.scrollTo({top:destination,behavior:reduced.matches?"instant":"smooth"});
      });
    });
  }
  document.addEventListener("click",function(event){
    var element=event.target;
    if(!(element instanceof Element))return;
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
