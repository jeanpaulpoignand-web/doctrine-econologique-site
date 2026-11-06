# Doctrine Éconologique — Décision UX V2.4 : des preuves discrètes, jamais absentes

- **Date :** 6 novembre 2026
- **Version :** V2.4 — consigne de design éditorial
- **Origine :** décision de l'utilisateur à la suite des propositions de refonte V2.3
- **Statut :** règle retenue pour la conception du site, des piliers et des QCM ; pas une mise en production
- **Périmètre :** accueil, dossiers/piliers, QCM, bulletins, résultats, interfaces mobiles

## Principe directeur

L'internaute vient d'abord chercher une réponse intelligible à une question qui le concerne ; il ne vient pas pour lire un appareil méthodologique. Les étiquettes `[FAIT]`, `[CALCUL]`, `[HYPOTHÈSE]`, `[ANALYSE]`, `[PROPOSITION]`, et `[SOURCE]` ne doivent **pas** être omniprésentes, répétées en tête de paragraphes ou transformées en badges colorés concurrençant le contenu.

**Règle : « Comprendre d'abord, vérifier si on le souhaite. »** Les preuves restent vérifiables à un clic, avec un traitement visuel sobre et cohérent. Le site n'abandonne aucune exigence de rigueur factuelle.

## Hiérarchie d'affichage

1. **Premier niveau — humain :** question concrète, réponse courte, conséquence pratique et possibilité de participer à un QCM. Pas de jargon de méthode ni de constellation de badges.
2. **Deuxième niveau — explication :** éléments clés, exemple compréhensible, chiffre important avec sa nature indiquée en langage courant lorsque cela change son interprétation.
3. **Troisième niveau — vérification :** lien discret « Sources et méthode » / « Voir le détail des calculs » / « D'où vient ce chiffre ? », qui ouvre un panneau ou conduit vers une section accessible. On y trouve la source, la date, l'hypothèse, les limites, le calcul reproductible et le statut de la proposition.

## Règles d'interface

- Aucune répétition systématique de `[FAIT]` / `[CALCUL]` / `[HYPOTHÈSE]` / `[PROPOSITION]` sur toutes les cartes et toutes les réponses.
- Préférer un lien bas de carte en texte secondaire (« Sources et méthode »), un accordéon HTML `<details><summary>` ou une note de bas de page, discret mais visible et utilisable au clavier.
- Rendre l'ouverture facultative : on peut lire ou remplir un QCM sans passer par les détails méthodologiques.
- Dans les QCM : afficher la question, les choix, puis une réponse rédigée en langage naturel, avec « Pourquoi ? » et « Vérifier les sources » comme approfondissements.
- Ne jamais sacrifier l'information **matériellement déterminante** : une simulation, une estimation, une affirmation débattue ou une proposition ne peut pas être présentée comme un fait établi. Une réserve courte en langue naturelle reste directement au niveau du chiffre ou de la conclusion quand nécessaire (ex. « estimation selon ce scénario »).
- Toujours conserver les références originales, la datation, les incertitudes et la traçabilité dans le panneau de vérification ou les pages sources.
- Éviter les pop-ups imposées, les menus complexes et les animations intrusives ; favoriser une typographie calme, des contrastes suffisants et de grandes zones tactiles.

## Exemple d'une carte QCM

**Pourquoi ma facture augmente-t-elle ?**

« Les prix dépendent notamment de la production, du réseau et des règles du marché. Découvrez quels leviers la Doctrine propose de modifier. »

**[Répondre aux questions]**

« Sources et méthode › » (affichage discret, optionnel)

## Sauvegarde et publication

- Classer cette décision dans `[DOCTRINE] Éconologique — Souveraineté Française/06 — 🟣 SCRIPTS_TECHNIQUES — Apps Script/01 — 🌐 SITE_WEB — Refonte UX-SEO-QCM — V2 — 2026-11-06`.
- Déposer aussi le journal de décision sur une branche GitHub de travail V2.4 indépendante de `main`.
- Ne pas modifier le site public ni remplacer les prototypes V2.0 / V2.2 / V2.3 sans validation humaine.
