# Doctrine Éconologique — Prépublication du site V2.6

**Date :** 7 novembre 2026  
**Statut :** maquette navigable, branche de prépublication, non indexée — pas de publication sur `main`.  
**Branche :** `preview-v26-2026-11-07`  
**GitHub (PR brouillon, cible hors production) :** https://github.com/jeanpaulpoignand-web/doctrine-econologique-site/pull/21  
**Prévisualisation proposée :** https://raw.githack.com/jeanpaulpoignand-web/doctrine-econologique-site/preview-v26-2026-11-07/index.html

## Périmètre intégré

- Accueil V2.3 validé : reprise à la racine de la prépublication, typographie, couleurs et structure conservées. Titre et description adaptés à la prépublication ; `noindex,nofollow` conservé.
- Catalogue des neuf questionnaires, harmonisé avec la charte de l'accueil.
- Neuf QCM fonctionnels déjà harmonisés en V2.4/V2.5, sans retouche supplémentaire de leurs moteurs : Général (10 questions), Énergie (19), ASPA, Bâtiment/Pilier VI, Textile, Frontaliers, Fraude fiscale, Consigne mégots, Bulletin citoyen (12 questions et 15 formations).
- Script de routage de la branche d'essai ajouté à `assets/doctrine-share.js` ; il ne s'active que sur `raw.githack.com` et quand le chemin contient exactement `preview-v26-2026-11-07`. Il transforme les liens internes vers `/index.html`, ajoute un bandeau discret de prépublication, et une balise `noindex,nofollow` dans le DOM des pages ouvertes.
- Le reste du site, notamment les pages des piliers, est inchangé dans le périmètre de ce lot.

## Contrôles automatiques

- `tests/test_preview_v26.py` : parcours accueil → QCM Énergie → accueil → catalogue, liens vers les neuf QCM, présence des assets, indexation bloquée, exceptions JavaScript, débordement horizontal ; rendu 1440 × 900 et 390 × 844.
- Le test de navigation simule l'origine RawGitHack en servant **les fichiers réels de la branche par interception Playwright**. Cela démontre l'intégrité de l'arborescence et du routage, mais **n'est pas à lui seul une preuve d'accessibilité CDN depuis tous les appareils**.
- Les suites antérieures des huit QCM et du Bulletin citoyen ont été exécutées et sont vertes sur les branches de travail antérieures ; voir PR n°17 à 20 et leurs journaux.
- **Contrôle d'accessibilité externe de RawGitHack :** réussi depuis un runner GitHub Actions. Réponses HTTP 200 avec `Content-Type: text/html` pour `index.html`, `questionnaires/index.html`, `qcm-general/index.html` et `qcm-democratie-decisionnelle/index.html`. Les cinq autres QCM ont été validés dans le miroir de navigation et non contrôlés individuellement sur le CDN.
- **Résultat de la recette V2.6 actualisée :** SUCCESS — desktop et mobile, accès accueil → QCM Énergie → retour accueil → catalogue → neuf questionnaires ; assets présents, `noindex` effectif, aucune exception JavaScript détectée, aucun débordement horizontal. Workflow : https://github.com/jeanpaulpoignand-web/doctrine-econologique-site/actions/runs/42312771288 .

## Risques et garde-fous

- La branche `main` du site officiel n'a pas été modifiée par ce lot.
- Ne **jamais fusionner telle quelle** cette prépublication sur `main` : sa page d'accueil porte volontairement `noindex` et elle contient un routeur de démonstration.
- Pour la publication finale, créer une branche de livraison séparée, restaurer ou adapter proprement les métadonnées SEO des audits Grégoire (`title`, `description`, `canonical`, OG/Twitter, Search Console, sitemap et données structurées). Le site officiel doit rester indexable.
- Safari sur iPhone réel, réseau de distribution du site, performance, accessibilité approfondie et validation humaine restent à effectuer.
- Aucun logo Grok non validé ni emblème « République française » n'est utilisé dans cette prépublication.

## Retour arrière

La production reste sur `main`. Retirer la branche `preview-v26-2026-11-07` n'entraîne aucune modification du site public ni des moteurs des QCM.