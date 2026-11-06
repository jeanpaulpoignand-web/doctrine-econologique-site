# DOCTRINE ÉCONOLOGIQUE — SITE WEB
## Journal de décisions et protocole de retour arrière — V2.0 — 6 novembre 2026

**Statut : PROTOTYPE À VALIDER — NON PUBLIÉ.**

**Classement officiel** : `[DOCTRINE] Éconologique — Souveraineté Française / 06 — 🟣 SCRIPTS_TECHNIQUES — Apps Script / 01 — 🌐 SITE_WEB — Refonte UX-SEO-QCM — V2 — 2026-11-06`.

### 1. Objet
Fusionner l'élégance éditoriale suggérée par Grok (typographies, bleu nuit et or, rythme de lecture) avec une interface orientée citoyens, par questions du quotidien et accès immédiat aux QCM. **Aucun changement du contenu de la Doctrine ou des réponses aux QCM.** La démarche est une contribution citoyenne indépendante et transpartisane.

### 2. Sources analysées
- Audit Grok du 6 novembre 2026 : https://docs.google.com/document/d/1SEErGJ-G4NfSB9u0jZOWCt93Uv-dyJcjEqmfz-AP6vY/edit
- Prototype HTML Grok « Vision Livre » : https://drive.google.com/file/d/1gq28cURbNHTMRWSNUp1syGmwx3w9iomT/view
- Audit UX Grok du 19 octobre 2026 : https://docs.google.com/document/d/18kWydbjX-b9hK2uMHd1YsX-bOquW7AH3rvwysT-dLw0/edit
- Guide officiel de la Doctrine V6, révision du 7 octobre 2026 : https://drive.google.com/file/d/1TLdzH_czwB4eABeAPr7uqCS_cbA8MPA5/view
- Site actuellement publié : https://doctrine-econologique.fr/
- Code source de production : https://github.com/jeanpaulpoignand-web/doctrine-econologique-site (branche `main`, **ne pas remplacer sans validation**).

### 3. Contenu du prototype V2
- Accueil par préoccupations concrètes (énergie, réparation, grand âge, fiscalité).
- Navigation par 4 thèmes, recherche locale, 17 dossiers (les piliers XVI–XVII sont indiqués comme sans lien de dossier à ce stade).
- Section QCM prioritaire, contenant un lien vers le bulletin citoyen, le QCM général et l'index des questionnaires.
- Liens QCM complémentaires sur les cartes où ils existent dans la page d'accueil actuelle (I, IV, VI, VIII, X, XIII, XV, XVII).
- Barre inférieure d'accès Accueil / Sujets / QCM sur mobile.
- Accès aux méthodes et aux catégories de preuve [FAIT], [CALCUL], [HYPOTHÈSE], [PROPOSITION].
- Prototype muni volontairement de `robots: noindex,nofollow` : pas de publication ni d'indexation d'une maquette incomplète.

### 4. Vérifications exécutées
- 17 cartes thématiques présentes.
- 3 cartes d'entrée QCM et 8 liens QCM thématiques.
- Absence de débordement horizontal vérifiée en 1440×900 et 390×844 dans Chromium.
- Tests à compléter : inspection des URLs de tous les QCM, clavier et lecteurs d'écran, performances réelles, liens internes, navigation iOS/Safari, réglages SEO de production et données structurées.

### 5. SEO pour version de production (PAS encore activé)
- Conserver les chemins d'URL et les références déjà indexées.
- Retirer `noindex,nofollow` **uniquement** après validation de la page destinée à remplacer l'accueil.
- Préserver ou réviser avec soin canonical, titles, meta descriptions, Open Graph, `lang="fr"`, sitemap, robots.txt.
- Rendre l'information critique présente dans le HTML indexable; conserver un lien HTML explicite vers le répertoire QCM.
- Ajouter les descriptions et données structurées seulement quand elles correspondent au contenu réel des pages.
- Réduire les dépendances aux ressources externes, préserver Core Web Vitals et contraste.
- Analyser les parcours QCM avec mesure respectueuse de la vie privée, sans mécanisme manipulateur.

### 6. Retour arrière / publication contrôlée
1. Conserver **intacte** la branche GitHub de production `main`.
2. Enregistrer le prototype dans une branche dédiée et dans le présent dossier Drive; ne pas modifier l'URL publique.
3. Vérifier l'aperçu téléchargé et faire valider le design.
4. Avant toute fusion vers `main`, enregistrer l'identifiant du commit stable et un export/snapshot du code concerné.
5. Publier seulement après validation écrite; en cas de problème, revenir au commit stable par un nouveau commit de restauration ou un revert, sans réécrire l'historique.
6. Les versions remplacées sont archivées selon le guide : dossier `90 — ⚫ ARCHIVES`, avec mention `⚠️ SUPERSEDÉ` et date; ne jamais supprimer une ancienne version.

### 7. Règle de classement permanente
Chaque version doit comporter : **code de section + objet + IA/contributeur si pertinent + version + date ISO**. Exemples :
- `06_SITE_WEB_Prototype_Fusion_Grok_ChatGPT_UX_SEO_QCM_V2.0_2026-11-06.html`
- `06_SITE_WEB_Journal_Decisions_Refonte_UX_SEO_QCM_V2.0_2026-11-06.md`
- `06_SITE_WEB_Apercu_desktop_V2.0_2026-11-06.png`

**État final de cette étape : démonstration en cours, site public préservé.**
