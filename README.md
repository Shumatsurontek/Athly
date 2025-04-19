# Athly - Votre Coach Sportif IA Personnel

Athly est une application de coaching sportif personnel utilisant l'intelligence artificielle pour générer des programmes d'entraînement personnalisés et fournir des conseils d'experts en fonction de vos objectifs, de votre niveau et de vos contraintes.

## Fonctionnalités

- 🏋️ Génération de programmes d'entraînement personnalisés
- 🤖 Interface de chat pour poser des questions à votre coach IA
- 📊 Formats visuels clairs pour vos programmes d'entraînement
- 📱 Interface utilisateur responsive et intuitive

## Architecture

L'application Athly utilise une architecture à base d'agents LangChain:

1. **Agent Orchestrateur**: Coordonne le flux de travail entre les agents spécialisés
2. **Agent Expert en Sport**: Fournit des conseils spécialisés et génère des structures de programmes
3. **Agent Générateur de Tables**: Structure les données d'entraînement en formats visuels

## Prérequis

- Python 3.10+
- Node.js 14+
- Clé API Mistral

## Installation

### Backend

1. Clonez le dépôt:
   ```bash
   git clone https://github.com/votre-username/athly.git
   cd athly
   ```

2. Créez un environnement virtuel et installez les dépendances:
   ```bash
   cd backend
   python -m venv env
   source env/bin/activate  # ou env\Scripts\activate sur Windows
   pip install -r requirements.txt
   ```

3. Créez un fichier `.env` dans le dossier `backend`:
   ```
   MISTRAL_API_KEY=votre_clé_api_mistral
   ```

### Frontend

1. Installez les dépendances:
   ```bash
   cd frontend
   npm install
   ```

## Démarrage

1. Démarrez le backend:
   ```bash
   cd backend
   python main.py
   ```

2. Démarrez le frontend:
   ```bash
   cd frontend
   npm run dev
   ```

3. Accédez à l'application dans votre navigateur: `http://localhost:3000`

## Tests

Pour exécuter les tests:

```bash
cd backend
python -m unittest discover tests
```

## Structure du projet

```
athly/
├── backend/
│   ├── agents/            # Agents LangChain
│   ├── models/            # Base de connaissances
│   ├── data/              # Données d'entraînement
│   ├── logs/              # Logs de l'application
│   └── tests/             # Tests unitaires et d'intégration
├── frontend/
│   ├── public/            # Fichiers statiques
│   └── src/               # Code source React
│       ├── components/    # Composants UI
│       └── pages/         # Pages de l'application
└── docs/                  # Documentation
```

## Obtenir une clé API Mistral

Pour utiliser Athly, vous devez obtenir une clé API Mistral:

1. Créez un compte sur [Mistral AI Platform](https://console.mistral.ai/)
2. Obtenez votre clé API depuis votre espace utilisateur
3. Ajoutez cette clé dans le fichier `.env` du backend

## Dépannage

Si vous rencontrez des erreurs lors de l'initialisation de l'agent, vérifiez:
- La validité de votre clé API Mistral
- La connexion internet
- La version des dépendances dans requirements.txt 