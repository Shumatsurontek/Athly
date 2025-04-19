# Athly - Votre coach sportif IA personnel

Athly est une application web qui utilise l'intelligence artificielle pour générer des programmes d'entraînement personnalisés et fournir des conseils adaptés à vos objectifs sportifs.

## Fonctionnalités

- **Chat Intelligent** : Posez vos questions et obtenez des conseils personnalisés
- **Programmes Personnalisés** : Générez des programmes d'entraînement sur mesure
- **Approche Multisport** : Combinez course à pied, musculation et exercices au poids du corps

## Technologies utilisées

### Frontend
- Next.js / React
- TypeScript
- CSS Modules

### Backend
- Python
- FastAPI
- Mistral AI API

## Installation

### Prérequis
- Node.js (v14+)
- Python 3.8+
- Clé API Mistral AI

### Étapes d'installation

1. Clonez le dépôt
```bash
git clone https://github.com/[votre-nom]/athly.git
cd athly
```

2. Installez les dépendances
```bash
# Dépendances principales et frontend
npm run install:all

# Dépendances backend (dans un environnement virtuel Python)
python -m venv env
source env/bin/activate  # Sur Windows: env\Scripts\activate
pip install -r backend/requirements.txt
```

3. Configurez l'environnement
   - Créez un fichier `backend/.env` avec votre clé API Mistral:
```
MISTRAL_API_KEY=votre_clé_api_mistral
DEBUG=True
ENVIRONMENT=development
PORT=8000
HOST=0.0.0.0
```

4. Lancez l'application
```bash
# Mode développement (lance le backend et le frontend)
npm run dev

# Ou séparément:
npm run frontend
npm run backend
```

## Structure du projet

- `frontend/` - Application Next.js
  - `src/pages/` - Pages de l'application
  - `src/components/` - Composants React réutilisables
  - `public/` - Fichiers statiques
- `backend/` - API FastAPI
  - `agents/` - Agents IA spécialisés
  - `models/` - Modèles de données et base de connaissances
  - `data/` - Données d'entraînement et ressources

## Contributions

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou à soumettre une pull request.

## Licence

Ce projet est sous licence MIT 