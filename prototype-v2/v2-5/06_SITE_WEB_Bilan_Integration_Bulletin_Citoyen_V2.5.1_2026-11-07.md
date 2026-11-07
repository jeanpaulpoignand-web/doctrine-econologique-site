# Doctrine Éconologique — Bulletin citoyen
## Bilan d’intégration visuelle V2.5.1 — 7 novembre 2026

### Statut
**Prototype fonctionnel validé sur branche de travail, non publié.**

Dépôt : `jeanpaulpoignand-web/doctrine-econologique-site`
Branche : `design/bulletin-citoyen-charte-v2-5-2026-11-07`
Pull request : https://github.com/jeanpaulpoignand-web/doctrine-econologique-site/pull/20
Branche officielle `main` non modifiée.

### Origine du design
- Conservation de la ligne d’accueil V2.3 : fond crème, texte bleu nuit, accent terracotta, typographies Cormorant Garamond et IBM Plex Sans.
- Reprise du principe de la charte QCM V2.4 : question lisible en priorité, sources et détails au second plan.
- Réduction des animations incitatives, suppression du doigt clignotant et des effets d’enfoncement automatiques sur les cartes de choix.
- Accueil, parcours des 12 questions, curseurs, modale d’aide, vote par parti (15 formations), classement, remise à zéro, cinq questions complémentaires, mode futur et vues 390 px rendus avec le même système graphique.
- Aucune adoption de logo ni de marque institutionnelle ; identité citoyenne et transpartisane conservée.

### Périmètre réel des modifications
- Nouveau fichier `assets/bulletin-citoyen-v25.css`, surcouche de styles strictement ciblée sur `body.bulletin-v25`.
- Dans `qcm-democratie-decisionnelle/index.html`, uniquement deux insertions : la classe `bulletin-v25` sur `<body>` et le lien vers la feuille CSS.
- Vérification GitHub Actions `tests/check_bulletin_v25_integrity.py` : **PASS** ; après retrait des deux insertions, l’intégralité du HTML correspond octet pour octet à `main`. Il en découle que le moteur JavaScript, les 12 questions, 15 matrices des partis, indices de confiance, sources, liens, titres, balises SEO et avertissements restent intacts.

### Recette navigateur réelle
Workflow : https://github.com/jeanpaulpoignand-web/doctrine-econologique-site/actions/runs/42310912021
Résultat : **SUCCESS** — Chromium, vues ordinateur 1440×900 et mobile 390×844.
- Accueil : affichage, charte chargée, titres et couleur de fond, aucun débordement horizontal.
- Parcours complet de 12 questions : 9 positions saisies sur curseur, 3 choix « Sans avis », résultat après la dernière question.
- Affichage des formations classées, ouverture des 15 formations et des sources détaillées, absence d’erreurs JavaScript détectées.
- Modale « Avant de voter, je veux en savoir plus » : ouverture et fermeture clavier.
- Modification des réponses, annulation puis confirmation de remise à zéro.
- Entrée « vote par parti » : les 15 cartes sont présentes, un choix est affiché.
- Mode futur : explication des valeurs fictives et interface accessible.
- Captures réelles de l’accueil, première question, aide, résultat et vote classique sur ordinateur et mobile.
- Contrôles automatiques des 8 autres QCM V2.4 également **SUCCESS** sur la même branche (non-régression et recette navigateur).

### Principales corrections grâce aux captures
- Navigation mobile placée en grille de deux colonnes plutôt qu’en quatre lignes.
- Bouton d’aide réduit à une hauteur normale sur mobile (ancien défaut de flex-basis vertical).
- Encadré « cinq questions complémentaires » passé en fond crème, avec texte contrasté et pastilles discrètes.

### Limites et décisions reportées
- Les captures Chromium ne remplacent pas une recette Safari iOS native, une vérification complète lecteur d’écran ou un audit de performance et de contraste exhaustif.
- Les données des partis, leur actualisation documentaire, et les ratios de score n’ont pas été réévalués : c’est une rénovation **visuelle** uniquement.
- Les titres et métadonnées ont été conservés sans optimisation éditoriale supplémentaire ; la charte graphique n’a pas à modifier les critères SEO de Grégoire.
- Les trois PR de V2.4 (#17, #18, #19) et celle de V2.5 (#20) forment une chaîne de travail ; ne pas fusionner en production sans recette de bout en bout et accord du propriétaire.
- Le contenu statique « Ce que dit le pilier » est conservé à la fin de chaque écran, sans dissimulation de données SEO.

### Livrables
- CSS V2.5.1 sauvegardée sur Google Drive.
- Code et tests versionnés sur GitHub.
- Captures et archive ZIP sauvegardées sur Google Drive avec la même nomenclature.