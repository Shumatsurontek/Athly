#!/bin/bash

echo "🚀 Lancement d'Athly en mode développement..."

# Vérifier que Docker est en cours d'exécution
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker n'est pas en cours d'exécution. Veuillez démarrer Docker Desktop."
    exit 1
fi

# Arrêter les services existants
echo "🛑 Arrêt des services existants..."
docker compose down

# Construire et démarrer les services
echo "🔨 Construction et démarrage des services..."
docker compose up --build -d

echo "⏳ Attente du démarrage des services..."
sleep 10

# Vérifier que les services sont en cours d'exécution
if docker compose ps | grep -q "Up"; then
    echo "✅ Services démarrés avec succès!"
    echo ""
    echo "🌐 Application disponible sur:"
    echo "   Frontend: http://localhost:3000"
    echo "   Backend API: http://localhost:8000"
    echo ""
    echo "📋 Commandes utiles:"
    echo "   Voir les logs: docker compose logs -f"
    echo "   Arrêter: docker compose down"
else
    echo "❌ Erreur lors du démarrage des services"
    docker compose logs
    exit 1
fi 