# Doctrine Éconologique — Journal de consolidation UX / SEO / QCM V2.3

**Date** : 6 novembre 2026  
**Statut** : prototype de démonstration non publié, non indexé.  
**Auteurs des contributions** : proposition « Vision Livre » et V2.2 de Grok ; parcours citoyen V2.0 de ChatGPT ; consolidation V2.3 réalisée par ChatGPT.  
**Répartition des droits** : Grok peut lire GitHub et déposer sur Drive ; Claude et ChatGPT sont habilités à intervenir sur GitHub. La branche de sauvegarde Grok V2.2 a été créée et alimentée par ChatGPT, à partir des documents Grok présents sur Drive.

## Dossier canonique Drive

`[DOCTRINE] Éconologique — Souveraineté Française / 06 — 🟣 SCRIPTS_TECHNIQUES — Apps Script / 01 — 🌐 SITE_WEB — Refonte UX-SEO-QCM — V2 — 2026-11-06`

URL : https://drive.google.com/drive/folders/1sKH5ptEyqqir0utiKCh7p3G5WKNylnYE

## Origines préservées

- Code original Grok V2.2 : `06_SITE_WEB_Prototype_Grok_Fusion_V2.2_2026-11-06.html` (Drive).
- Audit original Grok V2.2 et journal Grok V2.2 : conservés à part.
- Code original ChatGPT V2.0 : `06_SITE_WEB_Prototype_Fusion_Grok_ChatGPT_UX_SEO_QCM_V2.0_2026-11-06.html` (Drive).
- Sauvegarde GitHub Grok V2.2 : branche `review/grok-ux-seo-qcm-v2-2-2026-11-06`, rédigée et committée par ChatGPT sans modifier les fichiers originaux de Grok.
- Branche de production : `main` ; fichier `index.html` du site officiel conservé. SHA du fichier vérifié au début du chantier : `06727f1a89d957f3d854effadc2dfb75bdd99978`.

## Décisions UX et design V2.3

1. **Conserver l'architecture V2.0** : accueil élégant, bloc « Et vous, que décideriez-vous ? », QCM général, bulletin citoyen, catalogue de 17 thèmes avec recherche, filtres et liens détaillés.
2. **Reprendre de Grok V2.2 le parcours découverte court**, avec trois sujets du quotidien : énergie, produits durables, grand âge. Les révélations sont rendues accessibles par de vrais boutons HTML `aria-expanded` et `aria-controls` pilotant des blocs masqués avec `hidden` ; le clavier fonctionne sans hack.
3. **Reprendre les badges d'impact citoyen** sur les 17 cartes ; étiquettes qualitatives sans chiffres inventés.
4. **Mettre en valeur la méthode contradictoire des cinq IA** avec une présentation compacte, des pastilles et un panneau `<details>` natif. Préciser que plusieurs IA n'impliquent pas l'exactitude scientifique et que les lecteurs doivent vérifier les sources.
5. **Conserver les QCM visibles sur l'accueil et la barre mobile**, y compris le QCM général omis dans la V2.2.
6. **Éviter les boutons flottants redondants** sur smartphone : barre inférieure QCM conservée, bouton flottant Grok non retenu car il masquait les cartes et surchargeait l'écran.
7. **Conserver `noindex, nofollow`** pendant la phase bêta. Ne pas reprendre le `SearchAction` de Grok puisque la recherche en page n'est pas une fonction `?s=` sur le domaine officiel. Le JSON-LD de prototype se limite à `WebPage` / `WebSite` sans fonctionnalité fictive.
8. **Conserver 15 liens vers des pages de dossiers existantes dans le dépôt** et ne pas inventer les URL des thèmes XVI et XVII.

## Contrôles effectués au 6 novembre 2026

- 17 cartes thématiques et 17 badges.
- 10 chemins QCM / questionnaires retrouvés dans le dépôt `main` (source GitHub contrôlée dans le chantier V2.1).
- 15 pages de dossiers dont le fichier `index.html` existe sur la branche `main` (source GitHub contrôlée dans le chantier V2.1).
- Test Chromium / Playwright sur viewport 390 px : 17 cartes visibles, révélation du parcours découverte fonctionnelle, recherche « retraite » → 1 résultat, filtre Production → 5 résultats, menu mobile opérationnel, panneau 5 IA ouvrable et absence de débordement horizontal, aucune erreur `pageerror` constatée.
- Prévisualisation visuelle sur navigateur Chromium à 1440 px ; images d'aperçu enregistrées.
- Vérification de la présence de `noindex`, du QCM général et des URL officielles dans le HTML.

**Contrôles non réalisés / réserves** : navigation sur appareil réel et lecteur d'écran ; mesure Core Web Vitals sur hébergement de production ; vérification de la disponibilité publique de chaque lien ; performance SEO réelle. Le site officiel ne doit pas être modifié avant validation.

## Sauvegarde et retour arrière

- La branche V2.3 est distincte de `main` et n'y fusionne rien.
- Les fichiers V2.0 et V2.2 sont conservés sans modification sur Drive, et la V2.2 est sauvegardée sur GitHub comme contribution Grok.
- Pour abandonner le prototype, ne pas fusionner la branche de démonstration ; pour revenir à la V2.0, restaurer le chemin de cette version sur la branche de test ; la production n'a pas été modifiée.
- Tout changement futur : numéro de version distinct, date, journal de différences et confirmation du dépôt Drive + GitHub.

## Nomenclature V2.3

- `06_SITE_WEB_Prototype_Fusion_Grok_ChatGPT_V2.3_2026-11-06.html`
- `06_SITE_WEB_Journal_Fusion_Grok_ChatGPT_V2.3_2026-11-06.md`
- `06_SITE_WEB_Apercu_DESKTOP_V2.3_2026-11-06.png`
- `06_SITE_WEB_Apercu_ACCUEIL_MOBILE_V2.3_2026-11-06.png`
- `06_SITE_WEB_Apercu_DECOUVERTE_DESKTOP_V2.3_2026-11-06.png`

Le prototype n'est pas un remplacement de `doctrine-econologique.fr`. Il est conçu pour être publié sur un lien de prévisualisation isolé.
