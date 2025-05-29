# Guide de Contribution

## 🚀 Configuration du Projet

### Prérequis
- Node.js 18+ et npm/yarn
- Python 3.9+
- Git configuré avec votre nom et email

### Installation
```bash
# Clone du repo
git clone <repo-url>
cd <project-name>

# Frontend
cd frontend
npm install

# Backend
cd ../backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 📋 Workflow de Développement

### 1. Création de Branches
```bash
# Toujours partir de main à jour
git checkout main
git pull origin main

# Créer une branche feature
git checkout -b feature/nom-de-la-feature
# ou pour un bugfix
git checkout -b fix/description-du-bug
```

### 2. Convention de Nommage des Branches
- `feature/` - Nouvelles fonctionnalités
- `fix/` - Corrections de bugs
- `hotfix/` - Corrections urgentes
- `refactor/` - Refactoring de code
- `docs/` - Documentation uniquement

### 3. Commits
Utilisez les [Conventional Commits](https://www.conventionalcommits.org/):

```
type(scope): description

feat(auth): add JWT authentication
fix(api): resolve user creation bug
docs(readme): update installation guide
style(frontend): fix linting issues
refactor(backend): optimize database queries
test(api): add user endpoint tests
```

Types autorisés: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

## 🔍 Standards de Code

### Frontend (JavaScript/TypeScript)
- ESLint + Prettier configurés
- Tests avec Jest/Vitest
- Composants en PascalCase
- Fonctions en camelCase

### Backend (Python)
- Black pour le formatage
- Flake8 pour le linting
- Type hints obligatoires
- Tests avec pytest

## 📝 Pull Requests

### Template de PR
```markdown
## Description
Brève description des changements

## Type de changement
- [ ] Bug fix
- [ ] Nouvelle fonctionnalité
- [ ] Breaking change
- [ ] Documentation

## Tests
- [ ] Tests unitaires ajoutés/mis à jour
- [ ] Tests d'intégration passent
- [ ] Tests manuels effectués

## Checklist
- [ ] Code respecte les standards
- [ ] Documentation mise à jour
- [ ] Pas de conflits avec main
- [ ] CI/CD passe
```

### Critères d'Acceptation
1. ✅ Tous les tests passent
2. ✅ Code review approuvé par 2 développeurs
3. ✅ Pas de conflits
4. ✅ Documentation à jour
5. ✅ Performance acceptable

## 🛡️ Règles de Protection

### Branche `main`
- Pas de push direct
- PR obligatoire avec review
- Tests CI/CD requis
- Historique linéaire préféré

### Branche `develop`
- PR obligatoire
- 1 review minimum
- Tests requis

## 🚨 Urgences

Pour les hotfixes critiques:
1. Créer `hotfix/description`
2. PR directe vers `main`
3. Notification immédiate de l'équipe
4. Merge rapide après review express

## 📞 Support

- Issues GitHub pour bugs/features
- Discussions pour questions
- Slack #dev pour communication rapide 