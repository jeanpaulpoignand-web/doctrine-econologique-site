# QCM 2007–2026 — Version V10

Application HTML statique prête pour GitHub Pages.

## Principe V10

La V10 remplace les documents explicatifs longs par des pages d’extraits ciblés :

- une question du QCM ;
- une fiche pédagogique courte ;
- un document V10 avec extraits ciblés ;
- des couleurs de lecture :
  - jaune = passage utile ;
  - rouge = passage décisif ;
- un lien vers l’original Drive pour contrôle ;
- un bouton retour vers la question du QCM.

Le texte source n’est pas réécrit. Les pages V10 servent à guider la lecture, pas à remplacer les originaux.

## Structure

```text
index.html
README.md

fiches/
  q1.html
  ...
  q10.html

documents/
  index.html
  q1-smic-net-pouvoir-achat.html
  q2-chomage-emploi-productif.html
  q3-pouvoir-achat-reel.html
  q4-energie-prix-racine.html
  q5-retraites-cotisants-soutenabilite.html
  q6-cout-vie-quotidienne.html
  q7-sante-financement-soins.html
  q8-securite-accueil-cohesion.html
  q9-reindustrialisation-emplois-territoires.html
  q10-souverainete-leviers-decision.html

sources/
  index.html
```

## Mise en ligne GitHub Pages

1. Décompresser le ZIP.
2. Déposer tout le contenu dans le dépôt GitHub.
3. Aller dans `Settings` → `Pages`.
4. Choisir `Deploy from a branch`.
5. Sélectionner `main` puis `/root`.
6. Cliquer sur `Save`.

## Point important

Les originaux Drive doivent rester partagés en mode :
“toute personne disposant du lien peut consulter”.
