# Athly - Coach IA personnel

Athly est une application de coaching sportif IA qui génère des programmes d'entraînement personnalisés et fournit des conseils adaptés aux besoins des utilisateurs.

## Fonctionnalités

- Interface de chat avec un coach IA
- Génération de programmes d'entraînement personnalisés
- Export des programmes en format Excel
- Base de connaissances sur les exercices et méthodes d'entraînement
- Support pour plusieurs modèles d'IA (Mistral AI et Qwen)
- Intégration de données de programmes d'entraînement via des fichiers Excel

## Configuration

1. Cloner le repository
2. Installer les dépendances backend:
```bash
cd backend
pip install -r requirements.txt
pip install -r requirements-ml.txt
```

3. Installer les dépendances frontend:
```bash
cd frontend
npm install
```

4. Créer un fichier `.env` dans le dossier backend avec:
```
MISTRAL_API_KEY=your_mistral_api_key_here
HUGGINGFACE_API_KEY=your_huggingface_api_key_here
USE_QWEN=true
```

## Utilisation des Fichiers Excel pour les Programmes

### Structure des Fichiers

Pour utiliser vos propres programmes d'entraînement, placez des fichiers Excel (.xlsx) dans le dossier `backend/data/programs/`. Chaque fichier doit suivre cette structure:

1. Une feuille "Introduction" avec une colonne nommée "Introduction" contenant la description du programme
2. Des feuilles "Semaine 1", "Semaine 2", etc. avec les détails des séances pour chaque semaine

Nommez vos fichiers avec des mots-clés descriptifs, par exemple: `course_debutant_8semaines.xlsx`

### API pour les Programmes

L'application expose les endpoints suivants:

- `POST /api/programs/list` - Liste tous les programmes disponibles
- `GET /api/programs/{program_name}` - Obtient les détails d'un programme spécifique

## Lancement de l'Application

1. Démarrer le backend:
```bash
cd backend
uvicorn main:app --reload
```

2. Démarrer le frontend:
```bash
cd frontend
npm run dev
```

3. Accéder à l'application à l'adresse: [http://localhost:3000](http://localhost:3000)

## Choix du Modèle d'IA

Vous pouvez choisir le modèle d'IA à utiliser:

- **Mistral AI**: Modèle par défaut, nécessite une clé API Mistral
- **Qwen (Hugging Face)**: Alternative via l'API Hugging Face, activée en mettant `USE_QWEN=true` dans le fichier `.env`

## Développement

Pour tester le modèle IA directement sans passer par les agents:
- Accéder à [http://localhost:8000/static/test.html](http://localhost:8000/static/test.html)

## Architecture

L'application Athly utilise une architecture à base d'agents LangChain:

1. **Agent Orchestrateur**: Coordonne le flux de travail entre les agents spécialisés
2. **Agent Expert en Sport**: Fournit des conseils spécialisés et génère des structures de programmes
3. **Agent Générateur de Tables**: Structure les données d'entraînement en formats visuels

## Prérequis

- Python 3.10+
- Node.js 14+
- Clé API Mistral

## Tests

Pour exécuter les tests:

```bash
cd backend
python -m unittest discover tests
```