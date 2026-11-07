# Doctrine Éconologique — V2.4 — Intégration graphique des deux QCM pilotes

Date : 6 novembre 2026. Responsable de l'intégration : ChatGPT. Statut : **branche d'essai uniquement — NON PUBLIÉ**.

## Décision

Conserver uniquement les apports graphiques probants de Grok : palette crème/bleu nuit/terracotta, typographie de l'accueil V2.3, cartes de réponses lisibles, progression sobre, sources et méthode disponibles mais visuellement discrètes. Rejeter les images dites « réelles » qui ne correspondent pas au HTML, les allégations non prouvées d'anonymat/sécurité, les décomptes erronés et la référence à la République française. **Ne pas installer de logo sans validation du propriétaire.** Le vrai SVG n°1, monogramme DÉ, reste une piste provisoire, non adoptée.

## Base de code, dépôt et nomenclature

Dépôt : `jeanpaulpoignand-web/doctrine-econologique-site`

Branche isolée créée depuis `main` : `design/qcm-fusion-fonctionnelle-v2-4-2026-11-06`

Fichiers modifiés/ajoutés sur cette seule branche :

- `assets/qcm-charte-v24.css` (nouveau, 11 458 caractères, base commune, ciblée par classes CSS)
- `qcm-general/index.html` (uniquement classe `<body>` + lien CSS)
- `qcm-energie/index.html` (classe `<body>`, lien CSS, mise en accordéon de deux blocs techniques préexistants)
- `prototype-v2/v2-4/06_SITE_WEB_Journal_Integration_Charte_QCM_V2.4_2026-11-06.md` (journal de preuve)

**Aucun texte de question, proposition de réponse, règle de score, variable de calcul, script JavaScript, titre SEO, meta description, canonical, Open Graph, lien HTML ou balisage H1/H2/H3 n'a été remplacé.**

## Contrôle de non-régression effectué sur les fichiers GitHub

Comparaison de chaque fichier de la branche avec son original `main` :

| Contrôle statique | QCM général | QCM Énergie |
|---|---|---|
| Scripts JavaScript identiques, octet pour octet dans les éléments `<script>` | OUI | OUI |
| Balises `<title>`, H1/H2/H3 identiques | OUI | OUI |
| Balises meta et liens SEO identiques (hors nouvelle feuille CSS) | OUI | OUI |
| Liens HTML existants identiques | OUI | OUI |
| Feuille CSS partagée correctement référencée | OUI | OUI |
| Outils de validation repliés dans un `details` | Sans objet | OUI |
| Note méthodologique des résultats repliée dans un `details` | Sans objet | OUI |
| Source `main` inchangée | OUI | OUI |

Empreintes d'origine observées : général `7aacbf43dde99541920fe1081f78df3a11f58fa8`, énergie `5fff8e31a46dbe2f62f87e596dd5c09ea5f7dd4b`. Accueil `main` toujours `06727f1a89d957f3d854effadc2dfb75bdd99978`.

Feuille CSS : analyse syntaxique de 93 règles sans erreur. Un rendu **de démonstration avec HTML simplifié** (pas le vrai QCM) a été vérifié à 1440 px et 390 px par Chromium : fond et sélection conformes ; aucun défilement horizontal. Cette démonstration n'est **pas** une recette fonctionnelle du code complet.

## Reste à vérifier avant toute publication

- Rendu réel des deux pages complètes, sur téléphone et ordinateur, avec ressources locales résolues ; l'environnement de navigateur ne permettait pas de consulter les vraies pages de la branche.
- Parcours interactifs des 10 questions et 19 questions, modes rapide/pédagogique, marche arrière, redémarrage, résultat et calcul des profils ; un script intact rend la régression moins probable, mais ne prouve pas l'absence de défaut de présentation.
- Navigation et affichage de l'accordéon, capacité à suivre les liens vers 19 fiches, clavier et lecture d'écran, contraste/zoom 200 %, états des réponses, PageSpeed et référencement après déploiement.
- Validation humaine de la nouvelle charte avant tout déploiement sur `main`.

## Garde-fous SEO de Grégoire

Ne jamais modifier les URL publiées, les balises title/description/canonical, le sitemap, les H1/H2/H3, le nom de l'auteur responsable ni les liens vers les sources. Conserver les textes probants dans le HTML sous un accordéon, pas dans une injection JavaScript indexable incertaine. Ne pas diffuser les prototypes comme pages indexables.

## Retour arrière

Aucune action sur la branche `main`. Pour annuler la V2.4, abandonner la branche d'essai : les deux QCM publics et tous leurs fichiers sont inchangés. Pas de remplacement de fichier existant dans le Drive.
