#!/bin/bash

# Script de lancement pour Athly
set -e

echo "🚀 Lancement d'Athly..."

# Vérifier que Docker est en cours d'exécution
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker n'est pas en cours d'exécution. Veuillez démarrer Docker Desktop."
    exit 1
fi

# Vérifier que Node.js est installé
if ! command -v node &> /dev/null; then
    echo "❌ Node.js n'est pas installé. Veuillez installer Node.js."
    exit 1
fi

# Vérifier que le fichier .env existe
if [ ! -f .env ]; then
    echo "📝 Création du fichier .env à partir de .env.example..."
    cp .env.example .env
    echo "⚠️  N'oubliez pas de configurer vos variables d'environnement dans .env"
fi

# Construire et démarrer le backend avec Docker
echo "🔨 Construction et démarrage du backend..."
docker compose -f docker-compose.dev.yml up --build -d

echo "⏳ Attente du démarrage du backend..."
sleep 5

# Installer les dépendances du frontend si nécessaire
if [ ! -d "frontend/node_modules" ]; then
    echo "📦 Installation des dépendances du frontend..."
    cd frontend && npm install && cd ..
fi

# Démarrer le frontend en local
echo "🌐 Démarrage du frontend..."
cd frontend && npm run dev &
FRONTEND_PID=$!
cd ..

echo "⏳ Attente du démarrage du frontend..."
sleep 10

# Vérifier que les services sont en cours d'exécution
if docker compose -f docker-compose.dev.yml ps | grep -q "Up"; then
    echo "✅ Services démarrés avec succès!"
    echo ""
    echo "🌐 Application disponible sur:"
    echo "   Frontend: http://localhost:3000"
    echo "   Backend API: http://localhost:8000"
    echo ""
    echo "📋 Commandes utiles:"
    echo "   Voir les logs backend: docker compose -f docker-compose.dev.yml logs -f"
    echo "   Arrêter backend: docker compose -f docker-compose.dev.yml down"
    echo "   Arrêter frontend: kill $FRONTEND_PID"
    echo "   Redémarrer: ./launch.sh"
    echo ""
    echo "🔄 Le frontend se recharge automatiquement lors des modifications"
    echo "🔄 Le backend se recharge automatiquement lors des modifications"
else
    echo "❌ Erreur lors du démarrage du backend"
    docker compose -f docker-compose.dev.yml logs
    exit 1
fi 