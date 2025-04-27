#!/bin/bash

# Vérifier si nous sommes à la racine du projet
if [ ! -d "frontend" ] || [ ! -d "backend" ]; then
  echo "❌ Erreur: Ce script doit être exécuté à la racine du projet (où se trouvent les dossiers frontend et backend)."
  exit 1
fi

# Build du frontend Next.js en mode statique
echo "⚙️ Construction du frontend Next.js (export statique)..."
cd frontend
npm install
npm run build
# Vérifier si le dossier 'out' a été créé
if [ ! -d "out" ]; then
  echo "❌ Erreur: La construction du frontend n'a pas généré de dossier 'out'."
  echo "Vérifiez votre configuration Next.js (next.config.js)."
  exit 1
fi
cd ..

# Arrêt des conteneurs existants si nécessaire
echo "🛑 Arrêt des conteneurs existants..."
docker-compose down

# Construction et démarrage des conteneurs
echo "🚀 Construction et démarrage des conteneurs..."
docker-compose up --build

echo "✅ Application démarrée ! Accessible à l'adresse http://localhost:3000"
echo "📝 Pour voir les logs en temps réel: docker-compose logs -f" 