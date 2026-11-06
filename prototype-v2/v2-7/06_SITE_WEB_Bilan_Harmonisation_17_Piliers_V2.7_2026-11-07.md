# Doctrine Éconologique — Bilan d’harmonisation V2.7

**Date : 7 novembre 2026**  
**Statut : prépublication non indexée ; production inchangée**  
**Branche :** `preview-v27-2026-11-07`, créée à partir de `preview-v26-2026-11-07`.  
**Demande de fusion :** https://github.com/jeanpaulpoignand-web/doctrine-econologique-site/pull/22  
**Lien de prévisualisation :** https://raw.githack.com/jeanpaulpoignand-web/doctrine-econologique-site/preview-v27-2026-11-07/index.html  
**Catalogue des 17 piliers :** https://raw.githack.com/jeanpaulpoignand-web/doctrine-econologique-site/preview-v27-2026-11-07/piliers/index.html

## 1. Périmètre réel

L’inventaire du site recensait **15 pages de piliers existantes (I à XV)**. Deux numéros ne comportent pas encore de page publiée : **XVI — Autoroutes et fin des concessions** et **XVII — Propreté publique et responsabilité du déchet**. Ils restent visibles au catalogue sous le libellé **« en chantier »**, sans page ni contenu fictifs. Le Pilier **XIV — Amortissement de la dette** conserve sa mention **« non audité »**.

La V2.7 harmonise les 15 pages existantes et le catalogue, sans toucher aux neuf questionnaires ni au moteur du Bulletin citoyen hérités de la V2.6.

## 2. Charte appliquée

Nouvelle feuille de style **`assets/pilier-charte-v27.css`** : fond crème, typographie éditoriale Cormorant Garamond / IBM Plex Sans, titres bleu nuit, accents terracotta, tableaux lisibles avec défilement horizontal dans leur seul conteneur, cartes chiffrées claires, repères méthodologiques discrets mais visibles, liens et focus clavier contrastés, mise en page responsive. Une classe CSS est ajoutée à chaque page : `pilier-v27` ou `piliers-index-v27`. Le catalogue importe également le script de navigation, strictement limité à la prépublication.

La navigation d’essai utilise un routage propre à `preview-v27-2026-11-07` pour conserver les visiteurs sur le miroir RawGitHack. La V2.7 reste **non indexée** dans ce contexte. Toute publication définitive devra utiliser une procédure distincte et les métadonnées SEO de la version officielle.

## 3. Contrôles et résultats

**Contrôle d’intégrité — SUCCÈS.** Le workflow GitHub vérifie les **16 fichiers HTML** (15 pages + index), octet à octet par rapport à la branche V2.6 après retrait exclusif des ajouts autorisés de CSS, d’imports de polices et de navigation. Les textes, qualifications `[FAIT]`, `[CALCUL]`, `[HYPOTHÈSE]`, données chiffrées, sources, liens, titres H1/H2/H3, canonicals et métadonnées SEO demeurent donc inchangés.

**Recette navigateur Chromium — SUCCÈS** sur **1440 × 900** et **390 × 844** : accueil, catalogue des neuf QCM, catalogue des 17 piliers, accès aux 15 pages, vérification du statut des deux chantiers et du Pilier XIV, présence du H1, canonical, CSS, `noindex` du miroir, chargement des ressources, absence d’exception JavaScript et de débordement horizontal détecté.

**Contrôle externe HTTP — SUCCÈS :** réponses HTTP 200 pour l’accueil V2.7, le catalogue, le Pilier 1, le Pilier XIV et le Bulletin citoyen.

**GitHub Actions :** https://github.com/jeanpaulpoignand-web/doctrine-econologique-site/actions/runs/42314595678

## 4. Contrôle visuel

Captures Chromium réelles examinées pour le Pilier 1 (ordinateur et mobile), le catalogue des 17 (ordinateur et mobile), ainsi que d’autres piliers représentatifs (VII, XIV, XV). Le catalogue affiche 15 cartes liées vers les pages et deux cartes de chantier non liées.

Les captures complètes et les résultats de recette sont archivés séparément au format ZIP dans le dossier Google Drive officiel.

## 5. Limites et prochaine décision

- **Safari sur iPhone réel : non vérifié pour la V2.7** ; l’utilisateur avait validé la V2.6 sur iPhone, ce qui ne remplace pas la validation V2.7.
- La recette vérifie la navigation, le rendu et la préservation des contenus ; elle **ne constitue pas un nouvel audit documentaire** des chiffres ou des positions doctrinales.
- Le Pilier XIV demeure non audité, les Piliers XVI et XVII non publiés ; leur rédaction n’entre pas dans le périmètre de la V2.7.
- **Aucun déploiement vers `main`** : la prépublication porte volontairement la balise `noindex`, un routage de miroir et une identité de test. Avant la production, restaurer les métadonnées SEO, schema.org, Search Console, Open Graph, canonicals et contrôles de Grégoire, puis soumettre une PR de publication distincte à autorisation explicite.

## 6. Conclusion

**Harmonisation des 15 pages disponibles et du catalogue des 17 achevée, contrôles d’intégrité et Chromium réussis.** Le prochain jalon est la validation visuelle sur l’iPhone de l’utilisateur. Les fichiers `main` sont restés inchangés.
