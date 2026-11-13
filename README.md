# Doctrine Éconologique

**Un cadre pour une France souveraine, productive et durable.**

Doctrine Éconologique propose une vision économique, politique et sociétale nouvelle, fondée sur la réalité physique (énergie, matière, territoire) plutôt que sur les abstractions financières et les dogmes dominants. Elle repose sur six piliers fondamentaux : **énergie, industrie, réparation, transmission, justice sociale et vérité des coûts**.

**Site officiel** : [https://doctrine-econologique.fr/](https://doctrine-econologique.fr/)

---

## 🌍 Pourquoi la Doctrine Éconologique ?

Face à la désindustrialisation, à la perte de souveraineté énergétique, à l’explosion des fraudes et dettes, et à une écologie souvent déconnectée des réalités productives, ce projet propose une alternative concrète et chiffrée.

Il ne s’agit pas d’une énième idéologie, mais d’un **outil citoyen** : analyses approfondies, questionnaires interactifs (QCM) et documents sources pour reprendre le pouvoir par la connaissance.

### Les grands piliers
- **Énergie** : Sobriété, nucléaire, renouvelables pilotables et vérité des coûts.
- **Industrie et production** : Relocalisation, réindustrialisation, économie de la réparation.
- **Démocratie décisionnelle** : Outils pour une démocratie plus directe et compétente.
- **Fraude fiscale et financière** : Chiffrage et mécanismes de récupération.
- **Immigration et cohésion sociale** : Approche réaliste et humaniste.
- **Aspa et justice sociale** : Minimum vieillesse, protection et incitations au travail.

---

## ✨ Fonctionnalités du site

- Page d’accueil riche et pédagogique.
- **QCM interactifs** auto-correctifs sur les sujets clés.
- Documents sources (version V13 du manifeste).
- Design responsive élégant et accessible.

---

## 📁 Structure du repository


## Méthode de validation V2.8 — références de comparaison

Depuis le correctif de la PR #48, `tests/check_release_v28.py` compare **12 piliers et 5 pages de navigation et d'information à `origin/main`**, au lieu du preview du 7 novembre (`origin/preview-v27-logo-2026-11-07`). Il s'agit d'une dérogation distincte de l'exception textuelle du QCM Énergie.

### Les 12 piliers

- `piliers/energie-souveraine/index.html`
- `piliers/garantie-decennale/index.html`
- `piliers/financement-public/index.html`
- `piliers/grand-age-ehpad/index.html`
- `piliers/batiment-metiers-utiles/index.html`
- `piliers/econologie-culturelle/index.html`
- `piliers/frontaliers-capital-humain/index.html`
- `piliers/agriculture-alimentation/index.html`
- `piliers/democratie-decisionnelle/index.html`
- `piliers/amortissement-dette/index.html`
- `piliers/fraude-fiscale/index.html`
- `piliers/textile-habillement-chaussure/index.html`

### Les 5 pages

- `questionnaires/index.html`
- `piliers/index.html`
- `a-propos/index.html`
- `guide-de-lecture/index.html`
- `bulletin-arbitrage/index.html`

### Portée et limite de cette référence

Les révisions éditoriales des 8 et 13 novembre étaient déjà publiées sur main. Cette dérogation entérine donc l'état de main issu notamment des PR #45, #46 et #47 fusionnées avec une CI rouge ; elle ne valide pas rétroactivement ces fusions. Selon l'audit Claude du 13 novembre, les différences de parité constatées par rapport au preview concernent le JSON-LD (description et dateModified) et les titres H1-H3 ; le JavaScript fonctionnel des 12 piliers est identique au preview.

La comparaison porte sur les blocs `<script>` (y compris le JSON-LD), les titres H1-H3 et la balise canonical, pas sur l'intégralité du HTML. `origin/main` est une référence mobile, résolue au moment du checkout : après une fusion, ce contrôle seul ne peut plus détecter une régression déjà intégrée à main. Les contrôles SEO/Apple et les tests de navigateur complètent cette comparaison.

Les autres pages contrôlées par `assert_eq`, notamment les moteurs QCM, conservent la référence du preview, avec les exceptions précisément bornées dans le script. L'accueil et le Pilier IV suivent leurs contrôles spécifiques. Les gestionnaires `onclick` hors des blocs `<script>` ne sont pas couverts par la comparaison de parité.

Audit de référence : [Claude — Correction CI PR45/46/47, V1](https://docs.google.com/document/d/1eq_K9TLfvJHP4g5BTxZQP274WDkAS9Pnx4E098ulNKU/edit), commit audité `e88e57073c4379555f4d78d77f40b6a599e312c3`.
