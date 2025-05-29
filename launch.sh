#!/bin/bash

# Script de lancement pour Athly
set -e

echo "🚀 Lancement d'Athly avec Docker..."

# Vérifier que Docker est en cours d'exécution
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker n'est pas en cours d'exécution. Veuillez démarrer Docker Desktop."
    exit 1
fi

# Vérifier que le fichier .env existe
if [ ! -f .env ]; then
    echo "📝 Création du fichier .env à partir de .env.example..."
    cp .env.example .env
    echo "⚠️  N'oubliez pas de configurer vos variables d'environnement dans .env"
fi

# Construire et démarrer tous les services avec Docker
echo "🔨 Construction et démarrage des services..."
docker compose up --build -d

echo "⏳ Attente du démarrage des services..."
sleep 15

# Vérifier que les services sont en cours d'exécution
if docker compose ps | grep -q "Up"; then
    echo "✅ Services démarrés avec succès!"
    echo ""
    echo "🌐 Application disponible sur:"
    echo "   Frontend: http://localhost:3000"
    echo "   Backend API: http://localhost:8000"
    echo "   Documentation API: http://localhost:8000/docs"
    echo ""
    echo "📋 Commandes utiles:"
    echo "   Voir les logs: docker compose logs -f"
    echo "   Voir logs d'un service: docker compose logs -f [backend|frontend]"
    echo "   Arrêter: docker compose down"
    echo "   Redémarrer: docker compose restart"
    echo "   Reconstruire: docker compose up --build"
    echo ""
    echo "🔄 Les services se rechargent automatiquement lors des modifications"
    echo "📊 Monitoring: docker compose ps"
else
    echo "❌ Erreur lors du démarrage des services"
    docker compose logs
    exit 1
fi 