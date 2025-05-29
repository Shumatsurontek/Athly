# 🚀 Configuration des Règles GitHub pour votre Projet

## 📋 Étapes d'Installation

### 1. Copier les Fichiers de Configuration

Copiez tous les fichiers créés dans votre projet existant :

```bash
# Dans votre projet langgraph-multiagent-poc
mkdir -p .github/ISSUE_TEMPLATE
mkdir -p .github/workflows

# Copiez les fichiers suivants :
# .github/CONTRIBUTING.md
# .github/pull_request_template.md
# .github/workflows/ci.yml
# .github/ISSUE_TEMPLATE/bug_report.yml
# .github/ISSUE_TEMPLATE/feature_request.yml
# frontend/.eslintrc.js (si vous avez un frontend)
# backend/pyproject.toml (mise à jour)
```

### 2. Configuration des Branch Protection Rules

#### Via l'Interface GitHub :

1. **Allez dans votre repo** → Settings → Branches
2. **Cliquez sur "Add rule"**
3. **Configurez pour la branche `main` :**
   - Branch name pattern: `main`
   - ✅ Require a pull request before merging
   - ✅ Require approvals: 2
   - ✅ Dismiss stale PR approvals when new commits are pushed
   - ✅ Require review from code owners
   - ✅ Require status checks to pass before merging
   - ✅ Require branches to be up to date before merging
   - Status checks: `CI/CD Pipeline`
   - ✅ Require linear history
   - ✅ Include administrators

4. **Configurez pour la branche `develop` :**
   - Branch name pattern: `develop`
   - ✅ Require a pull request before merging
   - ✅ Require approvals: 1
   - ✅ Require status checks to pass before merging

#### Via GitHub CLI (Alternative) :

```bash
# Protection pour main
gh api repos/:owner/:repo/branches/main/protection \
  --method PUT \
  --field required_status_checks='{"strict":true,"contexts":["CI/CD Pipeline"]}' \
  --field enforce_admins=true \
  --field required_pull_request_reviews='{"required_approving_review_count":2,"dismiss_stale_reviews":true}' \
  --field restrictions=null

# Protection pour develop
gh api repos/:owner/:repo/branches/develop/protection \
  --method PUT \
  --field required_status_checks='{"strict":true,"contexts":["CI/CD Pipeline"]}' \
  --field enforce_admins=false \
  --field required_pull_request_reviews='{"required_approving_review_count":1}' \
  --field restrictions=null
```

### 3. Configuration des Labels

Créez les labels nécessaires :

```bash
# Via GitHub CLI
gh label create "bug" --color "d73a4a" --description "Something isn't working"
gh label create "enhancement" --color "a2eeef" --description "New feature or request"
gh label create "needs-triage" --color "fbca04" --description "Needs initial review"
gh label create "frontend" --color "0052cc" --description "Frontend related"
gh label create "backend" --color "5319e7" --description "Backend related"
gh label create "documentation" --color "0075ca" --description "Documentation"
gh label create "good first issue" --color "7057ff" --description "Good for newcomers"
gh label create "help wanted" --color "008672" --description "Extra attention is needed"
gh label create "priority:high" --color "b60205" --description "High priority"
gh label create "priority:medium" --color "fbca04" --description "Medium priority"
gh label create "priority:low" --color "0e8a16" --description "Low priority"
```

### 4. Configuration des Environments

1. **Allez dans** Settings → Environments
2. **Créez l'environment "production" :**
   - Protection rules: Required reviewers (ajoutez les admins)
   - Deployment branches: Selected branches → `main`

### 5. Adaptation du CI/CD

Modifiez le fichier `.github/workflows/ci.yml` selon votre structure :

```yaml
# Adaptez les chemins selon votre projet
backend:
  - 'poc/**'
  - 'core/**'
  - 'requirements*.txt'
  - 'pyproject.toml'
```

### 6. Configuration des Secrets

Ajoutez les secrets nécessaires dans Settings → Secrets and variables → Actions :

```bash
# Exemples de secrets à configurer
CODECOV_TOKEN=your_codecov_token
DATABASE_URL=your_test_database_url
API_KEY=your_api_key
```

### 7. Mise à Jour du README

Ajoutez des badges à votre README.md :

```markdown
# Votre Projet

[![CI/CD](https://github.com/username/repo/workflows/CI%2FCD%20Pipeline/badge.svg)](https://github.com/username/repo/actions)
[![codecov](https://codecov.io/gh/username/repo/branch/main/graph/badge.svg)](https://codecov.io/gh/username/repo)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## 🤝 Contribution

Consultez [CONTRIBUTING.md](.github/CONTRIBUTING.md) pour les règles de contribution.
```

## 🔧 Commandes Utiles

### Vérification des Règles

```bash
# Vérifier les protections de branche
gh api repos/:owner/:repo/branches/main/protection

# Lister les labels
gh label list

# Vérifier les workflows
gh workflow list
```

### Gestion des Branches

```bash
# Créer une branche develop si elle n'existe pas
git checkout -b develop
git push -u origin develop

# Workflow de développement
git checkout main
git pull origin main
git checkout -b feature/nouvelle-fonctionnalite
# ... développement ...
git push -u origin feature/nouvelle-fonctionnalite
# Créer une PR via l'interface GitHub
```

## 📚 Documentation Supplémentaire

- [GitHub Branch Protection](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/defining-the-mergeability-of-pull-requests/about-protected-branches)
- [GitHub Actions](https://docs.github.com/en/actions)
- [Conventional Commits](https://www.conventionalcommits.org/)

## ⚠️ Points d'Attention

1. **Testez d'abord** sur une branche de test
2. **Adaptez les chemins** selon votre structure de projet
3. **Configurez les secrets** avant d'activer le CI/CD
4. **Formez l'équipe** aux nouvelles règles
5. **Commencez progressivement** - activez les règles une par une 