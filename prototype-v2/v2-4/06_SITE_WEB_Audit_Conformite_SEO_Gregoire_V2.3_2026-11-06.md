# DOCTRINE ÉCONOLOGIQUE — AUDIT DE CONFORMITÉ SEO À LA RÉFÉRENCE GRÉGOIRE

**Date :** 6 novembre 2026  
**Auteur du contrôle :** ChatGPT (audit documentaire et statique, sans publication)  
**Objet :** vérifier que la refonte visuelle V2.3 ne fait pas perdre les critères SEO du guide externe Grégoire.  
**Statut :** audit de code et de documents ; **ne vaut pas crawl HTTP, mesure Search Console ou mesure Lighthouse**.

## Sources examinées

1. Audit externe de Grégoire, 2 novembre 2026 : « Guide SEO pour le site Doctrine éconologique » — Google Drive : https://drive.google.com/file/d/10l-1IZEo9IE_tlAfDfk0U31gJEDq_zcx/view
2. « 00_Audit_SEO_Site_Doctrine_Econologique » — Google Docs : https://docs.google.com/document/d/14c_N2-g2V9VwuH0BXwWw4qjLpppZSuVpXEnau4is5xU/edit (l'attribution de ce second document à Grégoire n'est pas établie par le document lui-même).
3. Rapport technique daté du 6 novembre 2026 — https://docs.google.com/document/d/11QfUWRcMuEWt_oWbypiXW5tfhbV7dJvt55K_EM6UhZ4/edit ; utile pour distinguer les défauts du 2 novembre déjà corrigés.
4. GitHub, dépôt `jeanpaulpoignand-web/doctrine-econologique-site`, branche `main`, `index.html`, blob SHA `06727f1a89d957f3d854effadc2dfb75bdd99978`.
5. GitHub, branche `preview-v23-2026-11-06`, `prototype-v2/v2-3/index.html`, blob SHA `7481cb5b3a3fb630bf9df9119a51c58108eb5f22`.
6. Google Search Central, génération des liens de titre : https://developers.google.com/search/docs/appearance/title-link ; guide SEO : https://developers.google.com/search/docs/fundamentals/seo-starter-guide ; noindex : https://developers.google.com/search/docs/crawling-indexing/block-indexing.

## Résultat principal

- **La version de production n'a pas été modifiée par la refonte.** Le fichier `main/index.html` a toujours le blob SHA de référence `06727f1a89d957f3d854effadc2dfb75bdd99978`. La V2.3 vit dans des branches et sous-dossiers séparés.
- **La V2.3 est une maquette et n'est pas prête à remplacer `main/index.html` à l'identique.** Les oublis ci-dessous sont sans conséquence sur le domaine actuellement publié, mais doivent être corrigés avant toute fusion vers la production.
- **La taille du titre n'est pas la source principale du risque SEO.** Le H1 principal est unique et très visible dans les deux versions. Google ne prescrit aucun nombre de pixels minimum pour être classé, mais utilise le titre visuel dominant et le H1 pour composer les liens de titre.

## Matrice de conformité

