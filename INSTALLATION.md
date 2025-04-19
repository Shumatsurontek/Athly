# Guide d'installation et de configuration d'Athly

Ce guide vous explique comment installer et configurer l'application Athly, votre coach sportif IA personnel.

## Prérequis

- Python 3.10+
- Node.js 14+
- Git

## Installation du Backend

1. Clonez le dépôt:
   ```bash
   git clone https://github.com/votre-username/athly.git
   cd athly
   ```

2. Créez un environnement virtuel Python et installez les dépendances:
   ```bash
   cd backend
   python -m venv env
   source env/bin/activate  # ou env\Scripts\activate sur Windows
   pip install -r requirements.txt
   ```

3. Configurez l'API Mistral:
   - Créez un compte sur [Mistral AI Platform](https://console.mistral.ai/)
   - Obtenez votre clé API depuis votre espace utilisateur
   - Modifiez le fichier `.env` dans le dossier `backend`:
     ```
     MISTRAL_API_KEY=votre_clé_api_mistral
     ```

## Installation du Frontend

1. Installez les dépendances:
   ```bash
   cd frontend
   npm install
   ```

## Démarrage de l'application

1. Démarrez le backend:
   ```bash
   cd backend
   source env/bin/activate  # ou env\Scripts\activate sur Windows
   python main.py
   ```

2. Démarrez le frontend:
   ```bash
   cd frontend
   npm run dev
   ```

3. Accédez à l'application dans votre navigateur: `http://localhost:3000`

## Architecture de l'agent

Athly utilise une architecture à base d'agents LangChain:

1. **Agent Orchestrateur**: Coordonne le flux de travail entre les agents spécialisés
2. **Agent Expert en Sport**: Fournit des conseils spécialisés et génère des structures de programmes
3. **Agent Générateur de Tables**: Structure les données d'entraînement en formats visuels

## Débogage de l'application

### Mode DEBUG et étapes intermédiaires

Pour activer le mode DEBUG et voir les étapes intermédiaires des agents:

1. Assurez-vous que `DEBUG=True` est défini dans votre fichier `.env`
2. Consultez les logs dans `backend/logs/app.log` pour voir les étapes détaillées

Les étapes intermédiaires vous montrent:
- Chaque appel d'outil effectué par l'agent
- Les entrées et sorties de chaque outil
- Le raisonnement de l'agent à chaque étape

### Suivi des performances

Pour suivre les performances et le temps d'exécution:
- Le temps total d'exécution de chaque opération est enregistré dans les logs
- Les requêtes longues (génération de programme) utilisent un timeout plus long (5 minutes)

## Dépannage

Si vous rencontrez des erreurs lors de l'initialisation de l'agent, vérifiez:
- La validité de votre clé API Mistral
- La connexion internet
- La version des dépendances dans requirements.txt

### Erreurs spécifiques à Mistral

Si l'agent ne répond pas correctement ou génère des erreurs de parsing:

1. Vérifiez que le format JSON est correctement défini dans le prompt
2. Utilisez un température plus basse (0.3-0.5) pour obtenir des réponses plus déterministes
3. Augmentez le nombre d'exemples dans le prompt si le modèle a du mal à suivre le format demandé

### Paramètres avancés de l'agent

L'agent est configuré avec:
- `max_iterations=25` - Permet jusqu'à 25 étapes d'exécution avant d'arrêter
- `early_stopping_method="generate"` - Génère une réponse finale si l'agent atteint le nombre maximum d'itérations
- Gestion personnalisée des erreurs de parsing - Permet à l'agent de continuer même en cas d'erreur de format 