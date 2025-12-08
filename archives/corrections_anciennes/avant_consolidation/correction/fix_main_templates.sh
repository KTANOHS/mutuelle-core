#!/bin/bash

echo "🔧 Correction des templates principaux..."

# 1. liste_membres.html
if [ -f "./templates/assureur/liste_membres.html" ]; then
    echo "📝 Correction de liste_membres.html..."
    
    # Copie de sauvegarde
    cp ./templates/assureur/liste_membres.html ./templates/assureur/liste_membres.html.backup
    
    # Remplacement précis
    sed -i '' '
    # Ligne 20 (ou similaire): bouton Créer un bon
    s|<a href="{% url .creer_bon. membre.id %}"|<a href="{% url '\''assureur:creer_bon_pour_membre'\'' membre.id %}"|g
    
    # Ligne 123 (ou similaire): autre bouton
    s|<a href="{% url .creer_bon. membre.id %}"|<a href="{% url '\''assureur:creer_bon_pour_membre'\'' membre.id %}"|g
    
    # Tous les autres cas
    s|{% url .creer_bon. membre.id %}|{% url '\''assureur:creer_bon_pour_membre'\'' membre.id %}|g
    s|{% url .creer_bon. %}|{% url '\''assureur:creer_bon'\'' %}|g
    ' ./templates/assureur/liste_membres.html
    
    echo "✅ liste_membres.html corrigé"
fi

# 2. detail_membre.html
if [ -f "./templates/assureur/detail_membre.html" ]; then
    echo "📝 Correction de detail_membre.html..."
    
    # Copie de sauvegarde
    cp ./templates/assureur/detail_membre.html ./templates/assureur/detail_membre.html.backup
    
    # Remplacement précis
    sed -i '' '
    # Ligne 20: bouton principal
    s|<a href="{% url .creer_bon. membre.id %}"|<a href="{% url '\''assureur:creer_bon_pour_membre'\'' membre.id %}"|g
    
    # Ligne 123: bouton dans l'onglet
    s|<a href="{% url .creer_bon. membre.id %}"|<a href="{% url '\''assureur:creer_bon_pour_membre'\'' membre.id %}"|g
    
    # Tous les autres cas
    s|{% url .creer_bon. membre.id %}|{% url '\''assureur:creer_bon_pour_membre'\'' membre.id %}|g
    s|{% url .creer_bon. %}|{% url '\''assureur:creer_bon'\'' %}|g
    ' ./templates/assureur/detail_membre.html
    
    echo "✅ detail_membre.html corrigé"
fi

echo "🎉 Templates principaux corrigés !"