| Critère / exigence | `main` actuel | Maquette V2.3 | Verdict / action avant publication |
|---|---|---|---|
| `lang="fr"`, viewport | Oui | Oui | CONFORME |
| Titre principal visuel dominant | CSS H1 `clamp(38px,7vw,76px)` | CSS H1 `clamp(55px,6vw,88px)` | CONFORME ; seule la lisibilité réelle sur mobile reste à confirmer |
| H1 principal unique | 1 | 1 | CONFORME |
| H2 pour rubriques / H3 pour cartes | Oui | Oui (8 H2, 27 H3 relevés) | Globalement CONFORME ; vérifier la pertinence éditoriale des intitulés |
| `<title>` descriptif, durable, exploitable par Google | « Doctrine Éconologique : 17 piliers pour une France qui produit » | « Doctrine Éconologique — Prototype collaboratif V2.3 (non indexé) » | **À CORRIGER EN PRODUCTION** ; retirer « prototype », choisir un titre utile sans écraser la marque |
| `meta description` | Oui, orientée sujets de société | Oui mais décrit un « bêta non indexé » | **À CORRIGER EN PRODUCTION**, sans supposer une longueur obligatoire en caractères |
| Canonical auto-référente | `https://doctrine-econologique.fr/` | Absente | **OBLIGATOIRE AVANT FUSION** |
| Open Graph / partage | 10 balises `og:` | Aucune | **À RÉTABLIR** (`og:title`, `og:description`, `og:url`, image stable) |
| Balise Search Console de vérification | Présente sur `main` | Absente | **À PRÉSERVER** sur la future page d'accueil ; ne pas la perdre |
| JSON-LD / données structurées | Graphe `WebSite` + `Organization`, responsabilité humaine | `WebPage` minimal lié à `WebSite` | **À REPRENDRE / ADAPTER** : garder les données structurées véridiques et correctement liées |
| Auteur humain / responsabilité éditoriale | Oui dans le code actuel et pages dédiées | Nom non retrouvé dans la maquette | **À RÉTABLIR** en lien discret vers `À propos`, sans placer les cinq IA en lieu et place de l'auteur |
| Directives `robots` | Aucune directive bloquante sur l'accueil | `noindex, nofollow` | **NORMAL POUR LA BÊTA**, mais bloquant si la maquette remplaçait l'accueil indexable |
| Liens HTML vers piliers et QCM | Oui (17 liens piliers sur l'accueil et nombreux liens QCM) | Oui (17 thèmes, nombreux QCM) | CONFORME sur le principe ; contrôle exact des destinations nécessaire |
| Navigation interne dans le même onglet | Liens relatifs ; contenu interne navigué normalement | 35 liens vers `doctrine-econologique.fr` ouvrent un nouvel onglet | **À CORRIGER** lors de l'intégration sur le domaine officiel (liens relatifs et même onglet) |
| Pages de piliers réelles en HTML | Oui sur `main` pour 15 piliers ; d'autres pages annexes | La maquette renvoie à ces pages | **NE PAS LES REMPLACER** par la seule page d'accueil moderne |
| Sitemap / robots.txt / CNAME | CNAME `doctrine-econologique.fr`, robots.txt, sitemap de 85 URL | Pas de sitemap propre à cette maquette | **PRÉSERVER** ces fichiers et les 85 URL utiles ; vérifier les URLs supplémentaires avant changement |
| Fichiers d'essai privés | `_config.yml` exclut `archives/` et `tools/` | Maquette stockée sous `prototype-v2/`, chemin **non exclu** par `_config.yml` | **RISQUE DE FUITE SI MERGE SUR MAIN** : exclure explicitement `prototype-v2/` ou ne pas embarquer ces fichiers dans la publication |
| Performances / Core Web Vitals | Non testées ici | Non testées ici | À MESURER sur un vrai hébergement mobile (LCP, CLS, INP) |
| Indexation réelle dans Google | Non vérifiée dans cet audit | Non souhaitée pour la bêta | À contrôler uniquement via Search Console après validation de la version finale |

## Chronologie : ne pas suivre à la lettre un audit dépassé

- Le guide Grégoire du **2 novembre** relevait que les piliers n'avaient pas de pages HTML. **Ce constat est dépassé** : au **6 novembre**, le dépôt `main` contient des pages de piliers, ainsi que des pages de fiches et d'annexes. Le sitemap contient **85 URLs**.
- L'audit technique du 6 novembre confirme 85 URLs de sitemap et 7 fichiers HTML de publication intentionnellement exclus de l'index. Son auteur note explicitement l'absence de crawl HTTP complet.
- Les recommandations de Grégoire à conserver portent sur la clarté des titres, la navigation HTML, les pages de fond, la responsabilité éditoriale, les sources primaires, la prévention des contenus faibles et le suivi Search Console. Ne pas réintroduire les défauts déjà corrigés.

## À propos de la « taille des titres »

Google Search Central explique que le titre visuel dominant, le contenu de `<title>`, le premier H1 visible et d'autres textes proéminents peuvent servir à construire le titre du résultat. Il n'existe pas d'exigence officielle imposant un H1 de 60 ou 80 px. Le H1 de la V2.3 est déjà très visible (jusqu'à 88 px), plus grand que celui du site actuel (jusqu'à 76 px). La bonne exigence est une *hiérarchie visuelle et sémantique stable*, pas une compétition de tailles.

## Compatibilité avec la décision UX « preuves discrètes »

Conserver les textes factuels et la distinction entre faits, interprétations et propositions, mais ne pas répéter les badges techniques partout. Une section accessible « Sources et méthode » peut révéler les références et calculs au besoin. Ne jamais cacher une hypothèse déterminante d'un chiffre affirmé dans le texte principal. Les informations nécessaires à la compréhension doivent rester dans le HTML et être utiles à l'humain, pas ajoutées pour les robots.

## Consignes impératives avant toute publication du nouveau design

1. **Ne toucher ni au domaine ni à `main`** tant que les contrôles ne sont pas clôturés et validés humainement.
2. Créer une branche de préparation de publication depuis le `main` actuel, puis **porter l'apparence et les composants V2.3/V2.4** dans le système existant plutôt que remplacer la page actuelle en bloc.
3. Préserver 85 URL connues du sitemap, la structure actuelle des pages piliers/QCM, les canonicals, les données Open Graph, la balise de vérification Google, les données structurées valides, le contenu utile et les chemins de navigation.
4. Nettoyer les mentions « prototype / bêta / non indexée » sur les futures pages publiques, et retirer `noindex` uniquement après validation, **pas sur les prototypes**.
5. Conserver le contenu des QCM et tous leurs calculs intacts ; migration purement visuelle dans un premier temps.
6. Vérifier la continuité `accueil → pilier → QCM → résultats → sources`, puis inspecter les titres et les liens **sur les pages finales rendues**.
7. S'assurer que les fichiers de maquette et de travail sous `prototype-v2/` ne sont pas publiés par le build final ; revoir `_config.yml` ou les chemins du dépôt avant fusion.
8. Faire ensuite les tests de rendu SEO et accessibilité, ainsi que les mesures de performance et de Search Console ; consigner les résultats, ne pas les inventer.

**Conclusion :** design V2.3 pertinent et grandeur des titres appropriée ; audit SEO Grégoire respecté partiellement par la bêta, mais non prêt pour une publication par substitution. Le site actuellement publié reste préservé. Il faut conserver les acquis SEO existants lors de la refonte complète, en particulier sur les QCM et piliers.
