.PHONY: setup test clean

# Variables
PYTHON = python3
TEST_DIR = tests

all: setup test

setup:
	mkdir -p logs
	@echo "Création des répertoires nécessaires..."

test:
	@echo "Exécution des tests unitaires..."
	$(PYTHON) -m unittest discover -s $(TEST_DIR)

test-verbose:
	@echo "Exécution des tests unitaires en mode verbeux..."
	$(PYTHON) -m unittest discover -v -s $(TEST_DIR)

clean:
	@echo "Nettoyage des fichiers temporaires..."
	rm -rf __pycache__
	rm -rf */__pycache__
	rm -rf */*/__pycache__
	rm -rf */*/*/__pycache__
	rm -rf .pytest_cache

help:
	@echo "Commandes disponibles:"
	@echo "  make setup       - Crée les répertoires nécessaires"
	@echo "  make test        - Exécute les tests unitaires"
	@echo "  make test-verbose - Exécute les tests unitaires en mode verbeux"
	@echo "  make clean       - Nettoie les fichiers temporaires" 