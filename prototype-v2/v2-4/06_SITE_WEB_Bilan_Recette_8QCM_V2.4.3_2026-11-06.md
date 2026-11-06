# Doctrine Éconologique — V2.4.3 — Bilan de refonte graphique des QCM

**Date : 6 novembre 2026 · Statut : préproduction, non publiée · Responsabilité intégration : ChatGPT**

## Objectif atteint

Huit questionnaires existants ont reçu une présentation harmonisée avec la V2.3, sur un enchaînement de branches GitHub **hors `main`** :

1. QCM général — 10 questions ;
2. QCM Énergie — 19 questions ;
3. QCM ASPA ;
4. QCM Pilier VI — Bâtiment ;
5. QCM Textile ;
6. QCM Fraude fiscale ;
7. QCM « Immigrants de la journée » — Frontaliers ;
8. QCM Consigne mégots (directive `noindex, follow` préservée).

**À traiter séparément :** Bulletin citoyen / Démocratie décisionnelle (application politique complexe). Le système visuel ne couvre pas encore toutes les pages des piliers ni la publication de l'accueil V2.3.

## Provenance et choix graphiques

Reprise des éléments utiles de Grok V2.4.2 : crème, bleu nuit, terracotta, Cormorant Garamond, IBM Plex Sans, cartes de réponses, navigation accessible, panneaux méthodologiques discrets. Écartés : faux emblèmes institutionnels, captures non conformes aux HTML, logos non approuvés.

Feuilles de style versionnées :
- `assets/qcm-charte-v24.css` — thème partagé ;
- `assets/qcm-charte-v24-classic.css` — ASPA, Bâtiment et Textile ;
- `assets/qcm-charte-v24-special.css` — Fraude, Frontaliers et Consigne mégots.

## UX et visibilité

- Liens de navigation Drive corrigés pour leur contraste.
- Barre de navigation mobile arrangée sur deux colonnes au lieu de quatre boutons empilés (largeur testée : 390 px).
- QCM général : « Repères et sources » fermé par défaut ; ce **seul changement mineur de JavaScript** est autorisé par le test de non-régression, sans modifier les calculs.
- QCM Énergie : les 19 fiches d'aide et les détails méthodologiques sont accessibles dans des volets repliables ; outils de simulation interne dépriorisés, mais conservés.
- Aucun nouveau logo adopté et aucune affiliation gouvernementale suggérée.

## Contrôles réels, 6 novembre 2026

**Tests statiques GitHub Actions : SUCCÈS** — exécution n° `42308870461` sur commit `6563acf307a31ba0688cdcf9d96aff8a21b0bf4a`.

Comparaison des 8 pages avec la production `main` : blocs JavaScript inchangés, sauf une seule variation d'ouverture du panneau documentaire explicitement autorisée ; titres H1/H2/H3, balises `<title>`/`meta`/`canonical` et liens `a[href]` inchangés ; feuille CSS liée uniquement sur les pages ciblées ; chaque page conserve un seul H1.

**Recette navigateur Chromium : SUCCÈS** — exécution n° `42308870536` sur le même commit.

- Les 8 pages s'ouvrent en HTTP local, avec titre H1 unique, charte CSS active, sans exception JavaScript détectée.
- QCM général : parcours des 10 réponses en mode rapide, écran de résultats obtenu, captures réelles de l'accueil, de la question et des résultats.
- QCM Énergie : parcours des 19 réponses en mode rapide, écran de résultats obtenu, captures réelles de l'accueil, de la question et des résultats.
- Mobile à 390 px : accueil QCM général, QCM Énergie et ASPA ; absence de débordement horizontal constatée.
- Neuf captures d'écran réelles ont été produites et archivées en ZIP via GitHub Actions, artefact n° `13546844361`.

**Limites des tests :** les questionnaires ASPA/Bâtiment/Textile/Fraude/Frontaliers/Consigne ont été contrôlés à l'ouverture mais pas encore parcourus jusqu'au résultat dans ce test automatisé ; les modes approfondis, tous les liens externes, l'accessibilité lecteur d'écran et les Core Web Vitals n'ont pas été certifiés. Il s'agit d'une validation **de préproduction**, non d'une recette exhaustive.

## GitHub : trois PR brouillon, aucune publication

- PR n°17 : https://github.com/jeanpaulpoignand-web/doctrine-econologique-site/pull/17 — QCM Général + Énergie vers `main`, **DRAFT**.
- PR n°18 : https://github.com/jeanpaulpoignand-web/doctrine-econologique-site/pull/18 — ajout ASPA, Bâtiment, Textile vers la branche pilote, **DRAFT**.
- PR n°19 : https://github.com/jeanpaulpoignand-web/doctrine-econologique-site/pull/19 — ajout Fraude, Frontaliers, Consigne, tests navigateur, **DRAFT**.

Les PR sont emboîtées : aucun merge ne doit se faire aveuglément ou hors ordre. Le site officiel `main` reste inchangé.

## Décision de conduite

**Ne pas publier maintenant.** Conserver les versions historiques. Avant validation humaine : tester modes approfondis et les six autres moteurs au-delà de la première page, compléter l'audit mobile/lecteur d'écran, revoir les grands tableaux de résultats ; isoler l'harmonisation du Bulletin citoyen dans une branche distincte. La publication de l'accueil V2.3 exigera de restaurer l'ensemble des métadonnées SEO signalées par Grégoire et de vérifier le domaine canonique.