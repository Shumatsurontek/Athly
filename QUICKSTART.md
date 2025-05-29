# 🚀 Guide de Démarrage Rapide - Athly

## Prérequis

- Docker Desktop installé et en cours d'exécution
- Git

## Démarrage en 3 étapes

### 1. Cloner et configurer

```bash
git clone <votre-repo>
cd Athly
```

### 2. Configurer l'environnement

```bash
# Copier le fichier d'exemple
cp .env.example .env

# Éditer .env avec vos valeurs (optionnel pour le développement)
# Notamment MISTRAL_API_KEY si vous utilisez l'API Mistral
```

### 3. Lancer l'application

```bash
# Option 1: Script automatique (recommandé)
./launch.sh

# Option 2: Commandes manuelles
docker compose up --build -d
```

## Accès à l'application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Documentation API**: http://localhost:8000/docs

## Commandes utiles

```bash
# Voir les logs en temps réel
docker compose logs -f

# Arrêter l'application
docker compose down

# Redémarrer un service
docker compose restart backend

# Reconstruire après des changements
docker compose up --build

# Accéder au shell d'un conteneur
docker compose exec backend bash
docker compose exec frontend sh
```

## Développement avec VS Code

1. Installer l'extension "Dev Containers"
2. Ouvrir le projet dans VS Code
3. Cliquer sur "Reopen in Container" quand proposé
4. VS Code s'ouvrira dans le conteneur backend avec tous les outils configurés

## Structure du projet

```
Athly/
├── backend/          # API Python (FastAPI/Django)
├── frontend/         # Interface React/Next.js
├── .devcontainer/    # Configuration VS Code Dev Containers
├── .github/          # GitHub Actions CI/CD
├── docker-compose.yml
├── .env.example
└── launch.sh         # Script de lancement
```

## Résolution de problèmes

### Docker n'est pas trouvé
```bash
# Vérifier que Docker Desktop est démarré
docker --version
docker compose version
```

### Ports déjà utilisés
```bash
# Vérifier les ports utilisés
lsof -i :3000
lsof -i :8000

# Arrêter les processus ou changer les ports dans docker-compose.yml
```

### Problèmes de permissions
```bash
# Sur macOS/Linux, s'assurer que Docker a les bonnes permissions
sudo chown -R $USER:$USER .
```

## Support

- Consulter les logs: `docker compose logs`
- Issues GitHub: [Lien vers votre repo]
- Documentation complète: `README.md` 