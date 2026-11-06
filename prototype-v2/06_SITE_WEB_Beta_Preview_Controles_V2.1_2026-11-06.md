# Doctrine Éconologique — Site web — Bêta V2.1

**Type :** compte rendu de prévisualisation et contrôle technique  
**Date :** 2026-11-06  
**Statut :** prototype public de démonstration, non publié sur le domaine officiel, **non indexable**.  
**Objet :** fusion de l’élégance visuelle proposée par Grok et de la navigation centrée sur les préoccupations citoyennes proposée par ChatGPT ; accès immédiat aux QCM.

## 1. Chemin officiel des archives

`[DOCTRINE] Éconologique — Souveraineté Française / 06 — 🟣 SCRIPTS_TECHNIQUES — Apps Script / 01 — 🌐 SITE_WEB — Refonte UX-SEO-QCM — V2 — 2026-11-06`

Dossier Drive : https://drive.google.com/drive/folders/1sKH5ptEyqqir0utiKCh7p3G5WKNylnYE

## 2. Liens GitHub et visualisation

- Référentiel officiel : https://github.com/jeanpaulpoignand-web/doctrine-econologique-site
- Branche historique de travail : `design/refonte-ux-seo-qcm-v2-2026-11-06`
- Branche dédiée à l’aperçu : `preview-ux-seo-qcm-v2-2026-11-06`
- Prototype dans cette branche : `prototype-v2/index.html`
- **Adresse de prévisualisation technique (tiers RawGitHack)** : https://raw.githack.com/jeanpaulpoignand-web/doctrine-econologique-site/preview-ux-seo-qcm-v2-2026-11-06/prototype-v2/index.html

**Limite importante :** RawGitHack n’est ni GitHub Pages ni l’hébergeur de la Doctrine. La prévisualisation peut afficher un avertissement/une confirmation de sécurité avant d’ouvrir la page HTML. Son fonctionnement dans le navigateur n’a pas pu être directement certifié dans l’environnement de vérification ; le dépôt GitHub et le fichier source ont été lus avec succès. Cette URL ne doit pas être diffusée comme adresse officielle ni utilisée pour collecter des données personnelles.

## 3. Contrôles du 6 novembre 2026

- `prototype-v2/index.html` : code HTML complet récupéré depuis GitHub, 17 cartes de sujet et un module QCM.
- 10 destinations QCM et index des questionnaires : toutes retrouvées sous `main` dans des fichiers `index.html` (GitHub).
- 15 destinations de piliers présentes dans le prototype : toutes retrouvées sous `main` dans des fichiers `index.html` (GitHub).
- Les piliers XVI et XVII sont présentés sans lien de dossier vérifié : ils ne doivent pas être raccordés au hasard.
- La balise `<meta name="robots" content="noindex, nofollow">` reste activée pour le prototype.
- Le site officiel n’a pas été modifié : aucun commit sur `main` pour cette opération.
- Les contrôles fonctionnels via navigateur automatisé n’ont pas été possibles dans l’environnement d’exécution (navigation file:// et localhost bloquée par l’administrateur). **Ne pas affirmer qu’une recette mobile/JS en navigateur a été validée dans cette étape.**

## 4. Liste de tests humains avant un éventuel basculement

1. Ouvrir le lien de démonstration sur ordinateur, Android et Safari iPhone, vérifier le chargement et l’absence de débordement horizontal.
2. Vérifier menu mobile, barre QCM, recherche par mots-clés, filtres par thème, et absence d’erreurs JavaScript.
3. Cliquer sur tous les QCM ; confirmer que chaque page officielle s’ouvre et qu’un retour est possible.
4. Contrôler la lisibilité, les contrastes, le focus clavier et la navigation sur écran tactile.
5. Exécuter Lighthouse/PageSpeed et vérifier les performances et la politique d’indexation ; conserver `noindex` pour la bêta.
6. Effectuer la revue éditoriale des titres, des chiffres, de chaque statut de pilier, et valider le périmètre des contenus.
7. Pour une mise en production ultérieure, prévoir URL canonique, métadonnées SEO, sitemap et navigation interne sans liens de test.

## 5. Retour arrière et gouvernance

- **Le domaine officiel continue de pointer vers l’état antérieur du site.** Aucun retour arrière n’est nécessaire tant que la bêta n’est pas fusionnée/déployée.
- Conserver la branche `main` et son historique Git intacts ; consulter la branche de prévisualisation séparée.
- En cas de problème sur la bêta, retirer le lien de démonstration des communications, ou restaurer la branche de prévisualisation à son commit précédent.
- Toute publication future sur le domaine officiel sera une opération distincte, après tests et validation explicite ; consigner le SHA Git exact d’avant et d’après déploiement.
- Archiver toute version remplacée selon le guide V6 officiel, sans suppression.

## 6. Prochaine étape recommandée

Recette visuelle et ergonomique de la prévisualisation, correction des liens manquants lorsque les pages existent, puis conception d’un hébergement de préproduction de première partie (GitHub Pages indépendant ou équivalent) sans risque de modifier la production.
