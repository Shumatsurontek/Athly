#!/usr/bin/env python3
import os
import subprocess
import platform
import shutil

def main():
    """
    Script de configuration pour l'application Athly.
    Ce script crée les répertoires nécessaires et installe les dépendances.
    """
    print("🏃 Configuration d'Athly - Votre coach sportif IA personnel 🏋️")
    
    # Création des répertoires
    create_directories()
    
    # Vérification des variables d'environnement
    check_env_variables()
    
    print("\n✅ Configuration terminée!")
    print("Pour installer les dépendances npm, exécutez: npm run install:all")
    print("Pour démarrer l'application: npm run dev")

def create_directories():
    """Crée les répertoires nécessaires pour l'application."""
    print("\n📁 Création des répertoires...")
    
    directories = [
        "backend/data",
        "backend/data/running",
        "backend/data/bodyweight", 
        "backend/data/strength",
        "backend/data/exercises"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"   ✓ {directory} créé")

def check_env_variables():
    """Vérifie si les variables d'environnement nécessaires sont définies."""
    print("\n🔑 Vérification des variables d'environnement...")
    
    env_file_path = "backend/.env"
    if not os.path.exists(env_file_path):
        print(f"   ❌ Le fichier {env_file_path} n'existe pas. Création d'un exemple...")
        with open(env_file_path, "w") as f:
            f.write("# API Keys\n")
            f.write("MISTRAL_API_KEY=votre_clé_api_mistral\n\n")
            f.write("# Configuration\n")
            f.write("DEBUG=True\n")
            f.write("ENVIRONMENT=development\n")
            f.write("PORT=8000\n")
            f.write("HOST=0.0.0.0\n")
        print(f"   ✓ Fichier {env_file_path} créé. Veuillez y ajouter votre clé API Mistral.")
    else:
        with open(env_file_path, "r") as f:
            env_content = f.read()
        
        if "MISTRAL_API_KEY=votre_clé_api_mistral" in env_content:
            print("   ⚠️ Vous devez définir votre clé API Mistral dans le fichier backend/.env")
        else:
            print("   ✓ Fichier .env configuré")
    
    # Installation de pip et des dépendances Python
    print("\n📦 Installation des dépendances Python...")
    try:
        print("   ⚙️ Vérifiez que vous avez installé les dépendances Python avec la commande:")
        print("   pip install -r backend/requirements.txt")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")

if __name__ == "__main__":
    main() 